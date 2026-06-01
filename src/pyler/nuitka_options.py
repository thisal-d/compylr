"""
nuitka_options.py
Defines all available Nuitka options in a structured data format.
Used by the GUI to dynamically generate controls.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any


@dataclass
class NuitkaOption:
    """Represents a single Nuitka command-line option."""
    key: str               # internal key / CLI flag (without --)
    label: str             # Human-friendly label
    tooltip: str           # Explanation for the user
    type: str              # "bool", "text", "choice", "file", "dir", "multi_text"
    default: Any = None
    choices: Optional[List[str]] = None
    placeholder: str = ""
    flag: str = ""         # CLI flag override (use when key != flag)
    group: str = ""        # logical group name


# ─────────────────────────────────────────────
# All Nuitka options, organised by section/group
# ─────────────────────────────────────────────

NUITKA_SECTIONS = [
    # ── 1. Compilation Mode ──────────────────────────────────────────────
    {
        "title": "Compilation Mode",
        "icon": "⚡",
        "options": [
            NuitkaOption(
                key="mode",
                label="Build Mode",
                tooltip=(
                    "Controls the output type:\n"
                    "• accelerated - Run from source, faster (default)\n"
                    "• standalone  - Folder with all dependencies (portable)\n"
                    "• onefile     - Single .exe with everything embedded\n"
                    "• module      - Python extension module (.pyd/.so)\n"
                    "• app         - Like onefile but for app bundles"
                ),
                type="choice",
                default="standalone",
                choices=["accelerated", "standalone", "onefile", "module", "app"],
                flag="--mode",
                group="mode",
            ),
        ],
    },

    # ── 2. Output Settings ───────────────────────────────────────────────
    {
        "title": "Output Settings",
        "icon": "📁",
        "options": [
            NuitkaOption(
                key="output_dir",
                label="Output Directory",
                tooltip="Directory where the compiled output is placed.",
                type="dir",
                default="",
                placeholder="e.g. dist/",
                flag="--output-dir",
            ),
            NuitkaOption(
                key="output_filename",
                label="Output Filename",
                tooltip="Override the name of the resulting binary (without extension).",
                type="text",
                default="",
                placeholder="e.g. MyApp",
                flag="--output-filename",
            ),
        ],
    },

    # ── 3. Windows Options ───────────────────────────────────────────────
    {
        "title": "Windows Options",
        "icon": "🪟",
        "options": [
            NuitkaOption(
                key="windows_console_mode",
                label="Console Window Mode",
                tooltip=(
                    "Controls the Windows console window:\n"
                    "• force  - Always show console (default)\n"
                    "• disable - No console (GUI apps)\n"
                    "• attach - Use parent console if available\n"
                    "• hide   - Create but immediately hide console"
                ),
                type="choice",
                default="disable",
                choices=["force", "disable", "attach", "hide"],
                flag="--windows-console-mode",
            ),
            NuitkaOption(
                key="windows_icon_from_ico",
                label="Application Icon (.ico/.png)",
                tooltip="Path to an .ico or .png file to use as the executable icon.",
                type="file",
                default="",
                placeholder="Select icon file…",
                flag="--windows-icon-from-ico",
            ),
            NuitkaOption(
                key="windows_uac_admin",
                label="Request UAC Admin Rights",
                tooltip="Embed a UAC manifest to request administrator privileges at launch.",
                type="bool",
                default=False,
                flag="--windows-uac-admin",
            ),
            NuitkaOption(
                key="windows_uac_uiaccess",
                label="UAC UIAccess",
                tooltip="Request UAC UI access (for remote desktop elevation prompts).",
                type="bool",
                default=False,
                flag="--windows-uac-uiaccess",
            ),
            NuitkaOption(
                key="onefile_windows_splash_screen_image",
                label="Onefile Splash Screen (.png)",
                tooltip="PNG image shown while the onefile executable is extracting (onefile mode only).",
                type="file",
                default="",
                placeholder="Select splash PNG…",
                flag="--onefile-windows-splash-screen-image",
            ),
        ],
    },

    # ── 4. Version / Metadata ────────────────────────────────────────────
    {
        "title": "Version & Metadata",
        "icon": "🏷️",
        "options": [
            NuitkaOption(
                key="product_name",
                label="Product Name",
                tooltip="Product name embedded in the Windows version information.",
                type="text",
                default="",
                placeholder="e.g. My Application",
                flag="--product-name",
            ),
            NuitkaOption(
                key="product_version",
                label="Product Version",
                tooltip="Product version (up to 4 numbers, e.g. 1.0.0.0).",
                type="text",
                default="",
                placeholder="e.g. 1.0.0.0",
                flag="--product-version",
            ),
            NuitkaOption(
                key="file_version",
                label="File Version",
                tooltip="File version embedded in the Windows version information.",
                type="text",
                default="",
                placeholder="e.g. 1.0.0.0",
                flag="--file-version",
            ),
            NuitkaOption(
                key="file_description",
                label="File Description",
                tooltip="Human-readable description of the binary.",
                type="text",
                default="",
                placeholder="e.g. My Application Executable",
                flag="--file-description",
            ),
            NuitkaOption(
                key="copyright",
                label="Copyright",
                tooltip="Copyright notice embedded in version information.",
                type="text",
                default="",
                placeholder="e.g. © 2024 My Company",
                flag="--copyright",
            ),
            NuitkaOption(
                key="trademark",
                label="Trademark",
                tooltip="Trademark notice embedded in version information.",
                type="text",
                default="",
                placeholder="e.g. MyApp™",
                flag="--trademark",
            ),
        ],
    },

    # ── 5. Compiler / Build ──────────────────────────────────────────────
    {
        "title": "Compiler & Build",
        "icon": "🔧",
        "options": [
            NuitkaOption(
                key="compiler",
                label="C Compiler",
                tooltip=(
                    "Choose the C compiler backend:\n"
                    "• auto    - Let Nuitka decide (default)\n"
                    "• msvc    - Visual Studio (--msvc=latest)\n"
                    "• mingw64 - MinGW64 (not supported for Python 3.13+)\n"
                    "• clang   - Clang from Visual Studio\n"
                    "• zig     - Zig compiler (AMD64 only on Windows)"
                ),
                type="choice",
                default="auto",
                choices=["auto", "msvc", "mingw64", "clang", "zig"],
                flag="",  # handled specially in builder
            ),
            NuitkaOption(
                key="jobs",
                label="Parallel Compile Jobs",
                tooltip="Number of parallel C compilation jobs. Defaults to CPU count.",
                type="text",
                default="",
                placeholder="e.g. 4 (blank = auto)",
                flag="--jobs",
            ),
            NuitkaOption(
                key="lto",
                label="Link-Time Optimisation (LTO)",
                tooltip=(
                    "Enable Link-Time Optimisation:\n"
                    "• auto - Nuitka decides\n"
                    "• yes  - Force enable\n"
                    "• no   - Force disable"
                ),
                type="choice",
                default="auto",
                choices=["auto", "yes", "no"],
                flag="--lto",
            ),
            NuitkaOption(
                key="clang",
                label="Use Clang",
                tooltip="Use Clang compiler (from Visual Studio or MinGW64 download).",
                type="bool",
                default=False,
                flag="--clang",
            ),
            NuitkaOption(
                key="static_libpython",
                label="Static libpython",
                tooltip=(
                    "Use static linking of libpython:\n"
                    "• auto - Nuitka decides\n"
                    "• yes  - Force static\n"
                    "• no   - Force dynamic"
                ),
                type="choice",
                default="auto",
                choices=["auto", "yes", "no"],
                flag="--static-libpython",
            ),
        ],
    },

    # ── 6. Python Flags ──────────────────────────────────────────────────
    {
        "title": "Python Flags",
        "icon": "🐍",
        "options": [
            NuitkaOption(
                key="python_flag_no_site",
                label="No Site (-S)",
                tooltip="Prevent importing the 'site' module on startup (default for standalone).",
                type="bool",
                default=False,
                flag="--python-flag=no_site",
            ),
            NuitkaOption(
                key="python_flag_no_warnings",
                label="No Warnings",
                tooltip="Suppress runtime Python warnings.",
                type="bool",
                default=False,
                flag="--python-flag=no_warnings",
            ),
            NuitkaOption(
                key="python_flag_no_asserts",
                label="No Assertions (-O)",
                tooltip="Disable assert statements and set __debug__ = False.",
                type="bool",
                default=False,
                flag="--python-flag=no_asserts",
            ),
            NuitkaOption(
                key="python_flag_no_docstrings",
                label="No Docstrings",
                tooltip="Strip all docstrings to reduce binary size.",
                type="bool",
                default=False,
                flag="--python-flag=no_docstrings",
            ),
            NuitkaOption(
                key="python_flag_isolated",
                label="Isolated",
                tooltip="Ignore PYTHONPATH and user site-packages at runtime.",
                type="bool",
                default=False,
                flag="--python-flag=isolated",
            ),
            NuitkaOption(
                key="python_flag_unbuffered",
                label="Unbuffered (-u)",
                tooltip="Force unbuffered stdout/stderr output.",
                type="bool",
                default=False,
                flag="--python-flag=unbuffered",
            ),
            NuitkaOption(
                key="python_flag_static_hashes",
                label="Static Hashes",
                tooltip="Disable hash randomisation (deterministic behaviour).",
                type="bool",
                default=False,
                flag="--python-flag=static_hashes",
            ),
            NuitkaOption(
                key="python_flag_safe_path",
                label="Safe Path (-P)",
                tooltip="Prevent adding the CWD to the module search path.",
                type="bool",
                default=False,
                flag="--python-flag=safe_path",
            ),
            NuitkaOption(
                key="python_flag_dont_write_bytecode",
                label="Don't Write Bytecode (-B)",
                tooltip="Prevent writing .pyc cache files during execution.",
                type="bool",
                default=False,
                flag="--python-flag=dont_write_bytecode",
            ),
        ],
    },

    # ── 7. Inclusion ─────────────────────────────────────────────────────
    {
        "title": "Module & Package Inclusion",
        "icon": "📦",
        "options": [
            NuitkaOption(
                key="include_modules",
                label="Include Modules",
                tooltip="Comma-separated list of modules to force-include (e.g. os,sys,json).",
                type="multi_text",
                default="",
                placeholder="e.g. requests, PIL, numpy",
                flag="--include-module",
            ),
            NuitkaOption(
                key="include_packages",
                label="Include Packages",
                tooltip="Comma-separated list of packages to force-include entirely.",
                type="multi_text",
                default="",
                placeholder="e.g. requests, PIL",
                flag="--include-package",
            ),
            NuitkaOption(
                key="include_package_data",
                label="Include Package Data",
                tooltip=(
                    "Include data files from a package.\n"
                    "Format: package_name or package_name:*.txt\n"
                    "Comma-separated for multiple."
                ),
                type="multi_text",
                default="",
                placeholder="e.g. mypackage, mypackage:*.json",
                flag="--include-package-data",
            ),
        ],
    },

    # ── 8. Data Files ────────────────────────────────────────────────────
    {
        "title": "Data Files",
        "icon": "📄",
        "options": [
            NuitkaOption(
                key="include_data_files",
                label="Include Data Files (src=dest)",
                tooltip=(
                    "Include individual data files.\n"
                    "Format: /path/to/file.txt=folder/file.txt\n"
                    "One entry per line."
                ),
                type="multi_text",
                default="",
                placeholder="e.g. assets/icon.png=assets/icon.png",
                flag="--include-data-files",
            ),
            NuitkaOption(
                key="include_data_dir",
                label="Include Data Directory (src=dest)",
                tooltip=(
                    "Include a whole directory recursively.\n"
                    "Format: /path/to/dir=dest/dir\n"
                    "One entry per line."
                ),
                type="multi_text",
                default="",
                placeholder="e.g. assets/=assets/",
                flag="--include-data-dir",
            ),
            NuitkaOption(
                key="noinclude_data_files",
                label="Exclude Data Files (pattern)",
                tooltip="Glob patterns of data files to exclude. One per line.",
                type="multi_text",
                default="",
                placeholder="e.g. *.pyc",
                flag="--noinclude-data-files",
            ),
        ],
    },

    # ── 9. Plugins ───────────────────────────────────────────────────────
    {
        "title": "Plugins",
        "icon": "🔌",
        "options": [
            NuitkaOption(
                key="enable_plugin_tk_inter",
                label="Enable Tkinter Plugin",
                tooltip="Enable the tk-inter plugin for Tkinter-based GUIs.",
                type="bool",
                default=False,
                flag="--enable-plugin=tk-inter",
            ),
            NuitkaOption(
                key="enable_plugin_customtkinter",
                label="Enable CustomTkinter Plugin",
                tooltip="Enable tk-inter plugin required for CustomTkinter applications.",
                type="bool",
                default=False,
                flag="--enable-plugin=tk-inter",  # customtkinter uses tk-inter
            ),
            NuitkaOption(
                key="enable_plugin_numpy",
                label="Enable NumPy Plugin",
                tooltip="Enable the numpy plugin for NumPy compatibility.",
                type="bool",
                default=False,
                flag="--enable-plugin=numpy",
            ),
            NuitkaOption(
                key="enable_plugin_anti_bloat",
                label="Enable Anti-Bloat Plugin",
                tooltip="Remove known unnecessary imports to reduce binary size.",
                type="bool",
                default=False,
                flag="--enable-plugin=anti-bloat",
            ),
            NuitkaOption(
                key="enable_plugin_pyside6",
                label="Enable PySide6 Plugin",
                tooltip="Enable the PySide6 plugin for Qt6-based GUIs.",
                type="bool",
                default=False,
                flag="--enable-plugin=pyside6",
            ),
            NuitkaOption(
                key="enable_plugin_pyqt6",
                label="Enable PyQt6 Plugin",
                tooltip="Enable the PyQt6 plugin for Qt6-based GUIs.",
                type="bool",
                default=False,
                flag="--enable-plugin=pyqt6",
            ),
            NuitkaOption(
                key="enable_plugin_pyqt5",
                label="Enable PyQt5 Plugin",
                tooltip="Enable the PyQt5 plugin for Qt5-based GUIs.",
                type="bool",
                default=False,
                flag="--enable-plugin=pyqt5",
            ),
            NuitkaOption(
                key="enable_plugin_matplotlib",
                label="Enable Matplotlib Plugin",
                tooltip="Enable Matplotlib compatibility plugin.",
                type="bool",
                default=False,
                flag="--enable-plugin=matplotlib",
            ),
            NuitkaOption(
                key="enable_plugin_multiprocessing",
                label="Enable Multiprocessing Plugin",
                tooltip="Enable proper multiprocessing support in compiled executables.",
                type="bool",
                default=False,
                flag="--enable-plugin=multiprocessing",
            ),
            NuitkaOption(
                key="extra_plugins",
                label="Additional Plugins",
                tooltip="Extra plugin names to enable, comma-separated.",
                type="multi_text",
                default="",
                placeholder="e.g. dill-compat, eventlet",
                flag="--enable-plugin",
            ),
        ],
    },

    # ── 10. Onefile Options ──────────────────────────────────────────────
    {
        "title": "Onefile Options",
        "icon": "📦",
        "options": [
            NuitkaOption(
                key="onefile_tempdir_spec",
                label="Onefile Temp Dir Spec",
                tooltip=(
                    "Where to extract the onefile contents at runtime.\n"
                    "Supports tokens: {TEMP}, {CACHE_DIR}, {COMPANY}, {PRODUCT}, {VERSION}\n"
                    "Example: {CACHE_DIR}/{COMPANY}/{PRODUCT}/{VERSION}"
                ),
                type="text",
                default="",
                placeholder="e.g. {TEMP}/{PRODUCT}",
                flag="--onefile-tempdir-spec",
            ),
            NuitkaOption(
                key="onefile_child_grace_time",
                label="Child Grace Time (ms)",
                tooltip=(
                    "Milliseconds to wait for the child process to shut down before force-killing it.\n"
                    "Use 'infinity' to disable the timeout."
                ),
                type="text",
                default="",
                placeholder="e.g. 5000 or infinity",
                flag="--onefile-child-grace-time",
            ),
            NuitkaOption(
                key="include_onefile_external_data",
                label="External Data Patterns",
                tooltip=(
                    "Data file patterns to keep outside the onefile archive (alongside the .exe).\n"
                    "One pattern per line."
                ),
                type="multi_text",
                default="",
                placeholder="e.g. *.dat",
                flag="--include-onefile-external-data",
            ),
        ],
    },

    # ── 11. Debugging & Reports ──────────────────────────────────────────
    {
        "title": "Debugging & Reports",
        "icon": "🐛",
        "options": [
            NuitkaOption(
                key="report",
                label="Compilation Report File",
                tooltip=(
                    "Write a detailed XML compilation report to this file.\n"
                    "Useful for troubleshooting missing modules or data files."
                ),
                type="text",
                default="",
                placeholder="e.g. compilation-report.xml",
                flag="--report",
            ),
            NuitkaOption(
                key="show_modules",
                label="Show Included Modules",
                tooltip="Print the list of included modules after compilation.",
                type="bool",
                default=False,
                flag="--show-modules",
            ),
            NuitkaOption(
                key="show_progress",
                label="Show Progress",
                tooltip="Display progress information during compilation.",
                type="bool",
                default=True,
                flag="--show-progress",
            ),
            NuitkaOption(
                key="show_memory",
                label="Show Memory Usage",
                tooltip="Display memory usage statistics during compilation.",
                type="bool",
                default=False,
                flag="--show-memory",
            ),
            NuitkaOption(
                key="verbose",
                label="Verbose Output",
                tooltip="Print detailed information about what Nuitka is doing.",
                type="bool",
                default=False,
                flag="--verbose",
            ),
            NuitkaOption(
                key="assume_yes_for_downloads",
                label="Auto-download Dependencies",
                tooltip="Automatically approve downloading required tools (MinGW64, ccache, etc.).",
                type="bool",
                default=True,
                flag="--assume-yes-for-downloads",
            ),
        ],
    },
]


def _clean(value: str) -> str:
    """Return the value only if it is non-empty and not still a placeholder."""
    v = (value or "").strip()
    # Placeholders always start with "e.g." or are decorative hints
    if v.lower().startswith("e.g.") or v.lower().startswith("select "):
        return ""
    return v


def build_nuitka_command(python_exe: str, script_path: str, options: dict) -> List[str]:
    """
    Construct the Nuitka command-line from a dict of {option.key: value}.

    IMPORTANT: Nuitka uses a custom option parser that requires --flag=value
    format (with '=') for options that take arguments. Space-separated
    --flag value format causes FATAL parse errors for options like --mode.

    Returns a list of strings suitable for subprocess (no shell=True needed).
    """
    cmd = [python_exe, "-m", "nuitka"]

    # ── Mode ─────────────────────────────────────────────────────────────
    mode = options.get("mode", "standalone")
    if mode and mode != "accelerated":
        cmd.append(f"--mode={mode}")

    # ── Output settings ───────────────────────────────────────────────────
    output_dir = _clean(options.get("output_dir", ""))
    if output_dir:
        cmd.append(f"--output-dir={output_dir}")

    output_filename = _clean(options.get("output_filename", ""))
    if output_filename:
        cmd.append(f"--output-filename={output_filename}")

    # ── Windows options ───────────────────────────────────────────────────
    console_mode = options.get("windows_console_mode", "")
    if console_mode:
        cmd.append(f"--windows-console-mode={console_mode}")

    icon = _clean(options.get("windows_icon_from_ico", ""))
    if icon:
        cmd.append(f"--windows-icon-from-ico={icon}")

    if options.get("windows_uac_admin"):
        cmd.append("--windows-uac-admin")

    if options.get("windows_uac_uiaccess"):
        cmd.append("--windows-uac-uiaccess")

    splash = _clean(options.get("onefile_windows_splash_screen_image", ""))
    if splash and mode == "onefile":
        cmd.append(f"--onefile-windows-splash-screen-image={splash}")

    # ── Version / metadata ────────────────────────────────────────────────
    for key, flag in [
        ("product_name",     "--product-name"),
        ("product_version",  "--product-version"),
        ("file_version",     "--file-version"),
        ("file_description", "--file-description"),
        ("copyright",        "--copyright"),
        ("trademark",        "--trademark"),
    ]:
        val = _clean(options.get(key, ""))
        if val:
            cmd.append(f"{flag}={val}")

    # ── Compiler ──────────────────────────────────────────────────────────
    compiler = options.get("compiler", "auto")
    if compiler == "msvc":
        cmd.append("--msvc=latest")
    elif compiler == "mingw64":
        cmd.append("--mingw64")
    elif compiler == "clang":
        cmd.append("--clang")
    elif compiler == "zig":
        cmd.append("--zig")

    # --jobs must be a real integer; silently skip if non-numeric
    jobs_raw = _clean(options.get("jobs", ""))
    if jobs_raw:
        try:
            cmd.append(f"--jobs={int(jobs_raw)}")
        except ValueError:
            pass

    lto = options.get("lto", "auto")
    if lto and lto != "auto":
        cmd.append(f"--lto={lto}")

    static_libpython = options.get("static_libpython", "auto")
    if static_libpython and static_libpython != "auto":
        cmd.append(f"--static-libpython={static_libpython}")

    # ── Python flags ──────────────────────────────────────────────────────
    python_flag_map = {
        "python_flag_no_site":            "no_site",
        "python_flag_no_warnings":        "no_warnings",
        "python_flag_no_asserts":         "no_asserts",
        "python_flag_no_docstrings":      "no_docstrings",
        "python_flag_isolated":           "isolated",
        "python_flag_unbuffered":         "unbuffered",
        "python_flag_static_hashes":      "static_hashes",
        "python_flag_safe_path":          "safe_path",
        "python_flag_dont_write_bytecode":"dont_write_bytecode",
    }
    for key, flag_val in python_flag_map.items():
        if options.get(key):
            cmd.append(f"--python-flag={flag_val}")

    # ── Module / package inclusion ────────────────────────────────────────
    def _split(val: str) -> List[str]:
        return [v.strip() for v in val.replace("\n", ",").split(",") if v.strip()]

    for mod in _split(options.get("include_modules", "")):
        cmd.append(f"--include-module={mod}")

    for pkg in _split(options.get("include_packages", "")):
        cmd.append(f"--include-package={pkg}")

    for pkgdata in _split(options.get("include_package_data", "")):
        cmd.append(f"--include-package-data={pkgdata}")

    # ── Data files ────────────────────────────────────────────────────────
    for df in _split(options.get("include_data_files", "")):
        cmd.append(f"--include-data-files={df}")

    for dd in _split(options.get("include_data_dir", "")):
        cmd.append(f"--include-data-dir={dd}")

    for ndf in _split(options.get("noinclude_data_files", "")):
        cmd.append(f"--noinclude-data-files={ndf}")

    # ── Plugins ───────────────────────────────────────────────────────────
    plugin_map = {
        "enable_plugin_tk_inter":        "tk-inter",
        "enable_plugin_numpy":           "numpy",
        "enable_plugin_anti_bloat":      "anti-bloat",
        "enable_plugin_pyside6":         "pyside6",
        "enable_plugin_pyqt6":           "pyqt6",
        "enable_plugin_pyqt5":           "pyqt5",
        "enable_plugin_matplotlib":      "matplotlib",
        "enable_plugin_multiprocessing": "multiprocessing",
    }
    enabled_plugins: set = set()
    for key, plugin_name in plugin_map.items():
        if options.get(key):
            enabled_plugins.add(plugin_name)
    if options.get("enable_plugin_customtkinter"):
        enabled_plugins.add("tk-inter")

    for p in sorted(enabled_plugins):
        cmd.append(f"--enable-plugin={p}")

    for ep in _split(options.get("extra_plugins", "")):
        if ep not in enabled_plugins:
            cmd.append(f"--enable-plugin={ep}")

    # ── Onefile options ───────────────────────────────────────────────────
    if mode == "onefile":
        tmpdir = _clean(options.get("onefile_tempdir_spec", ""))
        if tmpdir:
            cmd.append(f"--onefile-tempdir-spec={tmpdir}")

        grace_raw = _clean(options.get("onefile_child_grace_time", ""))
        if grace_raw:
            cmd.append(f"--onefile-child-grace-time={grace_raw}")

        for ext in _split(options.get("include_onefile_external_data", "")):
            cmd.append(f"--include-onefile-external-data={ext}")

    # ── Debugging / reports ───────────────────────────────────────────────
    report = _clean(options.get("report", ""))
    if report:
        cmd.append(f"--report={report}")

    if options.get("show_modules"):
        cmd.append("--show-modules")
    if options.get("show_progress", True):
        cmd.append("--show-progress")
    if options.get("show_memory"):
        cmd.append("--show-memory")
    if options.get("verbose"):
        cmd.append("--verbose")
    if options.get("assume_yes_for_downloads", True):
        cmd.append("--assume-yes-for-downloads")

    # ── Script path (always last) ─────────────────────────────────────────
    cmd.append(script_path)

    return cmd

