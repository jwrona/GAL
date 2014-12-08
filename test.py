import networkx as nx
from networkx.algorithms.components import strongly_connected_components

from graph import Graph
from tarjan import Tarjan
import gabow
import graph_conv


if __name__ == '__main__':
	# generate random graph and convert to custom representation
	nx_graph = nx.gnm_random_graph(15, 25, directed=True)
	custom_graph = graph_conv.nx2custom(nx_graph)

	# get strong connected components
	print "Strong connected components returned from networkx library:"
	print [ sorted(component) for component in nx.strongly_connected_components(nx_graph) ]
	print
	print "Strong connected components returned from Tarjan's algorithm:"
	print Tarjan(custom_graph).get_scc().values()
	print
	print "Strong connected components returned from Gabow's algorithm:"
	print [ sorted(component) for component in gabow.strongly_connected_components_gabow(custom_graph) ]
