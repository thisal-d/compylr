from dataclasses import dataclass
from typing import List, Optional, Any

@dataclass
class NuitkaOption:
    """Represents a single Nuitka command-line option."""
    key: str               # internal key / CLI flag (without --)
    label: str             # Human-friendly label
    tooltip: str           # Explanation for the user
    type: str              # "bool", "text", "choice", "file", "dir", "multi_text"
    default: Any = None
    choices: Optional[List[str]] = None
    placeholder: str = ""
    flag: str = ""         # CLI flag override (use when key != flag)
    group: str = ""        # logical group name
