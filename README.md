
<img src="https://github.com/mirr-x/42-CC-1337/blob/main/images/flyin.png" alt="42 Porto Common Core Banner" />

*This project has been created as part of the 42 curriculum by molahrac.*

## Description
Fly-in is a Python simulation that routes multiple drones through connected zones
from a start hub to an end hub while respecting movement costs and constraints.
It parses a map description, computes paths, and outputs the drones' movements
turn by turn.

## Instructions
Run the default map:
```bash
make run
```

Run a specific map:
```bash
make run MAP=maps/medium/02_circular_loop.txt
```

Debug:
```bash
make debug MAP=maps/easy/01_linear_path.txt
```

Lint:
```bash
make lint
```

## Algorithm & Implementation Strategy
- The parser reads zones and connections, validates syntax and metadata, and builds
  an adjacency map.
- Paths are computed with a Dijkstra-based search using movement costs
  (restricted zones cost 2 turns, others cost 1). Priority zones are preferred
  by ordering neighbors first during expansion.
- Drones are assigned shortest paths in round-robin order and then simulated
  turn by turn with zone/connection occupancy tracking.

## Visual Representation
The project now renders a fullscreen Pygame view of the network in addition to
the textual turn output.

- Drone colors reflect their current state.
- Planned paths are shown as faint overlays.
- Zone capacity is displayed as `current/max`.
- Drone markers are offset when multiple drones share the same zone.
- `SPACE` pauses or resumes the simulation.
- `UP` and `DOWN` adjust the simulation speed.

The simulation still prints one line per turn containing the movement tokens
(`D<ID>-<zone>` or `D<ID>-<connection>`), so the terminal output remains useful
for debugging and grading.

## Resources
- Dijkstra's algorithm: https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
- Dijkstra's algorithm: https://www.geeksforgeeks.org/dsa/dijkstras-shortest-path-algorithm-greedy-algo-7/
- Dijkstra visualization: https://www.cs.usfca.edu/~galles/visualization/Dijkstra.html
- BFS (Breadth-First Search): https://www.geeksforgeeks.org/dsa/breadth-first-search-or-bfs-for-a-graph/
- Pygame offical DOCS: https://www.pygame.org/docs/

**AI usage:**  was used to review requirements
updates (.gitignore, README) and to assist with pygame logic. All
changes were reviewed and understood before applying.
