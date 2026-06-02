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

