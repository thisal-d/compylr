import customtkinter as ctk
from typing import Callable, Optional
import tkinter as tk

class OptionRow(ctk.CTkFrame):
    """One row: label on the left, control on the right + tooltip."""

    def __init__(self, parent, label: str, tooltip: str, theme: dict, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        self._t = theme
        self._tooltip_text = tooltip
        self._label_str = label
        
        self.grid_columnconfigure(0, minsize=280, weight=0)
        self.grid_columnconfigure(1, weight=1)
        
        # Left container for label and help text
        self._left_frame = ctk.CTkFrame(self, fg_color="transparent")
        self._left_frame.grid(row=0, column=0, sticky="nw", padx=(0, 20), pady=6)
        
        self._lbl = ctk.CTkLabel(
            self._left_frame,
            text=label,
            font=(theme.get("font_family", "Segoe UI"), 13, "bold"),
            text_color=theme["text"],
            anchor="w",
            justify="left"
        )
        self._lbl.pack(anchor="w", fill="x")
        
        if tooltip:
            self._info = ctk.CTkLabel(
                self._left_frame,
                text=tooltip,
                font=(theme.get("font_family", "Segoe UI"), 11),
                text_color=theme["text_muted"],
                anchor="w",
                justify="left",
                wraplength=260
            )
            self._info.pack(anchor="w", fill="x", pady=(2, 0))
            
        self._ctrl_frame = ctk.CTkFrame(self, fg_color="transparent")
        self._ctrl_frame.grid(row=0, column=1, sticky="ew", pady=6)

    @property
    def ctrl(self) -> ctk.CTkFrame:
        return self._ctrl_frame

