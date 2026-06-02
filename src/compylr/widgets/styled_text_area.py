import customtkinter as ctk
from typing import Callable, Optional
import tkinter as tk

class StyledTextArea(ctk.CTkTextbox):
    """A multi-line text widget with styling."""

    def __init__(self, parent, theme: dict, height: int = 60,
                 placeholder: str = "", **kwargs):
        self._t = theme
        self._placeholder = placeholder
        self._has_placeholder = False
        super().__init__(
            parent, 
            height=height,
            font=(theme.get("font_family", "Segoe UI"), 12),
            fg_color=theme["bg_input"], 
            text_color=theme["text"],
            border_color=theme["border"],
            border_width=1,
            corner_radius=6,
            wrap="word",
            **kwargs
        )

        if placeholder:
            self._set_placeholder()
        self.bind("<FocusIn>",  self._on_focus_in)
        self.bind("<FocusOut>", self._on_focus_out)

    def _set_placeholder(self):
        self._has_placeholder = True
        self.configure(text_color=self._t["text_muted"])
        self.delete("1.0", "end")
        self.insert("1.0", self._placeholder)

    def _on_focus_in(self, _=None):
        self.configure(border_color=self._t["accent"])
        if self._has_placeholder:
            self.delete("1.0", "end")
            self.configure(text_color=self._t["text"])
            self._has_placeholder = False

    def _on_focus_out(self, _=None):
        self.configure(border_color=self._t["border"])
        if not self.get("1.0", "end").strip() and self._placeholder:
            self._set_placeholder()

    def get_value(self) -> str:
        if self._has_placeholder:
            return ""
        return self.get("1.0", "end").strip()

    def set_value(self, val: str):
        self._has_placeholder = False
        self.delete("1.0", "end")
        self.insert("1.0", val)
        self.configure(text_color=self._t["text"])

