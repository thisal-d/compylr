"""
Compylr - app.py
Main application window.
"""

import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import subprocess
import shutil
import sys
import os
import json
from pathlib import Path

from compylr.theme import DARK, LIGHT, FONTS, get_theme
from compylr.widgets import (
    SectionCard, OptionRow, AnimatedToggle, StyledEntry,
    StyledDropdown, StyledTextArea, PurpleButton, LogTerminal, ScrollableFrame
)
from compylr.nuitka_options import NUITKA_SECTIONS, build_nuitka_command

SETTINGS_FILE = Path.home() / ".compylr" / "settings.json"

# Known Nuitka error patterns → helpful user hints
_ERROR_HINTS = {
    "PermissionError": (
        "⚠  A previous build left a locked file.\n"
        "   → Enable 'Clean Build Directory' and retry."
    ),
    "__constants.h: No such file or directory": (
        "⚠  Corrupted build cache from a previous failed/killed build.\n"
        "   → Enable 'Clean Build Directory' and retry."
    ),
    "FATAL: Failed unexpectedly in Scons C backend": (
        "⚠  C compilation backend crashed. Common causes:\n"
        "   • Corrupted build directory — enable Clean Build\n"
        "   • Missing compiler — install Visual Studio C++ tools\n"
        "   • Anti-virus blocking compiler — add exclusion"
    ),
    "The '--mode' option requires an argument": (
        "⚠  Nuitka flag format error. This is a Compylr bug — please report it."
    ),
    "fatal error:": (
        "⚠  C compiler error. Check that your C compiler is installed correctly."
    ),
    "ModuleNotFoundError": (
        "⚠  A Python module was not found at compile time.\n"
        "   → Add it to 'Include Modules' in the Module & Package Inclusion section."
    ),
    "clcache": (
        "⚠  clcache issue — try switching compiler to MSVC or MinGW64."
    ),
}


class _NuitkaLogFilter:
    """
    Filters and compresses the extremely verbose Nuitka-Progress output.

    Rules:
    • "Nuitka-Progress: Not finished with the module…"  →  silently absorbed
    • "Nuitka-Progress: Optimizing module 'X', N more…"  →  shown as a compact
      one-liner that overwrites the last progress line in the same batch
    • "Nuitka-Progress: PASS N:"                         →  emitted as a section header
    • Everything else (warnings, errors, Nuitka-Options, Scons, etc.)  →  passed through
    """

    # Lines that contain any of these strings are dropped entirely
    _DROP_CONTAINS = (
        "Not finished with the module due to",
        "Doing module local optimizations",
        "Doing module dependency considerations",
        "Nuitka-Memory: Total memory",
    )
    # Lines that start with these prefixes are summarised
    _OPT_PREFIX = "Nuitka-Progress: Optimizing module "
    _PASS_PREFIX = "Nuitka-Progress: PASS"

    def __init__(self):
        self._pass_num = 0          # current PASS number
        self._mod_count = 0         # modules optimized this PASS
        self._pending_summary = ""  # last "Optimizing module" line (not yet emitted)

    def process(self, line: str):
        """
        Returns (display_text, kind) to log, or None to suppress.
        """
        # ── PASS header ───────────────────────────────────────────────
        if line.startswith(self._PASS_PREFIX):
            # Flush any pending module summary first
            flush = self.flush()
            self._pass_num += 1
            self._mod_count = 0
            header = f"\n{'- '*30}\n  {line.strip()}\n{'- '*30}"
            results = []
            if flush:
                results.append(flush)
            results.append((header, "info"))
            # We can only return one value; chain via a side-effect approach:
            # store extra items and return the most recent
            self._pending_extras = results[:-1]
            return results[-1]

        # ── Suppressed noise ──────────────────────────────────────────
        for fragment in self._DROP_CONTAINS:
            if fragment in line:
                return None

        # ── Module optimisation progress ──────────────────────────────
        if line.startswith(self._OPT_PREFIX):
            rest = line[len(self._OPT_PREFIX):]
            # rest looks like "'some.module', 42 more modules to go after that."
            try:
                mod_name = rest.split("'")[1]
                remaining = rest.split(",")[1].strip().split()[0]
                self._mod_count += 1
                self._pending_summary = (
                    f"  ⚙  Optimizing: {mod_name}  ({remaining} remaining)",
                    "plain"
                )
            except (IndexError, ValueError):
                self._pending_summary = (line, "plain")
            # Emit progress every 5 modules to avoid flooding
            if self._mod_count % 5 == 1:
                return self._pending_summary
            return None

        # ── Everything else passes through ────────────────────────────
        # Flush any pending summary before the next real line
        flush = self.flush()
        if flush and flush[0] != self._pending_summary:
            # There's a pending unshown summary — we need to emit it too
            # but we can only return one. Store it to be emitted next tick.
            # Simple approach: emit the real line and prepend the summary
            combined = f"{flush[0]}\n{line}"
            self._pending_summary = ""
            return combined, self._classify(line)

        self._pending_summary = ""
        return line, self._classify(line)

    def flush(self):
        """Return the last pending summary line (if any) and clear it."""
        if self._pending_summary:
            result = self._pending_summary
            self._pending_summary = ""
            return result
        return None

    @staticmethod
    def _classify(line: str) -> str:
        lo = line.lower()
        if "fatal error" in lo or "permissionerror" in lo: return "error"
        if "error" in lo:   return "error"
        if "warning" in lo: return "warning"
        if any(lo.startswith(p) for p in ("nuitka", "scons")): return "info"
        return "plain"


