"""
"""

# standard
import abc

# TODO: need code for A* search


class AbstractPathNode(object):
    
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def path(self, start, end):
        pass


class PathLeaf(AbstractPathNode):

    def __init__(self):
        raise NotImplementedError()
    
    def path(self, start, end):
        raise NotImplementedError()


class PathZone(AbstractPathNode):

    def __init__(self, dimensions=None):
        if dimensions is None:
            dimensions = (4,4,4)

        self.dimensions = dimensions

    def path(self, start, end):
        raise NotImplementedError()

PathLeaf()
