"""
"""

# standard
import abc

# custom
from pyz.pathfinding import pathfinding_utils
from pyz.pathfinding import coordinate_utils

####################################

class Mesh(object):

    __metaclass__ = abc.ABCMeta

    def __init__(self, dimensions, corner):
        assert len(dimensions) == len(corner)

        self.mins = tuple(corner)
        self.maxs = tuple(a+b for a,b in zip(dimensions, corner))

    def all_coords(self):
        return coordinate_utils.all_coords(zip(self.mins, self.maxs))

    def contains(self, coord):
        return all(a <= v < b for a,v,b in zip(self.mins, coord, self.maxs))

    @abc.abstractmethod
    def path(self, start, end):
        pass

####################################

class MeshLeaf(Mesh):

    def __init__(self, dimensions, corner, graph):
        Mesh.__init__(self, dimensions, corner)

        self.graph = graph # {coord -> set(coords)} # navigable
        self.edges = coordinate_utils.edge_coords(zip(self.mins, self.maxs))

        self.groups = {}
        self.landlocked_groups = {}
        self.open_groups = {}

        self.links = {}
        self.paths = {}

    def make_open(self):
        self.graph = {coord:self.potential_neighbors(coord) for coord in self.all_coords()}

    def make_closed(self):
        self.graph = {}

    def add_navigable(self, coord):
        if coord in self.graph:
            return

        neighbors = self.neighbors(coord)

        self.graph[coord] = neighbors
        for neighbor in neighbors:
            self.graph[neighbor].add(coord)

    def add_blocked(self, coord):
        if coord not in self.graph:
            return

        try:
            del self.graph[coord]
        except KeyError:
            pass

        neighbors = self.neighbors(coord)
        for neighbor in neighbors:
            self.graph[neighbor].discard(coord)

    ####################################

    def navigable(self):
        return set(self.graph.keys())

    def edges(self):
        return 

    def cost(self, coord_1, coord_2):
        return 1  # stub.

    def potential_neighbors(self, coord):
        return set(c for c in coordinate_utils.cardinal_neighbors(coord) if self.contains(c))

    def neighbors(self, coord):
        return coordinate_utils.cardinal_neighbors(coord) & self.navigable()

    ####################################

    def passable(self, coord):
        return coord in self.graph

    def path(self, start, end):
        return pathfinding_utils.my_a_star(self, start, end)

    def calculate_local_groups(self):

        remaining = self.navigable()

        if not remaining:
            return # completely non-navigable
        
        groups = {}
        label = 0
        while remaining:
            start = min(remaining)
            flood = pathfinding_utils.flood_fill(self.graph, start)

            remaining -= flood
            groups[label] = flood
            label += 1

        landlocked = {}
        open_groups = {}

        for (label,group) in groups.items():
            if not group & self.edges:
                landlocked[label] = group
            else:
                open_groups[label] = group

        self.groups = groups
        self.landlocked_groups = landlocked
        self.open_groups = open_groups

    def calculate_potential_links(self, group_label):
        return self.open_groups[group_label] & self.edges

