"""Class definition for Djikstra algorithm node.

Written by: Taylor Denouden
Date: November 24, 2015
"""


class Node:
    """Main class for Djikstra algorithm calculation."""

    def __init__(self, name):
        """Init Djikstra node with name and distance information."""
        self.name = name
        self.visited = False
        self.neighbors = {}
        self.edges = {}

    def get_name(self):
        """Return this nodes name."""
        return self.name

    def set_neighbor(self, node, distance):
        """Set the distance from self to node."""
        self.neighbors[node.get_name()] = node
        self.edges[node.get_name()] = distance

    def get_distance(self, node):
        """Get and return the edge weight between self and node."""
        return self.edges.get(node.get_name(), float("Inf"))

    def get_neighbors(self):
        """Get and return all neighbor nodes as a list."""
        return self.neighbors.values()

    def get_unvisited_neighbors(self):
        """Get and return all neighbor nodes as a list."""
        return [n for n in self.neighbors.values() if not n.get_visited()]

    def get_closest_neighbor(self):
        """Get and return the neighbor that is closest."""
        return self.neighbors[min(self.edges, key=self.edges.get)]

    def get_closest_unvisited_neighbor(self):
        """Get and return the neighbor that is closest and unvisited."""
        unvisited = [k for (k, v) in self.neighbors.iteritems()
                     if not v.get_visited()]

        if len(unvisited) == 0:
            return False

        unvisited_edges = {k: v for (k, v) in self.edges.iteritems()
                           if k in unvisited}
        return self.neighbors[min(unvisited_edges, key=unvisited_edges.get)]

    def set_visited(self, visited=True):
        """Set if node is visited."""
        self.visited = visited

    def get_visited(self):
        """Get node visited status."""
        return self.visited
