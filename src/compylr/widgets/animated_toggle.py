import customtkinter as ctk
from typing import Callable, Optional
import tkinter as tk

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

