<div align="center">
  <img src="https://github.com/user-attachments/assets/62305c41-61ca-4d2f-a0c1-ee6cb79c4b73" alt="Compylr Logo" width="180"/>

# Compylr

_A modern, powerful, and intuitive GUI for transforming Python scripts into standalone executables using Nuitka._

![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue)
![CustomTkinter](https://img.shields.io/badge/UI-CustomTkinter-blueviolet)
![Nuitka](https://img.shields.io/badge/Compiler-Nuitka-brightgreen)
![License](https://img.shields.io/badge/License-MIT-gray)

</div>

## 📌 Overview

Compylr takes the complexity out of compiling Python applications. It provides a sleek, modern user interface built with CustomTkinter that lets you configure Nuitka's powerful compilation options visually. No more memorizing long command-line flags — just point, click, and build.

## ✨ Features

- **Modern & Responsive UI**: Fully redesigned using CustomTkinter with dark and light mode support.
- **Visual Configuration**: Configure build modes, output settings, windows options, metadata, and data files through an intuitive sidebar menu.
- **Live Command Preview**: See the exact Nuitka command being generated in real-time.
- **Integrated Terminal**: View color-coded compilation progress, warnings, and errors directly inside the app.
- **Smart Troubleshooting**: Automatically suggests fixes for common compilation errors (e.g., corrupted caches, missing modules).
- **Clean Build Support**: One-click option to safely clean old `.build` and `.dist` directories before recompiling.

## 📸 Screenshots

### 1. Compilation Mode & Output Settings

<img width="1479" height="891" alt="1a" src="https://github.com/user-attachments/assets/3b2a39ad-a6c8-4a04-8dad-a588cb75c8f4" />

### 2. Windows Options & Version Metadata

<img width="1479" height="891" alt="2a" src="https://github.com/user-attachments/assets/1a847bd6-daa4-4067-a658-4e019519ead5" />

### 3. Compiler & Build Options

<img width="1479" height="891" alt="3a" src="https://github.com/user-attachments/assets/21abb860-87bd-43bf-8a6e-4d7f281bfee0" />

### 4. Python Flags & Package Inclusions

<img width="1479" height="891" alt="4a" src="https://github.com/user-attachments/assets/3dc8b493-14f8-479f-aa4a-55c511a3a60a" />

### 5. Plugins & Data Files

<img width="1479" height="891" alt="5a" src="https://github.com/user-attachments/assets/002df3ec-e407-4733-87b3-ff4e40af8861" />

### 6. Compiler Terminal & Live Build

<img width="1479" height="891" alt="6a" src="https://github.com/user-attachments/assets/ed3aa189-c9c3-497f-bf7b-e7f19d3c45a3" />

## 🚀 Installation

Install Compylr directly using `pip`:

```bash
pip install compylr
```

### Requirements

- Python 3.8+
- C Compiler (MinGW64 or MSVC on Windows) — required by Nuitka for compilation.

## 💻 Usage

Launch the application directly from your terminal:

```bash
compylr
```

1. **Select Script**: Browse for the `.py` file you want to compile.
2. **Select Interpreter**: (Optional) Pick a specific Python executable to run Nuitka.
3. **Configure Options**: Navigate through the sidebar sections (Compilation Mode, Windows Options, Plugins, etc.) to set your desired flags.
4. **Build**: Go to the **Build** section and click `🚀 Build Executable`.

## 📁 Project Structure

```text
compylr/
├── src/
│   └── compylr/
│       ├── logo/              # Window icon and branding logo assets
│       │   ├── logo.ico
│       │   └── logo.png
│       ├── __init__.py
│       ├── main.py            # Application entry point
│       ├── app.py             # Main CustomTkinter application and layout
│       ├── widgets.py         # Custom reusable UI components
│       ├── theme.py           # Color palettes and font definitions
│       └── nuitka_options.py  # Definition of all Nuitka flags and groups
├── readme-assets/             # Screenshots and README header logo assets
├── requirements.txt           # Python dependencies
├── pyproject.toml             # Pyproject settings metadata
├── LICENSE                    # MIT License file
└── README.md                  # This file
```

## 🛠 Technologies Used

- **[Python](https://www.python.org/)** - Core programming language
- **[CustomTkinter](https://customtkinter.tomschimansky.com/)** - Modern UI framework
- **[Nuitka](https://nuitka.net/)** - The Python compiler

## 🔮 Future Improvements

- Profile management (save and load compilation profiles for different projects).
- Direct compilation to macOS and Linux formats (when supported on host).
- Integrated dependency analyzer.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!
Feel free to check the [issues page](https://github.com/Thisal-D/compylr/issues).

## 📝 License

This project is [MIT](LICENSE) licensed.

---

<div align="center">
  Made with ❤️ by <a href="https://github.com/Thisal-D">Thisal</a>
</div>
