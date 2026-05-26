"""Convert graph coordinates to screen positions."""


class GraphLayout:
    """Map graph coordinates to screen coordinates."""

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

        self.scale = 100  # distance between nodes
        self.offset_x = width // 2  # get mid of width so it clould be like x=0
        self.offset_y = height // 2  # get mid of heig so it clould be like y=0

    def set_scale(self, scale: int) -> None:
        """Set the coordinate scale used for screen conversion."""

        self.scale = scale

    def to_screen(self, zone) -> tuple[int, int]:
        """Convert zone coordinates to screen position."""

        x, y = zone.cord
        x = x * self.scale + self.offset_x
        y = y * self.scale + self.offset_y
        return x, y
