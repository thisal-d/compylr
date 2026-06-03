<div align="center">
    <img src="https://raw.githubusercontent.com/Thisal-D/compylr/feature/ui-modernization/readme-assets/logo.png" alt="Compylr Logo" width="180"/>

# Compylr

_A modern, powerful, and intuitive GUI for transforming Python scripts into standalone executables using Nuitka._

[![PyPI version](https://badge.fury.io/py/compylr.svg)](https://pypi.org/project/compylr/)

![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue)
![CustomTkinter](https://img.shields.io/badge/UI-CustomTkinter-blueviolet)
![Nuitka](https://img.shields.io/badge/Compiler-Nuitka-brightgreen)
![License](https://img.shields.io/badge/License-MIT-gray)

[![PyPI Downloads](https://static.pepy.tech/personalized-badge/compylr?period=total&units=INTERNATIONAL_SYSTEM&left_color=blue&right_color=green&left_text=Downloads/All)](https://pepy.tech/projects/compylr)
[![PyPI Downloads](https://static.pepy.tech/personalized-badge/compylr?period=month&units=INTERNATIONAL_SYSTEM&left_color=blue&right_color=green&left_text=Downloads/Month)](https://pepy.tech/projects/compylr)
[![PyPI Downloads](https://static.pepy.tech/personalized-badge/compylr?period=week&units=INTERNATIONAL_SYSTEM&left_color=blue&right_color=green&left_text=Downloads/week)](https://pepy.tech/projects/compylr)

</div>

---

Stop memorizing Nuitka flags. **Compylr** gives you a clean, modern interface to configure, preview, and run your Python-to-EXE builds — visually. Just point, click, and ship.

## 🚀 Quick Start

**Install:**

```bash
pip install compylr
```

**Run:**

```bash
compylr
```

> **Requirements:** Python 3.8+ and a C compiler (MSVC or MinGW64 on Windows) for Nuitka to work.

---

## ✨ What You Get

| Feature                     | Description                                                                   |
| --------------------------- | ----------------------------------------------------------------------------- |
| 🎨 **Modern UI**            | Built with CustomTkinter — supports dark & light mode out of the box          |
| 🖱 **Visual Configuration** | Every Nuitka flag exposed as a clean GUI control — no CLI needed              |
| 👁 **Live Command Preview** | See the exact Nuitka command generated as you configure                       |
| 🖥 **Integrated Terminal**  | Color-coded build output with warnings, errors, and progress                  |
| 🧠 **Smart Hints**          | Automatically diagnoses common build failures and suggests fixes              |
| 🧹 **Clean Build**          | One-click wipe of stale `.build` / `.dist` directories before a fresh compile |

---

## 📸 Screenshots

### Compilation Mode & Output Settings

<img alt="Compilation Mode" src="https://raw.githubusercontent.com/Thisal-D/compylr/feature/ui-modernization/readme-assets/1a.png" />

### Windows Options & Version Metadata

<img alt="Windows Options" src="https://raw.githubusercontent.com/Thisal-D/compylr/feature/ui-modernization/readme-assets/2a.png" />

### Compiler & Build Options

<img alt="Compiler Options" src="https://raw.githubusercontent.com/Thisal-D/compylr/feature/ui-modernization/readme-assets/3a.png" />

### Python Flags & Package Inclusions

<img alt="Python Flags" src="https://raw.githubusercontent.com/Thisal-D/compylr/feature/ui-modernization/readme-assets/4a.png" />

### Plugins & Data Files

<img alt="Plugins" src="https://raw.githubusercontent.com/Thisal-D/compylr/feature/ui-modernization/readme-assets/5a.png" />

### Live Build Terminal

<img alt="Build Terminal" src="https://raw.githubusercontent.com/Thisal-D/compylr/feature/ui-modernization/readme-assets/6a.png" />

---

## 📁 Project Structure

```text
compylr/
├── src/
│   └── compylr/
│       ├── logo/              # Window icon and branding assets
│       │   ├── logo.ico
│       │   └── logo.png
│       ├── __init__.py
│       ├── main.py            # Entry point
│       ├── app.py             # Main application window
│       ├── widgets.py         # Reusable UI components
│       ├── theme.py           # Color palettes & font tokens
│       └── nuitka_options.py  # All Nuitka flags & section definitions
├── readme-assets/             # Screenshots and logo for README
├── requirements.txt
├── pyproject.toml
├── LICENSE
└── README.md
```

## 🛠 Built With

- **[Python](https://www.python.org/)** — Core language
- **[CustomTkinter](https://customtkinter.tomschimansky.com/)** — Modern UI framework
- **[Nuitka](https://nuitka.net/)** — Python-to-native compiler

## 🔮 Roadmap

- [ ] Save & load compilation profiles per project
- [ ] macOS / Linux build support (when Nuitka adds it)
- [ ] Integrated dependency analyzer

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!
Check the [issues page](https://github.com/Thisal-D/compylr/issues) to get started.

## 📝 License

[MIT](https://github.com/Thisal-D/compylr/blob/feature/ui-modernization/LICENSE) — do whatever you want with it.

---

<div align="center">
  Made with ❤️ by <a href="https://github.com/Thisal-D">Thisal</a>
</div>
