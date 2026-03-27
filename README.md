# 🕸️ graph-lab-py

A clean, Pythonic implementation of **weighted** and **unweighted** graph data structures. This repository serves as a foundational playground for learning graph theory and testing network algorithms.

## 🚀 Overview

This lab contains two core implementations:
- `unweighted_graph.py`: Basic node-edge connections where all paths have an equal cost.
- `weighted_graph.py`: Connections with assigned weights, representing distance, cost, or time.

## 📂 Project Structure

```text
graph-lab-py/
├── unweighted_graph.py  # Graph implementation (0 or 1 edge values)
├── weighted_graph.py    # Graph implementation (numerical edge weights)
├── tests/
│   └── test_graphs.py   # Smoke tests for shortest paths, MSTs, and cycles
└── README.md            # You are here!
```

## ✅ Run Tests

From the project root:

```bash
python3 -m unittest tests/test_graphs.py -v
```

This validates:
- weighted shortest paths (Dijkstra, Bellman-Ford)
- weighted MST (Prim, Kruskal)
- cycle detection for weighted/unweighted graphs
- edge cases like disconnected/unreachable inputs

## 🧪 Usage Examples

### Weighted Graph

```python
from weighted_graph import WGraph

g = WGraph({
	"A": [("B", 1), ("C", 4)],
	"B": [("A", 1), ("C", 2), ("D", 5)],
	"C": [("A", 4), ("B", 2), ("D", 1)],
	"D": [("B", 5), ("C", 1)],
})

print(g.dijkstra("A"))
print(g.bellman_ford("A"))
print(g.prim().graph)
print(g.kruskal().graph)
print(g.isCyclic())
```

### Unweighted Graph

```python
from unweighted_graph import UGraph

g = UGraph({
	"A": ["B", "C"],
	"B": ["D"],
	"C": ["D"],
	"D": [],
})

print(g.bestPath("A", "D"))
print(g.isCyclic())
```

## 📊 Visualizations

### Weighted Sample Graph

```mermaid
graph LR
	A((A)) -- "1" --- B((B))
	A -- "4" --- C((C))
	B -- "2" --- C
	B -- "5" --- D((D))
	C -- "1" --- D

	classDef node fill:#f8fafc,stroke:#334155,stroke-width:2px,color:#0f172a;
	class A,B,C,D node;
```

### Shortest Path from A to D (Cost = 4)

```mermaid
graph LR
	A((A)) -- "1" --> B((B))
	B -- "2" --> C((C))
	C -- "1" --> D((D))
	A -. "4" .-> C
	B -. "5" .-> D

	classDef pathNode fill:#ecfdf3,stroke:#0b6e4f,stroke-width:3px,color:#064e3b;
	classDef otherNode fill:#f8fafc,stroke:#64748b,stroke-width:2px,color:#0f172a;
	class A,B,C,D pathNode;

	%% Selected shortest-path links: A->B, B->C, C->D
	linkStyle 0,1,2 stroke:#0b6e4f,stroke-width:4px;
	%% Non-selected links: A->C, B->D
	linkStyle 3,4 stroke:#94a3b8,stroke-width:2px,stroke-dasharray: 6 6;
```

Shortest path result from `A` to `D`: `A -> B -> C -> D` with total cost `4`.

### MST (Prim/Kruskal Output)

```mermaid
graph LR
	A((A)) -- "1" --- B((B))
	B -- "2" --- C((C))
	C -- "1" --- D((D))

	classDef mst fill:#fff7ed,stroke:#c2410c,stroke-width:3px,color:#7c2d12;
	class A,B,C,D mst;
```

### Unweighted Sample Graph

```mermaid
graph TD
	A((A)) --> B((B))
	A --> C((C))
	B --> D((D))
	C --> D

	classDef source fill:#e0f2fe,stroke:#0369a1,stroke-width:3px,color:#0c4a6e;
	classDef target fill:#fef3c7,stroke:#b45309,stroke-width:3px,color:#78350f;
	class A source;
	class D target;
```

## Notes

- `dijkstra` raises an exception if any edge has a negative weight.
- `prim` raises an exception when the graph is disconnected.
- `bestPath` returns `[]` when no path exists or if a node is missing.
