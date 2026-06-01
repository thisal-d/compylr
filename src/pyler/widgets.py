"""
Compylr - widgets.py
Reusable CustomTkinter widgets for the Compylr UI.
"""

import customtkinter as ctk
from typing import Callable, Optional
import tkinter as tk

class SectionCard(ctk.CTkFrame):
    """A card container with a coloured header label."""

    def __init__(self, parent, title: str, icon: str, theme: dict, **kwargs):
        super().__init__(parent, fg_color=theme["bg_card"], border_color=theme["border_card"], border_width=1, corner_radius=8, **kwargs)
        self._t = theme
        self._title = title
        self._icon = icon
        self._build()

    def _build(self):
        t = self._t
        hdr = ctk.CTkFrame(self, fg_color=t["bg_active"], corner_radius=0)
        hdr.pack(fill="x", pady=(0, 0))
        
        lbl = ctk.CTkLabel(
            hdr,
            text=f"  {self._icon}  {self._title}",
            font=(t.get("font_family", "Segoe UI"), 14, "bold"),
            text_color=t["text_accent"],
            anchor="w"
        )
        lbl.pack(side="left", padx=10, pady=8)
        
        self.body = ctk.CTkFrame(self, fg_color="transparent")
        self.body.pack(fill="both", expand=True, padx=12, pady=10)

    def recolor(self, theme: dict):
        self._t = theme
        self.configure(fg_color=theme["bg_card"], border_color=theme["border_card"])


