# themes.py - Color themes for CyberScope

class Theme:
    def __init__(self, name, primary, secondary, background, text):
        self.name = name
        self.primary = primary
        self.secondary = secondary
        self.background = background
        self.text = text

# Predefined themes
THEMES = {
    "dark": Theme(
        name="Dark",
        primary="#00ff00",      # Green
        secondary="#ff00ff",    # Magenta
        background="#000000",   # Black
        text="#ffffff"          # White
    ),
    "light": Theme(
        name="Light",
        primary="#0000ff",
        secondary="#ff0000",
        background="#ffffff",
        text="#000000"
    ),
    "hacker": Theme(
        name="Hacker",
        primary="#00ff00",
        secondary="#33ff33",
        background="#0a0a0a",
        text="#00ff00"
    )
}

def get_theme(name="dark"):
    """Return theme object by name"""
    return THEMES.get(name, THEMES["dark"])
