import networkx as nx
from networkx.algorithms.components import strongly_connected_components

from graph import Graph
from tarjan import Tarjan


def custom2nx(graph_input):
	g = nx.DiGraph()
	g.add_nodes_from(graph_input.keys())
	for node, edges in graph_input.iteritems():
		for edge in edges:
			g.add_edge(node, edge)
	return g


def nx2custom(graph_input):
	g = Graph()
	g.add_arcs(graph_input.edges())
	return g


if __name__ == '__main__':
	# generate random graph and convert to custom representation
	nx_graph = nx.gnm_random_graph(15, 25, directed=True)
	custom_graph = nx2custom(nx_graph)

	# get strong connected components
	print "Strong connected components returned from networkx library:"
	print [ sorted(component) for component in nx.strongly_connected_components(nx_graph) ]
	print
	print "Strong connected components returned from Tarjan's algorithm:"
	print Tarjan(custom_graph).get_scc().values()
	print
	print "Strong connected components returned from Gabow's algorithm:"
	print "TODO: Here print the output of Gabow's algorihtm"
	

