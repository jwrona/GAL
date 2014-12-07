from pprint import pprint as pp

__author__ = "Tomas Varga"
__email__  = "xvarga00@stud.fit.vutbr.cz"

class Graph():
    """ class is representing a graph
    """
    ## CLASS METHODS
    def __init__(self, graph=None):
        if graph:
            self.graph = graph
        else:
            self.graph = {}
        
    # used when printing an instance of this object
    def __str__(self):
        pp(self.graph)
        return " "


    ## PRIVATE METHODS
    def __add_nodes(self, nodes):
        for node in nodes:
            if node not in self.graph:
                self.graph[node] = []

    def __add_arcs(self, arcs):
        for arc_from, arc_to in arcs:
            # if the node arc_from doesn't exist, it creates it
            if arc_from not in self.graph:
                self.graph[arc_from] = [arc_to]
            else:
                self.graph[arc_from].append(arc_to)
            # if the node arc_to doesn't exist, it creates it
            if arc_to not in self.graph:
                self.graph[arc_to] = []


    ## PUBLIC METHODS
    # get all graph nodes
    def get_nodes(self):
        return sorted(self.graph.keys())

    # get all graph arcs
    def get_arcs(self):
        return sorted([(arc_from, arc_to) for arc_from in self.graph.iterkeys() for arc_to in self.graph[arc_from]])

    # add one node
    def add_node(self, node):
        self.__add_nodes([node])

    # add list of nodes
    def add_nodes(self, nodes):
        self.__add_nodes(nodes)
        
    # add one arc
    def add_arc(self, arc):
        self.__add_arcs([arc])

    # add list of arcs
    def add_arcs(self, arcs):
        self.__add_arcs(arcs)
