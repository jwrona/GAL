#!/usr/bin/env python2

from __future__ import print_function
import argparse
import time
import multiprocessing
import sys
import networkx as nx
import graph_conv
import gc

from graph import Graph
from tarjan import Tarjan
import gabow

#sys.setrecursionlimit(10000)

parser = argparse.ArgumentParser(description='Algorithms time measurement.')
parser.add_argument('-r', '--resolution', choices=['low', 'mid', 'high'], required=True)
parser.add_argument('-t', '--run-times', type=int, default=3)
parser.add_argument('-n', '--run-number', type=int, default=1000)
parser.add_argument('-d', '--density', type=float, default=0.5)
args = parser.parse_args()

def test(nx_g, cm_g):
	print('Tarjan:     ', Tarjan(cm_g).get_scc())
	print()
	print('Gabow class:', [sorted(component) for component in gabow.Gabow(cm_g).get_scc()])
	print()
	print('Gabow func: ', [sorted(component) for component in gabow.strongly_connected_components_gabow(cm_g)])
	print()
	print('Tarjan NX:  ', [sorted(component) for component in nx.strongly_connected_components(nx_g)])
	print()
	print('Kosaraju NX:', [sorted(component) for component in nx.kosaraju_strongly_connected_components(nx_g)])

def timeit(times, number, nx_g, cm_g):
	results = ([], [], [])
	#results = ([], [], [], [])

	for t in range(times):
		#gc.disable()
		start = time.clock()
		for i in range(number):
			Tarjan(cm_g).get_scc()
		results[0].append(time.clock() - start)

		start = time.clock()
		for i in range(number):
			for component in gabow.strongly_connected_components_gabow(cm_g):
				pass
		results[1].append(time.clock() - start)

		start = time.clock()
		for i in range(number):
			for component in nx.strongly_connected_components(nx_g):
				pass
		results[2].append(time.clock() - start)

		#start = time.clock()
		#for i in range(number):
		#	for component in nx.kosaraju_strongly_connected_components(nx_g):
		#		pass
		#end = time.clock()
		#results[3].append(end - start)
		#gc.enable()
	return results


def measure(graph_size):
	global args
	run_times = args.run_times
	run_number = args.run_number
	density = 1.0 - args.density

	vertices = int(graph_size * density)
	edges = graph_size - vertices
	#max_edges = vertices**2

	print('graph size = {}: {} vertices, {} edges'.format(graph_size, vertices, edges), file=sys.stderr)

	nx_graph = nx.gnm_random_graph(vertices, edges, directed=True)
	custom_graph = graph_conv.nx2custom(nx_graph)

	#test(nx_graph, custom_graph)

	res_tuple = timeit(run_times, run_number, nx_graph, custom_graph)
	print(graph_size, '\t', end='')
	for alg in res_tuple:
		print(min(alg), '\t', end='')
	print()
	sys.stdout.flush()

if __name__ == '__main__':
	start = 0; step = 0; limit = 0
	if args.resolution == 'low':
		start = step = 500
		limit = 25001
	elif args.resolution == 'mid':
		start = step = 100
		limit = 5001
	elif args.resolution == 'high':
		start = step = 10
		limit = 501

	#measure(50)
	#print('|V|+|E|\tTarjan\'s\tGabow\'s\tNX_Tarjan\'s\tNX_Kosaraju\'s')
	print('|V|+|E|\tTarjan\'s\tGabow\'s\tNX_Tarjan\'s\t')

	#parallel run
	cpus = multiprocessing.cpu_count()
	pool = multiprocessing.Pool(cpus / 2)
	pool.map(measure, reversed(range(start, limit, step)))

	#serial run
	#map(measure, reversed(range(start, limit, step)))
