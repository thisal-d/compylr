import customtkinter as ctk
from typing import Callable, Optional
import tkinter as tk

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

