"""Centralized color definitions for visualization."""

BACKGROUND = (20, 20, 25)

EDGE = (160, 160, 160)

TEXT = (240, 240, 240)

DRONE_STATE_COLORS = {
    "MOVING": (0, 120, 255),
    "WAITING": (255, 210, 0),
    "DELIVERED": (0, 200, 80),
    "BLOCKED": (220, 50, 50),
    "IN_TRANSIT": (160, 80, 255),
}

DRONE_STATE_FALLBACK = (220, 50, 50)

WIDTH, HEIGHT = (1200, 800)
