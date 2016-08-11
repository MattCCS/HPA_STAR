
# standard
import time

# custom
from pyz.pathfinding import mesh

####################################

m = mesh.MeshLeaf((10,10), (0,0), {})
m.make_open()
BLOCKED = [
    (1, 7), (1, 8), (2, 7), (2, 8), (3, 7), (3, 8),

    (3, 4), (3, 5), (4, 1), (4, 2),
    (4, 3), (4, 4), (4, 5), (4, 6),
    (4, 7), (4, 8), (5, 1), (5, 2),
    (5, 3), (5, 4), (5, 5), (5, 6),
    (5, 7), (5, 8), (6, 2), (6, 3),
    (6, 4), (6, 5), (6, 6), (6, 7),
    (7, 3), (7, 4), (7, 5)
] # try toggling (5,3)  ;)

for each in BLOCKED:
    m.add_blocked(each)

print m.graph

print m.contains((0,0))
print m.contains((3,7))
print m.contains((9,9))
print m.contains((10,10))
print m.contains((3,17))
print m.contains((-5,0))

t0 = time.time()
out = m.path((2,4), (8,5))
t1 = time.time()
print t1-t0
print

if not out:
    print "No path!"
else:
    print list(out)

print m.calculate_local_zones()
