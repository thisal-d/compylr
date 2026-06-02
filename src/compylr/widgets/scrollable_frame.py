import customtkinter as ctk
from typing import Callable, Optional
import tkinter as tk

class ScrollableFrame(ctk.CTkScrollableFrame):
    """A vertically scrollable frame."""

    def __init__(self, parent, theme: dict, **kwargs):
        super().__init__(
            parent, 
            fg_color="transparent",
            scrollbar_button_color=theme["scrollbar"],
            scrollbar_button_hover_color=theme["scrollbar_hover"],
            **kwargs
        )
        self._t = theme
        
        # Keep `inner` attribute for compatibility with previous layout code
        self.inner = self
        
    def recolor(self, theme: dict):
        self._t = theme
        self.configure(
            scrollbar_button_color=theme["scrollbar"],
            scrollbar_button_hover_color=theme["scrollbar_hover"]
        )