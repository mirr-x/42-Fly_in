
This project has been created as part of the 42 curriculum by molahrac.*

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
The simulation outputs one line per turn containing the movement tokens
(`D<ID>-<zone>` or `D<ID>-<connection>`). This textual trace provides a clear
step-by-step visualization of drone progress. (Color metadata is parsed but not
rendered yet.)

## Resources
- Dijkstra's algorithm: https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
- Dijkstra's algorithm: https://www.geeksforgeeks.org/dsa/dijkstras-shortest-path-algorithm-greedy-algo-7/
- Dijkstra visualization: https://www.cs.usfca.edu/~galles/visualization/Dijkstra.html
- BFS (Breadth-First Search): https://www.geeksforgeeks.org/dsa/breadth-first-search-or-bfs-for-a-graph/

**AI usage:**  was used to review requirements and generate tooling
updates (Makefile, .gitignore, README) and to assist with code audits. All
changes were reviewed and understood before applying.
