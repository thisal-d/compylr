"""
Compylr - theme.py
Centralised colour / font tokens for Dark-Purple and Light themes.
"""

FONTS = {
    "family": "Segoe UI",
    "size_xs":   10,
    "size_sm":   11,
    "size_md":   12,
    "size_lg":   14,
    "size_xl":   18,
    "size_title":24,
}

DARK = {
    # Base surfaces
    "bg":           "#0E0E14",
    "bg_card":      "#16161F",
    "bg_sidebar":   "#111119",
    "bg_input":     "#1C1C2A",
    "bg_input2":    "#22222F",
    "bg_hover":     "#252535",
    "bg_active":    "#2A2A3E",
    "bg_header":    "#0B0B10",

    # Accent — purple spectrum
    "accent":       "#7C3AED",
    "accent_light": "#9D5EFF",
    "accent_dark":  "#5B21B6",
    "accent_glow":  "#7C3AED40",
    "accent2":      "#A855F7",

    # Status colours
    "success":      "#22C55E",
    "warning":      "#F59E0B",
    "error":        "#EF4444",
    "info":         "#38BDF8",

    # Text
    "text":         "#E8E8F0",
    "text_muted":   "#888899",
    "text_dim":     "#555566",
    "text_accent":  "#C084FC",

    # Borders
    "border":       "#2A2A3C",
    "border_focus": "#7C3AED",
    "border_card":  "#252535",

    # Terminal / log
    "terminal_bg":  "#0A0A0F",
    "terminal_fg":  "#C8C8D8",
    "terminal_green":"#22C55E",
    "terminal_yellow":"#F59E0B",
    "terminal_red": "#EF4444",
    "terminal_blue":"#60A5FA",
    "terminal_purple":"#C084FC",

    # Scrollbar
    "scrollbar":    "#2A2A3C",
    "scrollbar_hover":"#7C3AED",
}

LIGHT = {
    "bg":           "#F5F5FA",
    "bg_card":      "#FFFFFF",
    "bg_sidebar":   "#ECECF6",
    "bg_input":     "#F0F0F8",
    "bg_input2":    "#E8E8F4",
    "bg_hover":     "#E4E4F0",
    "bg_active":    "#DDD8FF",
    "bg_header":    "#EEEEF8",

    "accent":       "#7C3AED",
    "accent_light": "#9D5EFF",
    "accent_dark":  "#5B21B6",
    "accent_glow":  "#7C3AED25",
    "accent2":      "#A855F7",

    "success":      "#16A34A",
    "warning":      "#D97706",
    "error":        "#DC2626",
    "info":         "#0284C7",

    "text":         "#1A1A2E",
    "text_muted":   "#6B6B80",
    "text_dim":     "#9999AA",
    "text_accent":  "#7C3AED",

    "border":       "#D5D5E8",
    "border_focus": "#7C3AED",
    "border_card":  "#E0E0F0",

    "terminal_bg":  "#F8F8FD",
    "terminal_fg":  "#1E1E2F",
    "terminal_green":"#16A34A",
    "terminal_yellow":"#D97706",
    "terminal_red": "#DC2626",
    "terminal_blue":"#1D4ED8",
    "terminal_purple":"#6D28D9",

    "scrollbar":    "#C5C5DC",
    "scrollbar_hover":"#7C3AED",
}


def get_theme(mode: str) -> dict:
    return DARK if mode == "dark" else LIGHT
