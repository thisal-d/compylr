import customtkinter as ctk
from typing import Callable, Optional
import tkinter as tk

class StyledEntry(ctk.CTkEntry):
    """A styled text entry with focus highlight."""

    def __init__(self, parent, theme: dict, textvariable: tk.StringVar = None,
                 placeholder: str = "", **kwargs):
        self._t = theme
        var = textvariable or tk.StringVar()
        super().__init__(
            parent, 
            textvariable=var,
            placeholder_text=placeholder,
            font=(theme.get("font_family", "Segoe UI"), 12),
            fg_color=theme["bg_input"], 
            text_color=theme["text"],
            placeholder_text_color=theme["text_muted"],
            border_color=theme["border"],
            border_width=1,
            corner_radius=6,
            **kwargs
        )
        self.bind("<FocusIn>",  self._on_focus_in)
        self.bind("<FocusOut>", self._on_focus_out)

    def _on_focus_in(self, _=None):
        self.configure(border_color=self._t["accent"])

    def _on_focus_out(self, _=None):
        self.configure(border_color=self._t["border"])

    def get_value(self) -> str:
        return self.get()

    def set_value(self, val: str):
        self.delete(0, "end")
        self.insert(0, val)

