"""Class definition for Djikstra algorithm node.

Written by: Taylor Denouden
Date: November 24, 2015
"""


class Node:
    """Main class for Djikstra algorithm calculation."""

    def __init__(self, name):
        """Init Djikstra node with name and distance information."""
        self.name = name
        self._visited = False
        self._neighbors = {}
        self._edges = {}

    def set_neighbor(self, node, distance):
        """Set the distance from self to node."""
        self._neighbors[node.name] = node
        self._edges[node.name] = distance

    def get_distance(self, node):
        """Get and return the edge weight between self and node."""
        return self._edges.get(node.name, float("Inf"))

    def get_neighbors(self):
        """Get and return all neighbor nodes as a list."""
        return self._neighbors.values()

    def get_unvisited_neighbors(self):
        """Get and return all neighbor nodes as a list."""
        return [n for n in self._neighbors.values() if not n.get_visited()]

    def get_closest_neighbor(self):
        """Get and return the neighbor that is closest."""
        return self._neighbors[min(self._edges, key=self._edges.get)]

    def get_closest_unvisited_neighbor(self):
        """Get and return the neighbor that is closest and unvisited."""
        unvisited = [k for (k, v) in self._neighbors.iteritems()
                     if not v.get_visited()]

        if len(unvisited) == 0:
            return False

        unvisited_edges = {k: v for (k, v) in self._edges.iteritems()
                           if k in unvisited}
        return self._neighbors[min(unvisited_edges, key=unvisited_edges.get)]

    def set_visited(self, visited=True):
        """Set if node is visited."""
        self._visited = visited

    def get_visited(self):
        """Get node visited status."""
        return self._visited
