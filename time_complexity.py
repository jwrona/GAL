#!/usr/bin/env python2

from __future__ import print_function
import argparse
import time
import multiprocessing
import sys
import networkx as nx
import gc
from math import sqrt, ceil

import graph as g
from graph import Graph
import tarjan
import gabow

def test(nx_g, cm_g):
	print('Tarjan class:', [sorted(component) for component in tarjan.Tarjan(cm_g).get_scc()])
	print()
	print('Tarjan func: ', [sorted(component) for component in tarjan.strongly_connected_components(cm_g)])
	print()
	print('Gabow class:', [sorted(component) for component in gabow.Gabow(cm_g).get_scc()])
	print()
	print('Gabow func: ', [sorted(component) for component in gabow.strongly_connected_components(cm_g)])
	print()
	print('Tarjan NX:  ', [sorted(component) for component in nx.strongly_connected_components(nx_g)])
	print()
	print('Kosaraju NX:', [sorted(component) for component in nx.kosaraju_strongly_connected_components(nx_g)])

def time_one(times, number, scc_function, graph):
	run_times = []

	for t in range(times):
		#gc.disable()
		start = time.clock()
		for i in range(number):
			for c in scc_function(graph):
				pass
		run_times.append(time.clock() - start)
		#gc.enable()
	return run_times

def timeit(times, number, nx_g, cm_g):
	results = ([], [], [])
	#results = ([], [], [], [])

	for t in range(times):
		#gc.disable()
		start = time.clock()
		for i in range(number):
			for component in tarjan.strongly_connected_components(cm_g):
				pass
		results[0].append(time.clock() - start)

		start = time.clock()
		for i in range(number):
			for component in gabow.strongly_connected_components(cm_g):
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

def measure_one(graph_size):
	global args
	run_times = args.run_times
	run_number = args.run_number
	results = []

	print('graph size {}: '.format(graph_size), end='')
	for density in args.densities:
	 	if density == 1.0: #complete graph
			vertices = int(ceil(sqrt(graph_size)))
		else:
			vertices = int(round(graph_size * (1.0 - density)))
		edges = graph_size - vertices

		nx_graph = nx.gnm_random_graph(vertices, edges, directed=True)
		if nx_graph.number_of_nodes() + nx_graph.number_of_edges() != graph_size:
			results.append(float('nan'))
			continue
		print('[density {}: {} vertices, {} edges]\t'.format(density, nx_graph.number_of_nodes(), nx_graph.number_of_edges()), end='')

		if args.algorithm == 'tarjan':
			custom_graph = g.nx2custom(nx_graph)
			results.append(min(time_one(run_times, run_number, tarjan.strongly_connected_components, custom_graph)))
		elif args.algorithm == 'gabow':
			custom_graph = g.nx2custom(nx_graph)
			results.append(min(time_one(run_times, run_number, gabow.strongly_connected_components, custom_graph)))
		elif args.algorithm == 'tarjan_nx':
			results.append(min(time_one(run_times, run_number, nx.strongly_connected_components, nx_graph)))
		elif args.algorithm == 'kosaraju_nx':
			results.append(min(time_one(run_times, run_number, nx.kosaraju_strongly_connected_components, nx_graph)))

	print()
	with open(args.output, 'a') as f:
		print(graph_size, '\t', end = '', file = f)
		for density_res in results:
			print(density_res, '\t', end = '', file = f)
		print(file = f)

def measure_all(graph_size):
	global args
	run_times = args.run_times
	run_number = args.run_number
	density = 1.0 - args.density

	vertices = int(graph_size * density)
	edges = graph_size - vertices
	#max_edges = vertices**2

	print('graph size = {}: {} vertices, {} edges'.format(graph_size, vertices, edges))

	nx_graph = nx.gnm_random_graph(vertices, edges, directed=True)
	custom_graph = g.nx2custom(nx_graph)

	#test(nx_graph, custom_graph)

	res_tuple = timeit(run_times, run_number, nx_graph, custom_graph)
	with open(args.output, 'a') as f:
		print(graph_size, '\t', end = '', file = f)
		for alg_res in res_tuple:
			print(min(alg_res), '\t', end='', file = f)
		print(file = f)

if __name__ == '__main__':
	#sys.setrecursionlimit(10000)
	
	#create main parser
	parser = argparse.ArgumentParser(description='Algorithms time measurement.')
	parser.add_argument('-r', '--resolution', type=str, choices=['low', 'mid', 'high'], default='mid')
	parser.add_argument('-t', '--run-times', type=int, default=3)
	parser.add_argument('-n', '--run-number', type=int, default=1000)
	parser.add_argument('-o', '--output', type=str, default=1000, required=True)
	subparsers = parser.add_subparsers(help='measurement mode')
	
	# create the parser for the "one" command
	parser_one = subparsers.add_parser('one', help='one algorithm measurement - variable density')
	parser_one.add_argument('--algorithm', type=str, choices = ['tarjan', 'gabow', 'tarjan_nx', 'kosaraju_nx'], required = True)
	parser_one.add_argument('--densities', type=str, default='0.0,0.5,1.0', help = 'comma separated real numbers from 0.0 to 1.0 range')
	parser_one.set_defaults(func=measure_one)
	
	# create the parser for the "all" command
	parser_all = subparsers.add_parser('all', help='all algorithms measurement - variable size')
	parser_all.add_argument('--density', type=float, default=0.5)
	parser_all.set_defaults(func=measure_all)
	
	#parse arguments
	args = parser.parse_args()

	########################################################################
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

	if args.func == measure_one:
		args.densities = [float(x) for x in args.densities.split(',')]
		for d in args.densities:
			if d < 0.0 or d > 1.0:
				print('error: bad density', d, file = sys.stderr)
				exit(1)

		with open(args.output, 'w') as f:
			print('|V|+|E|\t', end = '', file = f)
			for density in args.densities:
				print(density, '\t', end = '', file = f)
			print(file = f)
	elif args.func == measure_all:
		if args.density < 0.0 or args.density > 1:
			print('error: bad density', args.density, file = sys.stderr)
			exit(1)
		with open(args.output, 'w') as f:
			print('|V|+|E|\tTarjan\'s\tGabow\'s\tNX_Tarjan\'s\t', file = f)
			#print('|V|+|E|\tTarjan\'s\tGabow\'s\tNX_Tarjan\'s\tNX_Kosaraju\'s')
	
	#parallel run
	cpus = multiprocessing.cpu_count()
	pool = multiprocessing.Pool(cpus / 2)
	pool.map(args.func, range(start, limit, step))

	#serial run
	#map(args.func, range(start, limit, step))