class CompylrApp:
    APP_TITLE = "Compylr"
    MIN_W, MIN_H = 1100, 720

    def __init__(self):
        self._mode = "dark"
        self._t = DARK.copy()
        ctk.set_appearance_mode(self._mode)
        self.root = ctk.CTk()
        self._t = DARK.copy()
        self._script_var = tk.StringVar()
        self._python_var = tk.StringVar(value=sys.executable)
        self._option_vars: dict = {}
        self._ctrl_widgets: dict = {}
        self._section_index = 0
        self._build_process: subprocess.Popen = None
        self._is_building = False
        self._clean_build_var = tk.BooleanVar(value=True)
        self._load_settings()
        self._setup_root()
        self._build_ui()

    # ── Bootstrap ──────────────────────────────────────────────────────
    def _setup_root(self):
        t = self._t
        self.root.title(self.APP_TITLE)
        self.root.minsize(self.MIN_W, self.MIN_H)
        self.root.geometry("1280x800")
        self.root.configure(fg_color=t["bg"])
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        
        # Load window icon
        try:
            icon_path = Path(__file__).parent / "logo" / "logo.ico"
            if icon_path.exists():
                self.root.iconbitmap(str(icon_path))
        except Exception:
            pass

    # ── Settings persistence ───────────────────────────────────────────
    def _load_settings(self):
        try:
            if SETTINGS_FILE.exists():
                data = json.loads(SETTINGS_FILE.read_text())
                self._mode = data.get("theme", "dark")
                self._t = get_theme(self._mode)
                self._script_var.set(data.get("last_script", ""))
                self._python_var.set(data.get("last_python", sys.executable))
        except Exception:
            pass

    def _save_settings(self):
        try:
            SETTINGS_FILE.parent.mkdir(parents=True, exist_ok=True)
            data = {
                "theme": self._mode,
                "last_script": self._script_var.get(),
                "last_python": self._python_var.get(),
            }
            SETTINGS_FILE.write_text(json.dumps(data, indent=2))
        except Exception:
            pass

    def _on_close(self):
        self._save_settings()
        if self._build_process and self._is_building:
            self._build_process.terminate()
        self.root.destroy()

    # ── Main UI layout ─────────────────────────────────────────────────
    def _build_ui(self):
        self._pages: dict = {}
        self._nav_btns: list = []
        self._build_titlebar()
        main = ctk.CTkFrame(self.root, fg_color=self._t["bg"], corner_radius=0)
        main.pack(fill="both", expand=True)
        self._build_sidebar(main)
        self._build_content(main)

    def _build_titlebar(self):
        t = self._t
        bar = ctk.CTkFrame(self.root, fg_color=t["bg_header"], height=52, corner_radius=0)
        bar.pack(fill="x")
        bar.pack_propagate(False)

        # Load and render logo
        logo_loaded = False
        try:
            from PIL import Image
            logo_path = Path(__file__).parent / "logo" / "logo.png"
            if logo_path.exists():
                logo_img = ctk.CTkImage(
                    light_image=Image.open(logo_path),
                    dark_image=Image.open(logo_path),
                    size=(24, 24)
                )
                logo_lbl = ctk.CTkLabel(bar, image=logo_img, text="")
                logo_lbl.pack(side="left", padx=(14, 8))
                logo_loaded = True
        except Exception:
            pass

        if not logo_loaded:
            ctk.CTkLabel(bar, text="⚡", font=("Segoe UI", 20),
                     text_color=t["accent"]).pack(side="left", padx=(14, 4))

        ctk.CTkLabel(bar, text="Compylr", font=("Segoe UI", 16, "bold"),
                 text_color=t["text"]).pack(side="left")
        ctk.CTkLabel(bar, text=" — Python → EXE",
                 font=("Segoe UI", 13), 
                 text_color=t["text_muted"]).pack(side="left", padx=4)

        # Theme toggle
        theme_frm = ctk.CTkFrame(bar, fg_color="transparent")
        theme_frm.pack(side="right", padx=14)
        ctk.CTkLabel(theme_frm, text="☀", font=("Segoe UI", 16),
                 text_color=t["text_muted"]).pack(side="left", padx=6)
        self._theme_var = tk.BooleanVar(value=(self._mode == "dark"))
        AnimatedToggle(theme_frm, variable=self._theme_var, theme=t,
                       command=self._toggle_theme).pack(side="left", padx=4, pady=12)
        ctk.CTkLabel(theme_frm, text="🌙", font=("Segoe UI", 16),
                 text_color=t["text_muted"]).pack(side="left", padx=6)

    # ── Sidebar ────────────────────────────────────────────────────────
    def _build_sidebar(self, parent):
        t = self._t
        self._sidebar = ctk.CTkFrame(parent, fg_color=t["bg_sidebar"], width=230, corner_radius=0)
        self._sidebar.pack(side="left", fill="y")
        self._sidebar.pack_propagate(False)

        ctk.CTkLabel(self._sidebar, text="SECTIONS",
                 font=("Segoe UI", 11, "bold"),
                 text_color=t["text_dim"]).pack(anchor="w", padx=16, pady=(16, 6))

        sections = NUITKA_SECTIONS + [{"title": "Build", "icon": "🚀"}]
        for i, sec in enumerate(sections):
            lbl = ctk.CTkLabel(
                self._sidebar,
                text=f"  {sec['icon']}  {sec['title']}",
                font=("Segoe UI", 13),
                text_color=t["text_muted"], 
                fg_color="transparent",
                anchor="w", cursor="hand2", pady=9, padx=12,
                corner_radius=6
            )
            lbl.pack(fill="x", padx=12, pady=2)
            idx = i
            lbl.bind("<Enter>", lambda e, l=lbl: l.configure(fg_color=t["bg_hover"], text_color=t["text"]))
            lbl.bind("<Leave>", lambda e, l=lbl, ii=idx: self._nav_leave(l, ii))
            lbl.bind("<Button-1>", lambda e, ii=idx: self._nav_select(ii))
            self._nav_btns.append(lbl)

    def _nav_leave(self, lbl, idx):
        t = self._t
        if idx == self._section_index:
            lbl.configure(fg_color=t["bg_active"], text_color=t["text"])
        else:
            lbl.configure(fg_color="transparent", text_color=t["text_muted"])

    def _nav_select(self, idx):
        t = self._t
        self._section_index = idx
        for i, btn in enumerate(self._nav_btns):
            if i == idx:
                btn.configure(fg_color=t["bg_active"], text_color=t["text"],
                           font=("Segoe UI", 13, "bold"))
            else:
                btn.configure(fg_color="transparent", text_color=t["text_muted"],
                           font=("Segoe UI", 13))
        self._show_section(idx)

    # ── Content ────────────────────────────────────────────────────────
    def _build_content(self, parent):
        t = self._t
        self._content_area = ctk.CTkFrame(parent, fg_color=t["bg"], corner_radius=0)
        self._content_area.pack(side="left", fill="both", expand=True)
        for i, sec in enumerate(NUITKA_SECTIONS):
            self._pages[i] = self._build_option_page(sec)
        self._pages[len(NUITKA_SECTIONS)] = self._build_build_page()
        self._nav_select(0)

    def _show_section(self, idx):
        for page in self._pages.values():
            page.pack_forget()
        if idx in self._pages:
            self._pages[idx].pack(fill="both", expand=True)

    # ── Option pages ───────────────────────────────────────────────────
    def _build_option_page(self, section: dict) -> ctk.CTkFrame:
        t = self._t
        page = ctk.CTkFrame(self._content_area, fg_color=t["bg"], corner_radius=0)
        self._build_source_bar(page)
        sf = ScrollableFrame(page, theme=t)
        sf.pack(fill="both", expand=True, padx=16, pady=8)
        card = SectionCard(sf.inner, section["title"], section["icon"], t)
        card.pack(fill="x", pady=6)
        for opt in section["options"]:
            self._build_option_row(card.body, opt)
        return page

    def _build_source_bar(self, parent):
        t = self._t
        bar = ctk.CTkFrame(parent, fg_color=t["bg_card"],
                       border_color=t["border_card"], border_width=1, corner_radius=8)
        bar.pack(fill="x", padx=16, pady=(12, 0))

        ctk.CTkLabel(bar, text="Script:", font=("Segoe UI", 13, "bold"),
                 text_color=t["text"]).pack(side="left", padx=(12, 4), pady=12)
        self._script_entry = StyledEntry(
            bar, theme=t, textvariable=self._script_var,
            placeholder="Select your .py file...")
        self._script_entry.pack(side="left", fill="x", expand=True, padx=4)
        PurpleButton(bar, "Browse...", t, command=self._browse_script,
                     style="secondary").pack(side="left", padx=4)

        ctk.CTkLabel(bar, text="Python:", font=("Segoe UI", 13),
                 text_color=t["text_muted"]).pack(side="left", padx=(8, 4))
        self._python_entry = StyledEntry(
            bar, theme=t, textvariable=self._python_var, width=220)
        self._python_entry.pack(side="left", padx=4)
        PurpleButton(bar, "...", t, command=self._browse_python,
                     style="ghost").pack(side="left", padx=(0, 10))

    def _browse_script(self):
        p = filedialog.askopenfilename(
            title="Select Python Script",
            filetypes=[("Python Files", "*.py"), ("All Files", "*.*")])
        if p:
            self._script_var.set(p)

    def _browse_python(self):
        p = filedialog.askopenfilename(
            title="Select Python Interpreter",
            filetypes=[("Executables", "*.exe"), ("All Files", "*.*")])
        if p:
            self._python_var.set(p)

    def _build_option_row(self, parent, opt):
        t = self._t
        row = OptionRow(parent, opt.label, opt.tooltip, t)
        row.pack(fill="x", pady=4)

        if opt.type == "bool":
            var = tk.BooleanVar(value=bool(opt.default))
            self._option_vars[opt.key] = var
            toggle = AnimatedToggle(row.ctrl, variable=var, theme=t)
            toggle.pack(side="left", padx=2)
            self._ctrl_widgets[opt.key] = toggle

        elif opt.type == "choice":
            var = tk.StringVar(value=str(opt.default or (opt.choices[0] if opt.choices else "")))
            self._option_vars[opt.key] = var
            dd = StyledDropdown(row.ctrl, var, opt.choices or [], t)
            dd.pack(side="left", fill="x", expand=True)
            self._ctrl_widgets[opt.key] = dd

        elif opt.type in ("text", "file", "dir"):
            var = tk.StringVar(value=str(opt.default or ""))
            self._option_vars[opt.key] = var
            frm = ctk.CTkFrame(row.ctrl, fg_color="transparent")
            frm.pack(fill="x", expand=True)
            entry = StyledEntry(frm, theme=t, textvariable=var,
                                placeholder=opt.placeholder)
            entry.pack(side="left", fill="x", expand=True)
            if opt.type == "file":
                def _browse_file(v=var):
                    p = filedialog.askopenfilename()
                    if p: v.set(p)
                PurpleButton(frm, "...", t, command=_browse_file,
                             style="ghost").pack(side="left", padx=4)
            elif opt.type == "dir":
                def _browse_dir(v=var):
                    p = filedialog.askdirectory()
                    if p: v.set(p)
                PurpleButton(frm, "…", t, command=_browse_dir,
                             style="ghost").pack(side="left", padx=4)
            self._ctrl_widgets[opt.key] = entry

        elif opt.type == "multi_text":
            var = tk.StringVar(value=str(opt.default or ""))
            self._option_vars[opt.key] = var
            ta = StyledTextArea(row.ctrl, theme=t, height=60,
                                placeholder=opt.placeholder)
            ta.pack(fill="x", expand=True)
            self._ctrl_widgets[opt.key] = ta

    # ── Build page ─────────────────────────────────────────────────────
    def _build_build_page(self) -> ctk.CTkFrame:
        t = self._t
        page = ctk.CTkFrame(self._content_area, fg_color=t["bg"], corner_radius=0)
        self._build_source_bar(page)

        # ── Command preview ────────────────────────────────────────────
        preview_card = ctk.CTkFrame(page, fg_color=t["bg_card"],
                                border_color=t["border_card"],
                                border_width=1, corner_radius=8)
        preview_card.pack(fill="x", padx=16, pady=(10, 0))
        hdr = ctk.CTkFrame(preview_card, fg_color=t["bg_active"], corner_radius=0)
        hdr.pack(fill="x")
        ctk.CTkLabel(hdr, text="  📋  Generated Command",
                 font=("Segoe UI", 13, "bold"),
                 text_color=t["text_accent"]).pack(side="left", padx=8, pady=6)
        PurpleButton(hdr, "↻ Refresh", t,
                     command=self._refresh_preview, style="ghost").pack(side="right", padx=8)
        self._cmd_preview = ctk.CTkTextbox(
            preview_card, font=("Consolas", 12), height=60,
            fg_color=t["bg_input"], text_color=t["terminal_purple"],
            border_width=0, corner_radius=6, wrap="word")
        self._cmd_preview.configure(state="disabled")
        self._cmd_preview.pack(fill="x", padx=10, pady=8)

        # ── Build options bar ──────────────────────────────────────────
        opts_bar = ctk.CTkFrame(page, fg_color=t["bg_card"],
                            border_color=t["border_card"], border_width=1, corner_radius=8)
        opts_bar.pack(fill="x", padx=16, pady=(6, 0))

        # Clean Build toggle
        cb_frm = ctk.CTkFrame(opts_bar, fg_color="transparent")
        cb_frm.pack(side="left", padx=12, pady=8)
        AnimatedToggle(cb_frm, variable=self._clean_build_var, theme=t).pack(side="left", padx=(0, 6))
        ctk.CTkLabel(cb_frm,
                 text="Clean build directory before build",
                 font=("Segoe UI", 12),
                 text_color=t["text_muted"]).pack(side="left")

        # Nuitka version display
        self._nuitka_ver_var = tk.StringVar(value="")
        ctk.CTkLabel(opts_bar, textvariable=self._nuitka_ver_var,
                 font=("Segoe UI", 12), text_color=t["text_dim"]).pack(side="right", padx=12)
        self.root.after(200, self._detect_nuitka_version)

        # ── Action buttons ─────────────────────────────────────────────
        btn_bar = ctk.CTkFrame(page, fg_color="transparent")
        btn_bar.pack(fill="x", padx=16, pady=10)

        self._build_btn = PurpleButton(
            btn_bar, "🚀  Build Executable", t,
            command=self._start_build, style="primary")
        self._build_btn.pack(side="left", padx=(0, 8))

        self._stop_btn = PurpleButton(
            btn_bar, "⏹  Stop", t, command=self._stop_build, style="danger")
        self._stop_btn.pack(side="left", padx=(0, 8))
        self._stop_btn.configure(state="disabled")

        PurpleButton(btn_bar, "📋  Copy Command", t,
                     command=self._copy_command, style="secondary").pack(side="left", padx=(0, 8))
        PurpleButton(btn_bar, "🗑  Clear Log", t,
                     command=lambda: self._log.clear(), style="ghost").pack(side="left")

        # ── Status bar ─────────────────────────────────────────────────
        self._status_var = tk.StringVar(value="Ready")
        status_bar = ctk.CTkFrame(page, fg_color=t["bg_card"],
                              border_color=t["border_card"], border_width=1, corner_radius=6)
        status_bar.pack(fill="x", padx=16)
        self._status_dot = ctk.CTkLabel(status_bar, text="●",
                                    font=("Segoe UI", 14),
                                    text_color=t["text_muted"])
        self._status_dot.pack(side="left", padx=(10, 4))
        ctk.CTkLabel(status_bar, textvariable=self._status_var,
                 font=("Segoe UI", 13),
                 text_color=t["text_muted"]).pack(side="left")

        # ── Log terminal ───────────────────────────────────────────────
        log_card = ctk.CTkFrame(page, fg_color=t["bg_card"],
                            border_color=t["border_card"], border_width=1, corner_radius=8)
        log_card.pack(fill="both", expand=True, padx=16, pady=(8, 16))
        ctk.CTkLabel(log_card, text="  🖥  Build Output",
                 font=("Segoe UI", 13, "bold"),
                 text_color=t["text_accent"]).pack(fill="x", pady=6)
        self._log = LogTerminal(log_card, t)
        self._log.pack(fill="both", expand=True, padx=4, pady=(0, 4))

        self._log.write("Welcome to Compylr ⚡", "info")
        self._log.write("Configure options in the left panel, then click Build.", "plain")
        self._log.write("", "plain")
        self._log.write("Tip: Enable 'Clean build directory' to fix corrupted-cache errors.", "info")

        return page

    # ── Nuitka version detection ───────────────────────────────────────
    def _detect_nuitka_version(self):
        try:
            py = self._python_var.get().strip() or sys.executable
            result = subprocess.run(
                [py, "-m", "nuitka", "--version"],
                capture_output=True, text=True, timeout=5
            )
            ver = result.stdout.strip().splitlines()[0] if result.stdout else "unknown"
            self._nuitka_ver_var.set(f"Nuitka {ver}")
        except Exception:
            self._nuitka_ver_var.set("Nuitka: not found")

    # ── Command generation ─────────────────────────────────────────────
    def _collect_options(self) -> dict:
        opts = {}
        for key, var in self._option_vars.items():
            widget = self._ctrl_widgets.get(key)
            if isinstance(widget, StyledTextArea):
                opts[key] = widget.get_value()
            elif isinstance(widget, StyledEntry):
                opts[key] = widget.get_value()
            elif isinstance(var, tk.BooleanVar):
                opts[key] = var.get()
            else:
                opts[key] = var.get()
        return opts

    def _refresh_preview(self):
        script = self._script_var.get().strip() or "your_script.py"
        py = self._python_var.get().strip() or sys.executable
        opts = self._collect_options()
        cmd = build_nuitka_command(py, script, opts)
        self._cmd_preview.configure(state="normal")
        self._cmd_preview.delete("1.0", "end")
        self._cmd_preview.insert("1.0", " ".join(cmd))
        self._cmd_preview.configure(state="disabled")

    def _copy_command(self):
        self._refresh_preview()
        self.root.clipboard_clear()
        self.root.clipboard_append(self._cmd_preview.get("1.0", "end").strip())
        self._log.write("Command copied to clipboard.", "info")

    # ── Build logic ────────────────────────────────────────────────────
    def _clean_build_dir(self, script: str):
        """Delete <script_stem>.build/ and <script_stem>.dist/ if they exist."""
        stem = Path(script).stem
        parent = Path(script).parent
        for suffix in (".build", ".dist"):
            target = parent / (stem + suffix)
            if target.exists():
                self._log.write(f"🧹  Cleaning: {target}", "warning")
                try:
                    shutil.rmtree(target, ignore_errors=True)
                    self._log.write("   Done.", "info")
                except Exception as e:
                    self._log.write(f"   Could not remove: {e}", "warning")

    def _start_build(self):
        script = self._script_var.get().strip()
        if not script or not Path(script).exists():
            messagebox.showerror("Compylr", "Please select a valid Python script.")
            return
        if self._is_building:
            return

        self._refresh_preview()
        py = self._python_var.get().strip() or sys.executable
        opts = self._collect_options()
        cmd = build_nuitka_command(py, script, opts)

        self._is_building = True
        self._build_btn.configure(state="disabled")
        self._stop_btn.configure(state="normal")
        self._set_status("Building…", "warning")
        self._log.clear()
        self._log.write(f"$ {' '.join(cmd)}", "cmd")
        self._log.write("", "plain")

        if self._clean_build_var.get():
            self._clean_build_dir(script)

        thread = threading.Thread(
            target=self._run_build, args=(cmd, script), daemon=True)
        thread.start()

    def _run_build(self, cmd: list, script: str):
        try:
            self._build_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True, bufsize=1,
                encoding="utf-8", errors="replace",
                cwd=str(Path(script).parent),
            )
            seen_lines = []
            log_filter = _NuitkaLogFilter()

            for line in self._build_process.stdout:
                if not self._is_building:
                    break
                line = line.rstrip()
                seen_lines.append(line)
                result = log_filter.process(line)
                if result is None:
                    continue  # suppressed (absorbed into progress summary)
                display_text, kind = result
                self.root.after(0, lambda l=display_text, k=kind: self._log.write(l, k))

            # Flush any pending summary line
            flush = log_filter.flush()
            if flush:
                self.root.after(0, lambda l=flush[0], k=flush[1]: self._log.write(l, k))

            self._build_process.wait()
            rc = self._build_process.returncode
            if rc == 0:
                self.root.after(0, self._on_build_success)
            else:
                full_log = "\n".join(seen_lines)
                hints = self._find_hints(full_log)
                self.root.after(0, lambda h=hints: self._on_build_failed(rc, h))
        except Exception as exc:
            self.root.after(0, lambda: self._log.write(f"Error: {exc}", "error"))
            self.root.after(0, lambda: self._on_build_failed(-1, []))

    @staticmethod
    def _classify_line(line: str) -> str:
        """Classify a raw Nuitka output line into a log kind tag."""
        lo = line.lower()
        if "fatal error" in lo or "permissionerror" in lo: return "error"
        if "error" in lo and "nuitka" not in lo.split(":")[0].lower(): return "error"
        if "error" in lo:   return "error"
        if "warning" in lo: return "warning"
        first = lo.split(":")[0].strip()
        if "nuitka" in first or "scons" in first: return "info"
        return "plain"

    @staticmethod
    def _find_hints(log_text: str) -> list:
        hints = []
        for pattern, hint in _ERROR_HINTS.items():
            if pattern.lower() in log_text.lower():
                hints.append(hint)
        return hints

    def _on_build_success(self):
        if not self._is_building:
            return
        self._log.write("\n✅  Build completed successfully!", "success")
        self._set_status("Build succeeded ✓", "success")
        self._reset_build_state()

    def _on_build_failed(self, code: int, hints: list = None):
        if not self._is_building:
            return
        self._log.write(f"\n❌  Build failed (exit code {code}).", "error")
        if hints:
            self._log.write("", "plain")
            for h in hints:
                self._log.write(h, "warning")
        self._set_status(f"Build failed (code {code})", "error")
        self._reset_build_state()

    def _stop_build(self):
        if self._build_process and self._is_building:
            try:
                if sys.platform == "win32":
                    subprocess.run(["taskkill", "/F", "/T", "/PID", str(self._build_process.pid)],
                                   capture_output=True, timeout=3)
                else:
                    self._build_process.terminate()
            except Exception:
                try:
                    self._build_process.terminate()
                except Exception:
                    pass
            self._log.write("⏹  Build cancelled by user.", "warning")
            self._set_status("Cancelled", "warning")
            self._reset_build_state()

    def _reset_build_state(self):
        self._is_building = False
        self._build_btn.configure(state="normal")
        self._stop_btn.configure(state="disabled")

    def _set_status(self, msg: str, kind: str = "plain"):
        color_map = {
            "success": self._t["success"],
            "warning": self._t["warning"],
            "error":   self._t["error"],
            "plain":   self._t["text_muted"],
        }
        self._status_var.set(msg)
        self._status_dot.configure(text_color=color_map.get(kind, self._t["text_muted"]))

    # ── Theme switch ───────────────────────────────────────────────────
    def _toggle_theme(self):
        self._mode = "dark" if self._theme_var.get() else "light"
        self._t = get_theme(self._mode)
        self._option_vars.clear()
        self._ctrl_widgets.clear()
        for widget in self.root.winfo_children():
            widget.destroy()
        self._setup_root()
        self._build_ui()

    def run(self):
        self.root.mainloop()
