"""
Compylr - Main entry point
"""
import sys
import os

if __name__ == "__main__" and __package__ is None:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pyler.app import CompylrApp


def main():
    """Launch the Compylr application."""
    app = CompylrApp()
    app.run()


if __name__ == "__main__":
    main()