class OptionRow(ctk.CTkFrame):
    """One row: label on the left, control on the right + tooltip."""

    def __init__(self, parent, label: str, tooltip: str, theme: dict, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        self._t = theme
        self._tooltip_text = tooltip
        self._label_str = label
        
        self.grid_columnconfigure(0, minsize=280, weight=0)
        self.grid_columnconfigure(1, weight=1)
        
        # Left container for label and help text
        self._left_frame = ctk.CTkFrame(self, fg_color="transparent")
        self._left_frame.grid(row=0, column=0, sticky="nw", padx=(0, 20), pady=6)
        
        self._lbl = ctk.CTkLabel(
            self._left_frame,
            text=label,
            font=(theme.get("font_family", "Segoe UI"), 13, "bold"),
            text_color=theme["text"],
            anchor="w",
            justify="left"
        )
        self._lbl.pack(anchor="w", fill="x")
        
        if tooltip:
            self._info = ctk.CTkLabel(
                self._left_frame,
                text=tooltip,
                font=(theme.get("font_family", "Segoe UI"), 11),
                text_color=theme["text_muted"],
                anchor="w",
                justify="left",
                wraplength=260
            )
            self._info.pack(anchor="w", fill="x", pady=(2, 0))
            
        self._ctrl_frame = ctk.CTkFrame(self, fg_color="transparent")
        self._ctrl_frame.grid(row=0, column=1, sticky="ew", pady=6)

    @property
    def ctrl(self) -> ctk.CTkFrame:
        return self._ctrl_frame


class AnimatedToggle(ctk.CTkSwitch):
    """
    A polished iOS-style toggle switch using CTkSwitch.
    """
    def __init__(self, parent, variable: tk.BooleanVar, theme: dict,
                 command: Optional[Callable] = None, **kwargs):
        self._t = theme
        is_light = (theme.get("bg") == "#F5F5FA")
        track_color = "#B0B0C8" if is_light else theme["bg_input2"]
        btn_color = "#E2E8F0" if is_light else "#94A3B8"
        btn_hover = "#CBD5E1" if is_light else "#CBD5E1"
        
        super().__init__(
            parent,
            text="",
            variable=variable,
            command=command,
            progress_color=theme["accent"],
            button_color=btn_color,
            button_hover_color=btn_hover,
            fg_color=track_color,
            width=50,
            height=24,
            switch_width=40,
            switch_height=20,
            **kwargs
        )

    def recolor(self, theme: dict):
        self._t = theme
        is_light = (theme.get("bg") == "#F5F5FA")
        track_color = "#B0B0C8" if is_light else theme["bg_input2"]
        btn_color = "#E2E8F0" if is_light else "#94A3B8"
        btn_hover = "#CBD5E1" if is_light else "#CBD5E1"
        self.configure(
            progress_color=theme["accent"], 
            fg_color=track_color,
            button_color=btn_color,
            button_hover_color=btn_hover
        )


class StyledEntry(ctk.CTkEntry):
    """A styled text entry with focus highlight."""

    def __init__(self, parent, theme: dict, textvariable: tk.StringVar = None,
                 placeholder: str = "", **kwargs):
        self._t = theme
        var = textvariable or tk.StringVar()
        super().__init__(
            parent, 
            textvariable=var,
            placeholder_text=placeholder,
            font=(theme.get("font_family", "Segoe UI"), 12),
            fg_color=theme["bg_input"], 
            text_color=theme["text"],
            placeholder_text_color=theme["text_muted"],
            border_color=theme["border"],
            border_width=1,
            corner_radius=6,
            **kwargs
        )
        self.bind("<FocusIn>",  self._on_focus_in)
        self.bind("<FocusOut>", self._on_focus_out)

    def _on_focus_in(self, _=None):
        self.configure(border_color=self._t["accent"])

    def _on_focus_out(self, _=None):
        self.configure(border_color=self._t["border"])

    def get_value(self) -> str:
        return self.get()

    def set_value(self, val: str):
        self.delete(0, "end")
        self.insert(0, val)


class StyledDropdown(ctk.CTkOptionMenu):
    """A minimal themed OptionMenu."""

    def __init__(self, parent, variable: tk.StringVar, choices: list,
                 theme: dict, **kwargs):
        self._t = theme
        
        # Ensure choices isn't empty
        if not choices:
            choices = [""]
            
        super().__init__(
            parent, 
            variable=variable, 
            values=choices,
            font=(theme.get("font_family", "Segoe UI"), 12),
            dropdown_font=(theme.get("font_family", "Segoe UI"), 12),
            fg_color=theme["bg_input"],
            text_color=theme["text"],
            button_color=theme["bg_input"],
            button_hover_color=theme["bg_hover"],
            dropdown_fg_color=theme["bg_card"],
            dropdown_text_color=theme["text"],
            dropdown_hover_color=theme["accent"],
            corner_radius=6,
            **kwargs
        )


class StyledTextArea(ctk.CTkTextbox):
    """A multi-line text widget with styling."""

    def __init__(self, parent, theme: dict, height: int = 60,
                 placeholder: str = "", **kwargs):
        self._t = theme
        self._placeholder = placeholder
        self._has_placeholder = False
        super().__init__(
            parent, 
            height=height,
            font=(theme.get("font_family", "Segoe UI"), 12),
            fg_color=theme["bg_input"], 
            text_color=theme["text"],
            border_color=theme["border"],
            border_width=1,
            corner_radius=6,
            wrap="word",
            **kwargs
        )

        if placeholder:
            self._set_placeholder()
        self.bind("<FocusIn>",  self._on_focus_in)
        self.bind("<FocusOut>", self._on_focus_out)

    def _set_placeholder(self):
        self._has_placeholder = True
        self.configure(text_color=self._t["text_muted"])
        self.delete("1.0", "end")
        self.insert("1.0", self._placeholder)

    def _on_focus_in(self, _=None):
        self.configure(border_color=self._t["accent"])
        if self._has_placeholder:
            self.delete("1.0", "end")
            self.configure(text_color=self._t["text"])
            self._has_placeholder = False

    def _on_focus_out(self, _=None):
        self.configure(border_color=self._t["border"])
        if not self.get("1.0", "end").strip() and self._placeholder:
            self._set_placeholder()

    def get_value(self) -> str:
        if self._has_placeholder:
            return ""
        return self.get("1.0", "end").strip()

    def set_value(self, val: str):
        self._has_placeholder = False
        self.delete("1.0", "end")
        self.insert("1.0", val)
        self.configure(text_color=self._t["text"])


class PurpleButton(ctk.CTkButton):
    """A clickable label styled as a modern button."""

    def __init__(self, parent, text: str, theme: dict,
                 command: Optional[Callable] = None,
                 style: str = "primary",   # primary | secondary | danger | ghost
                 **kwargs):
        self._t = theme
        self._style = style
        colors = self._resolve_colors(theme, style)
        
        super().__init__(
            parent, 
            text=text,
            command=command,
            font=(theme.get("font_family", "Segoe UI"), 12, "bold"),
            fg_color=colors["bg"] if style != "ghost" else "transparent",
            text_color=colors["fg"],
            hover_color=colors["hover"],
            corner_radius=6,
            height=32,
            border_width=1 if style in ("secondary", "ghost") else 0,
            border_color=theme["border"] if style in ("secondary", "ghost") else colors["bg"],
            **kwargs
        )

    @staticmethod
    def _resolve_colors(t, style):
        if style == "primary":
            return {"bg": t["accent"], "fg": "#FFFFFF", "hover": t["accent_light"]}
        if style == "secondary":
            return {"bg": t["bg_input"], "fg": t["text"], "hover": t["bg_hover"]}
        if style == "danger":
            return {"bg": t["error"], "fg": "#FFFFFF", "hover": "#FF6B6B"}
        if style == "ghost":
            return {"bg": t["bg_card"], "fg": t["text_muted"], "hover": t["bg_hover"]}
        return {"bg": t["accent"], "fg": "#FFFFFF", "hover": t["accent_light"]}

    def recolor(self, theme: dict):
        self._t = theme
        colors = self._resolve_colors(theme, self._style)
        self.configure(
            fg_color=colors["bg"] if self._style != "ghost" else "transparent", 
            text_color=colors["fg"],
            hover_color=colors["hover"],
            border_color=theme["border"] if self._style in ("secondary", "ghost") else colors["bg"]
        )


class LogTerminal(ctk.CTkTextbox):
    """Coloured terminal-like output widget."""

    TAG_COLORS = {
        "info":    "terminal_blue",
        "success": "terminal_green",
        "warning": "terminal_yellow",
        "error":   "terminal_red",
        "cmd":     "terminal_purple",
        "plain":   "terminal_fg",
    }

    def __init__(self, parent, theme: dict, **kwargs):
        super().__init__(
            parent, 
            font=("Consolas", 12),
            fg_color=theme["terminal_bg"],
            text_color=theme["terminal_fg"],
            border_width=0,
            corner_radius=6,
            wrap="word",
            state="disabled",
            **kwargs
        )
        self._t = theme
        self._setup_tags()

    def _setup_tags(self):
        t = self._t
        for tag, color_key in self.TAG_COLORS.items():
            self.tag_config(tag, foreground=t[color_key])

    def write(self, text: str, kind: str = "plain"):
        self.configure(state="normal")
        tag = kind if kind in self.TAG_COLORS else "plain"
        self.insert("end", text + "\n", tag)
        self.see("end")
        self.configure(state="disabled")

    def clear(self):
        self.configure(state="normal")
        self.delete("1.0", "end")
        self.configure(state="disabled")

    def recolor(self, theme: dict):
        self._t = theme
        self.configure(fg_color=theme["terminal_bg"], text_color=theme["terminal_fg"])
        self._setup_tags()


class ScrollableFrame(ctk.CTkScrollableFrame):
    """A vertically scrollable frame."""

    def __init__(self, parent, theme: dict, **kwargs):
        super().__init__(
            parent, 
            fg_color="transparent",
            scrollbar_button_color=theme["scrollbar"],
            scrollbar_button_hover_color=theme["scrollbar_hover"],
            **kwargs
        )
        self._t = theme
        
        # Keep `inner` attribute for compatibility with previous layout code
        self.inner = self
        
    def recolor(self, theme: dict):
        self._t = theme
        self.configure(
            scrollbar_button_color=theme["scrollbar"],
            scrollbar_button_hover_color=theme["scrollbar_hover"]
        )
