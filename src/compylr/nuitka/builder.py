from typing import List

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

