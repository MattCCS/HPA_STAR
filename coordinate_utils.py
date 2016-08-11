"""
Relatively fast utilities for generating large coordinate sets
for use in pathfinding and game grid management.
"""

def cardinal_neighbors(coord):
    """
    Generates all coordinates in a cardinal direction
    around the given N-dimensional coordinate.
    """

    points = set()
    for i in xrange(len(coord)):
        val = coord[i]
        pre = coord[:i]
        post = coord[i+1:]
        points.add(pre + (val-1,) + post)
        points.add(pre + (val+1,) + post)
    return points

def all_coords(min_maxes):
    """
    Generates all coordinates in the given N-dimensional bounds.
    """
    if not min_maxes:
        yield tuple()

    (min_, max_) = min_maxes[0]

    if len(min_maxes) == 1:
        for i in xrange(min_, max_):
            yield (i,)
    else:
        rest = min_maxes[1:]

        for coord in all_coords(rest):
            for i in xrange(min_, max_):
                yield (i,) + coord

def is_edge(coord, min_maxes):
    """
    Tests whether the coord is an edge
    in the given N-dimensional min_maxes.
    """
    return any(v == a or v == b-1 for v,(a,b) in zip(coord, min_maxes))

def edge_coords(min_maxes):
    """
    Returns all coordinates bounded by the min_maxes
    that falls on 1 or more edges in N dimensions.
    """
    return set(coord for coord in all_coords(min_maxes) if is_edge(coord, min_maxes))
