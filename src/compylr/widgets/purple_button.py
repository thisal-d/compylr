import customtkinter as ctk
from typing import Callable, Optional
import tkinter as tk

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

