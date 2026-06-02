import customtkinter as ctk
from typing import Callable, Optional
import tkinter as tk

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

