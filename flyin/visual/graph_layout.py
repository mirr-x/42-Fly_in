"""Convert graph coordinates to screen positions."""

from flyin.models.zone import Zone


class GraphLayout:
    """Map graph coordinates to screen coordinates."""

    def __init__(
        self,
        width: int,
        height: int,
        origin_x: float = 0.5,
        origin_y: float = 0.5,
    ):
        self.width = width
        self.height = height

        self.scale = 100  # distance between nodes
        self.origin_x = float(origin_x)
        self.origin_y = float(origin_y)
        self.offset_x = int(width * self.origin_x)
        self.offset_y = int(height * self.origin_y)

    def set_scale(self, scale: int) -> None:
        """Set the coordinate scale used for screen conversion."""

        self.scale = scale

    def to_screen(self, zone: Zone) -> tuple[int, int]:
        """Convert zone coordinates to screen position."""

        x, y = zone.cord
        x = int(x * self.scale + self.offset_x)
        y = int(y * self.scale + self.offset_y)
        return x, y
