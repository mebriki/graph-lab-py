import unittest

from weighted_graph import WGraph
from unweighted_graph import UGraph


class TestWeightedGraph(unittest.TestCase):
    def setUp(self):
        self.graph = {
            "A": [("B", 1), ("C", 4)],
            "B": [("A", 1), ("C", 2), ("D", 5)],
            "C": [("A", 4), ("B", 2), ("D", 1)],
            "D": [("B", 5), ("C", 1)],
        }
        self.wg = WGraph(self.graph)

    def test_dijkstra_shortest_paths(self):
        result = self.wg.dijkstra("A")
        self.assertEqual(result["A"], (["A"], 0.0))
        self.assertEqual(result["B"], (["A", "B"], 1.0))
        self.assertEqual(result["C"], (["A", "B", "C"], 3.0))
        self.assertEqual(result["D"], (["A", "B", "C", "D"], 4.0))

    def test_dijkstra_rejects_negative_weights(self):
        bad = WGraph({"A": [("B", -1)], "B": []})
        with self.assertRaises(Exception) as ctx:
            bad.dijkstra("A")
        self.assertIn("Negative weight", str(ctx.exception))

    def test_bellman_ford_matches_expected(self):
        result = self.wg.bellman_ford("A")
        self.assertEqual(result["A"], (["A"], 0.0))
        self.assertEqual(result["B"], (["A", "B"], 1.0))
        self.assertEqual(result["C"], (["A", "B", "C"], 3.0))
        self.assertEqual(result["D"], (["A", "B", "C", "D"], 4.0))

    def test_bellman_ford_detects_negative_cycle(self):
        bad = WGraph({
            "A": [("B", 1)],
            "B": [("C", -3)],
            "C": [("A", 1)],
        })
        with self.assertRaises(Exception) as ctx:
            bad.bellman_ford("A")
        self.assertIn("Negative cycle", str(ctx.exception))

    def test_prim_total_weight(self):
        mst = self.wg.prim().graph
        total = sum(weight for edges in mst.values() for _, weight in edges) / 2
        self.assertEqual(total, 4)

    def test_prim_disconnected_graph_raises(self):
        disconnected = WGraph({
            "A": [("B", 1)],
            "B": [("A", 1)],
            "C": [],
        })
        with self.assertRaises(Exception) as ctx:
            disconnected.prim()
        self.assertIn("disconnected", str(ctx.exception).lower())

    def test_kruskal_total_weight(self):
        mst = self.wg.kruskal().graph
        total = sum(weight for edges in mst.values() for _, weight in edges) / 2
        self.assertEqual(total, 4)

    def test_is_cyclic_true_and_false(self):
        self.assertTrue(self.wg.isCyclic())

        acyclic = WGraph({
            "A": [("B", 1)],
            "B": [("A", 1), ("C", 2)],
            "C": [("B", 2)],
        })
        self.assertFalse(acyclic.isCyclic())


class TestUnweightedGraph(unittest.TestCase):
    def test_best_path_shortest(self):
        ug = UGraph({
            "A": ["B", "C"],
            "B": ["D"],
            "C": ["D"],
            "D": [],
        })
        self.assertEqual(ug.bestPath("A", "D"), ["A", "B", "D"])

    def test_best_path_missing_or_unreachable(self):
        ug = UGraph({"A": ["B"], "B": [], "C": []})
        self.assertEqual(ug.bestPath("A", "C"), [])
        self.assertEqual(ug.bestPath("A", "Z"), [])

    def test_cycle_detection_directed(self):
        cyclic = UGraph({"A": ["B"], "B": ["C"], "C": ["A"]})
        acyclic = UGraph({"A": ["B"], "B": ["C"], "C": []})
        self.assertTrue(cyclic.isCyclic())
        self.assertFalse(acyclic.isCyclic())


if __name__ == "__main__":
    unittest.main()
