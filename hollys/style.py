from typing import Optional


def get_color(palette: str, value: Optional[int] = None) -> str:
    if value:
        return f"var(--chakra-colors-{palette}-{value})"
    return f"var(--chakra-colors-{palette})"


class Color:
    navbar_bg = get_color("gray", 50)
    body_bg = get_color("white")
    border = get_color("gray", 200)
