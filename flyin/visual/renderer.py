"""Phase 2: Pygame graph renderer."""

import pygame
from typing import Dict, Tuple, List, Optional

from flyin.models.drone import Drone
from flyin.graph.graph import Graph

from flyin.visual.colors_config import (
    BACKGROUND, EDGE, TEXT,
    DRONE_STATE_COLORS, DRONE_STATE_FALLBACK
)
from flyin.visual.graph_layout import GraphLayout
from flyin.visual._renderer_helpers import get_drone_positions
from flyin.models.zone import Zone
from flyin._types import RoleZone


class Renderer:
    """Renderer for displaying the graph using pygame.

    Responsibilities:
    - draw graph (edges, zones)
    - draw drones using helper-provided positions
    - animate transitions between turns
    - handle simple keyboard controls (pause/speed)
    """

    def __init__(self, graph: Graph):
        self.graph = graph
        self.pygame = pygame
        self.pygame.init()  # pylint: disable=no-member
        # create a fullscreen window and use the actual display size
        info = self.pygame.display.Info()
        screen_w, screen_h = info.current_w, info.current_h
        flags = getattr(self.pygame, "FULLSCREEN", 0)
        self.screen = self.pygame.display.set_mode((screen_w, screen_h), flags)
        self.width = screen_w
        self.height = screen_h
        self.pygame.display.set_caption("Fly-in Graph Viewer")
        self.clock = pygame.time.Clock()
        self.animation_clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 14)
        self.small_font = pygame.font.SysFont("Arial", 10)

        # interaction + pacing
        self.running = True
        self.paused = False
        self.delay_ms = 500
        self.transition_steps = 12
        self.delay_step = 100
        self.min_delay_ms = 0
        self.max_delay_ms = 3000
        self.hold_ms = 250

        # shift origin left so large maps are more visible (10% from left)
        self.layout = GraphLayout(
            width=self.width, height=self.height, origin_x=0.03
        )

        # visual sizes
        self.zone_radius = 15
        self.drone_radius = 6
        self.offset_radius = 12.0

    def get_color(self, zone: Zone) -> Tuple[int, int, int]:
        """Return RGB color for a zone."""
        return zone.color.value

    def get_drone_color(self, drone: Drone) -> Tuple[int, int, int]:
        """Return RGB color for a drone based on its state."""
        state = getattr(drone.state, "name", str(drone.state)).upper()
        return DRONE_STATE_COLORS.get(state, DRONE_STATE_FALLBACK)

    def get_zone_occupancy(self, zone: Zone, drones: List[Drone]) -> int:
        """Count drones currently in the given zone."""
        return sum(1 for drone in drones if drone.current_zone == zone)

    def draw_edges(self) -> None:
        """Draw all graph connections (edges)."""
        for conn in self.graph.connections:
            a = conn.zone_a
            b = conn.zone_b
            x1, y1 = self.layout.to_screen(a)
            x2, y2 = self.layout.to_screen(b)
            self.pygame.draw.line(self.screen, EDGE, (x1, y1), (x2, y2), 2)

    def draw_nodes(self, drones: List[Drone]) -> None:
        """Draw all zones (nodes) and their capacity text."""
        for zone in self.graph.zones.values():
            x, y = self.layout.to_screen(zone)
            self.pygame.draw.circle(
                self.screen, self.get_color(zone), (x, y), self.zone_radius
            )

            if zone.role not in (RoleZone.STARTING, RoleZone.ENDING):
                occupancy = self.get_zone_occupancy(zone, drones)
                capacity_text = self.font.render(
                    f"{occupancy}/{zone.max_drones}", True, TEXT
                )
                capacity_rect = capacity_text.get_rect(
                    center=(x, y + self.zone_radius + 8)
                )
                self.screen.blit(capacity_text, capacity_rect)

            text = self.font.render(zone.name, True, TEXT)
            text_pos = (
                x + self.zone_radius + 6,
                y - self.zone_radius - 8,
            )
            self.screen.blit(text, text_pos)

    def draw_drones(
        self,
        drones: List[Drone],
        positions: Optional[Dict[str, Tuple[float, float]]] = None,
    ) -> None:
        """Draw all drones at the provided positions."""
        if positions is None:
            positions = get_drone_positions(self.layout, drones)

        for drone in drones:
            if drone.id not in positions:
                continue
            x, y = positions[drone.id]
            color = self.get_drone_color(drone)
            pos = (x, y)
            self.pygame.draw.circle(self.screen, color, pos, self.drone_radius)
            text = self.small_font.render(drone.id, True, TEXT)
            text_rect = text.get_rect(center=(x, y))
            self.screen.blit(text, text_rect)

    def draw_turn(self, turn: int) -> None:
        """Render the current turn counter on screen."""
        text = self.font.render(f"Turn: {turn}", True, TEXT)
        y = self.height - text.get_height() - 10
        self.screen.blit(text, (10, y))

    def render(
        self,
        turn: int,
        previous_drones: Optional[List[Drone]],
        drones: List[Drone],
    ) -> None:
        """Animate and render between previous and current drones."""
        self.clock.tick(60)
        self.handle_events()

        # If paused, wait here until unpaused
        while self.paused and self.running:
            self.handle_events()
            self.clock.tick(60)
            self.pygame.time.delay(100)

        start_drones = (
            previous_drones if previous_drones is not None else drones
        )
        start_positions = get_drone_positions(self.layout, start_drones)
        end_positions = get_drone_positions(self.layout, drones)
        frame_delay_ms = max(1, self.delay_ms // self.transition_steps)

        for step in range(1, self.transition_steps + 1):
            self.handle_events()
            if not self.running:
                return

            progress = step / self.transition_steps
            interpolated_positions: Dict[str, Tuple[float, float]] = {}
            for drone in drones:
                end_x, end_y = end_positions.get(drone.id, (0.0, 0.0))
                start_x, start_y = (
                    start_positions.get(drone.id, (end_x, end_y))
                )
                x = start_x + (end_x - start_x) * progress
                y = start_y + (end_y - start_y) * progress
                interpolated_positions[drone.id] = (x, y)

            self.screen.fill(BACKGROUND)
            self.draw_edges()
            self.draw_nodes(drones)
            self.draw_drones(drones, interpolated_positions)
            self.draw_turn(turn)
            self.pygame.display.flip()
            self.animation_clock.tick(60)
            self.pygame.time.delay(frame_delay_ms)

        hold_elapsed = 0
        while hold_elapsed < self.hold_ms and self.running and not self.paused:
            self.handle_events()
            if not self.running:
                return
            self.screen.fill(BACKGROUND)
            self.draw_edges()
            self.draw_nodes(drones)
            self.draw_drones(drones, end_positions)
            self.draw_turn(turn)
            self.pygame.display.flip()
            step_ms = min(16, self.hold_ms - hold_elapsed)
            self.pygame.time.delay(step_ms)
            hold_elapsed += step_ms

    def handle_events(self) -> None:
        """Handle user input events (pause, speed, quit)."""

        keydown = getattr(self.pygame, "KEYDOWN", None)
        k_space = getattr(self.pygame, "K_SPACE", None)
        k_up = getattr(self.pygame, "K_UP", None)
        k_down = getattr(self.pygame, "K_DOWN", None)
        quit_ = getattr(self.pygame, "QUIT", None)

        for event in self.pygame.event.get():
            if event.type == quit_:
                self.running = False
                return
            if event.type != keydown:
                continue
            if event.key == k_space:
                self.paused = not self.paused
            elif event.key == k_up:
                self.delay_ms = max(
                    self.min_delay_ms, self.delay_ms - self.delay_step
                )
            elif event.key == k_down:
                self.delay_ms = min(
                    self.max_delay_ms, self.delay_ms + self.delay_step
                )

            print(f"Speed: {self.delay_ms}ms")
