__author__ = "Tomas Varga"
__email__  = "xvarga00@stud.fit.vutbr.cz"
__author__ = "Jan Wrona"
__email__  = "xwrona00@stud.fit.vutbr.cz"

import networkx as nx
from graph import Graph

def custom2nx(graph_input):
	g = nx.DiGraph()
	g.add_nodes_from(graph_input.keys())
	for node, edges in graph_input.iteritems():
		for edge in edges:
			g.add_edge(node, edge)
	return g


def nx2custom(graph_input):
	g = Graph()
	g.add_nodes(graph_input.nodes())
	g.add_arcs(graph_input.edges())
	return g
