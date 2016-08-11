
# Adapted from http://www.redblobgames.com/pathfinding/

# standard
import heapq

####################################

class PriorityQueue(object):
    def __init__(self):
        self.elements = []
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self):
        return heapq.heappop(self.elements)[1]

####################################

def heuristic(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)

def extract_path(came_from, goal):

    steps = []
    current = goal

    while True:
        steps.append(current)
        current = came_from[current]
        if current is None:
            break

    return reversed(steps)

def my_a_star(graph, start, goal):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()
        
        if current == goal:
            return extract_path(came_from, goal)
        
        for next_ in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, next_)
            if next_ not in cost_so_far or new_cost < cost_so_far[next_]:
                cost_so_far[next_] = new_cost
                priority = new_cost + heuristic(goal, next_)
                frontier.put(next_, priority)
                came_from[next_] = current

####################################

def flood_fill(graph, start):
    """
    Flood-fills the graph from start.
    Graph must be a mapping of {hashable -> set(hashable)}
    """

    seen = set()
    frontier = set([start])

    while frontier:
        seen.update(frontier)
        frontier = set().union(*(graph[n] for n in list(frontier) if n in graph)) - seen

    return seen
