__author__ = "Jan Wrona"
__email__  = "xwrona00@stud.fit.vutbr.cz"


preorder_counter = 0

class Gabow():
	""" Class implementing Gabow's algorithm for getting
	    strongly connected components.
	"""

	## CLASS METHODS
	def __init__(self, graph):
		self.graph = graph

		self.preorder_counter = 0
		self.preorder = {}
		self.stack_s = []
		self.stack_p = []


	## PRIVATE METHODS
	def __scc_visit(self, node):
		""" Recursive function for founding
		    strongly connected components of graph.
		"""
		self.preorder[node] = self.preorder_counter
		self.preorder_counter += 1

		self.stack_s.append(node)
		self.stack_p.append(node)

		for neighbor in self.graph.graph[node]:
			if neighbor not in self.preorder:
				for component in self.__scc_visit(neighbor):
					yield component
			elif neighbor in self.stack_s:
				while self.preorder[self.stack_p[-1]] > self.preorder[neighbor]:
					self.stack_p.pop()

		if self.stack_p[-1] == node:
			popped = None
			component = []
			while popped != node:
				popped = self.stack_s.pop()
				component.append(popped)
			self.stack_p.pop()
			yield component


	## PUBLIC METHODS
	def get_scc(self):
		""" Returns dictionary of strongly connected components.
		"""
		for node in self.graph.get_nodes():
			if node not in self.preorder:
				for component in self.__scc_visit(node):
					yield component


def strongly_connected_components_gabow(graph):
	""" Function implementing Gabow's algorithm for getting
	    strongly connected components.
	"""

	def __scc_visit(node):
		""" Recursive function for founding
		    strongly connected components of graph.
		"""
		global preorder_counter

		preorder[node] = preorder_counter
		preorder_counter += 1

		stack_s.append(node)
		stack_p.append(node)

		for neighbor in graph.graph[node]:
			if neighbor not in preorder:
				for c in __scc_visit(neighbor):
					yield c
			elif neighbor in stack_s:
				while preorder[stack_p[-1]] > preorder[neighbor]:
					stack_p.pop()

		if stack_p[-1] == node:
			popped = None
			component = []
			while popped != node:
				popped = stack_s.pop()
				component.append(popped)
			stack_p.pop()
			yield component

	#######################################################################
	preorder_counter = 0
	preorder = {}
	stack_s = []
	stack_p = []

	for node in graph.get_nodes():
		if node not in preorder:
			for c in __scc_visit(node):
				yield c
