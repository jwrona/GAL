__author__ = "Tomas Varga"
__email__  = "xvarga00@stud.fit.vutbr.cz"

dfs_index = 1

class Tarjan():
	""" Class representing Tarjan's structure for getting
	    strongly connected components.
	"""

	## CLASS METHODS
	def __init__(self, graph):
		self.component_index = 1
		self.dfs_index = 1
		self.graph = graph
		self.mark = { node:0 for node in self.graph.get_nodes() }
		self.link = { node:0 for node in self.graph.get_nodes() }
		self.dfsn = { node:0 for node in self.graph.get_nodes() }
		self.stack = []


	## PRIVATE METHODS
	def __find_scc(self, node):
		""" Recursive function for founding 
		    strongly connected components of graph.
		"""
		self.dfsn[node] = self.dfs_index
		self.link[node] = self.dfsn[node]
		self.dfs_index += 1
		self.stack.append(node)
		self.mark[node] = -1

		for succ_node in self.graph.graph[node]:
			if self.mark[succ_node] == 0:
				self.__find_scc(succ_node)
				self.link[node] = min(self.link[node], self.link[succ_node])
			elif self.mark[succ_node] == -1:
				self.link[node] = min(self.link[node], self.dfsn[succ_node])

		if self.link[node] == self.dfsn[node]:
			while True:
				stack_node = self.stack.pop()
				self.mark[stack_node] = self.component_index
				if stack_node == node:
					break
			self.component_index += 1


	## PUBLIC METHODS
	def get_scc(self):
		""" Returns dictionary of strongly connected components.
		"""
		for node in self.graph.get_nodes():
			if self.mark[node] == 0:
				self.__find_scc(node)

		scc_dict = {}		
		for key, value in sorted(self.mark.iteritems()):
			scc_dict.setdefault(value, []).append(key)
		return scc_dict

def strongly_connected_components(graph):
	""" Function implementing Tarjan's algorithm for getting
	    strongly connected components.
	"""

	def __scc_visit(node):
		""" Recursive function for founding
		    strongly connected components of graph.
		"""
		global dfs_index

		dfsn[node] = dfs_index
		link[node] = dfsn[node]
		dfs_index += 1
		stack.append(node)
		mark[node] = -1

		for succ_node in graph.graph[node]:
			if mark[succ_node] == 0:
				for c in __scc_visit(succ_node):
					yield c
				link[node] = min(link[node], link[succ_node])
			elif mark[succ_node] == -1:
				link[node] = min(link[node], dfsn[succ_node])

		if link[node] == dfsn[node]:
			component = []
			while True:
				stack_node = stack.pop()
				component.append(stack_node)
				mark[stack_node] = 1
				if stack_node == node:
					break
			yield component

	#######################################################################
	global dfs_index
	dfs_index = 1
	mark = { node:0 for node in graph.get_nodes() }
	link = { node:0 for node in graph.get_nodes() }
	dfsn = { node:0 for node in graph.get_nodes() }
	stack = []

	for node in graph.get_nodes():
		if mark[node] == 0:
			for c in __scc_visit(node):
				yield c
