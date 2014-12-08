import networkx as nx
from graph import Graph
import tarjan
import gabow
import graph_conv


if __name__ == '__main__':
	for i in range(3):
		# generate random graph and convert to custom representation
		nx_graph = nx.gnm_random_graph(15, 25, directed=True)
		custom_graph = graph_conv.nx2custom(nx_graph)

		# get strong connected components
		print "Strongly connected components by Tarjan's algorithm:"
		print [ sorted(component) for component in tarjan.strongly_connected_components(custom_graph) ]
		print
		print "Strongly connected components by Gabow's algorithm:"
		print [ sorted(component) for component in gabow.strongly_connected_components(custom_graph) ]
		print
		print "Strongly connected components by Tarjan's networkx library algorithm:"
		print [ sorted(component) for component in nx.strongly_connected_components(nx_graph) ]
		print
		print "Strongly connected components by Kosaraju's networkx library algorithm:"
		print [ sorted(component) for component in nx.kosaraju_strongly_connected_components(nx_graph) ]
		print '-----------------------------------------------------------------------'
