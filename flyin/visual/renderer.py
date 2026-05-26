"""Phase 2: Pygame graph renderer."""

import pygame

from flyin.visual.colors_config import (
    BACKGROUND, WIDTH, HEIGHT, EDGE, TEXT
)
from flyin.visual.graph_layout import GraphLayout
from flyin.models.zone import Zone


class Renderer:
    """Renderer for displaying the graph using pygame."""

    def __init__(self, graph):
        """Initialize the pygame window and renderer state.

        Args:
            graph: Graph instance to draw.
        """

        self.graph = graph

        pygame.init()  # pylint: disable=no-member
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Fly-in Graph Viewer")

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 14)

        self.running = True

        self.layout = GraphLayout(width=WIDTH, height=HEIGHT)

    def get_color(self, zone: Zone) -> tuple[int, int, int]:
        """Return the color tuple for a given zone based on its category.

        Args:
            zone (_type_): zone from map

        Returns:
            _type_: _description_
        """
        return zone.color.value

    def draw_edges(self):
        """Draw every connection as a line between its endpoint zones."""

        for conn in self.graph.connections:
            a = conn.zone_a
            b = conn.zone_b

            x1, y1 = self.layout.to_screen(a)
            x2, y2 = self.layout.to_screen(b)

            pygame.draw.line(self.screen, EDGE, (x1, y1), (x2, y2), 2)
            pygame.display.flip()
            pygame.time.delay(300)

    def draw_nodes(self):
        """Draw each zone as a colored circle with its name label."""

        for zone in self.graph.zones.values():
            x, y = self.layout.to_screen(zone)
            pygame.draw.circle(self.screen, self.get_color(zone), (x, y), 15)

            text = self.font.render(zone.name, True, TEXT)
            self.screen.blit(text, (x + 10, y - 30))
            pygame.display.flip()
            pygame.time.delay(300)

    def run(self):
        """Run the main render loop until the window is closed.

        Args:
            layout: Layout helper used to map graph coordinates to screen
                positions.
        """

        # self.layout = layout

        while self.running:
            self.clock.tick(60)
            self.handle_events()

            self.screen.fill(BACKGROUND)

            self.draw_edges()
            self.draw_nodes()

            pygame.display.flip()

        pygame.quit()  # pylint: disable=no-member

    def handle_events(self):
        """Process pygame events and stop the loop when the window closes."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # pylint: disable=no-member
                self.running = False
