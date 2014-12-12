#!/usr/bin/env python2
from __future__ import print_function

__author__ = "Jan Wrona"
__email__  = "xwrona00@stud.fit.vutbr.cz"

import argparse, time, multiprocessing, sys, gc, csv
import psutil
import networkx as nx
import graph, tarjan, gabow
from math import sqrt, ceil

alg_setting = {
	'tarjan': {
		'func': tarjan.strongly_connected_components,
		'input': 'custom'
	},
	'gabow': {
		'func': gabow.strongly_connected_components,
		'input': 'custom'
	},
	'tarjan_nx': {
		'func': nx.strongly_connected_components,
		'input': 'nx'
	},
	'kosaraju_nx': {
		'func': nx.kosaraju_strongly_connected_components,
		'input': 'nx'
	}
}

def print_results(nx_g, cm_g):
	""" Print out result by each algorithm.
	    For testing/debuging purposes only.
	"""
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


def get_stats(repetitions, multiplication, algorithms, nx_graph, enable_gc):
	stats = {alg: {'time': [], 'memory': float('nan')} for alg in algorithms}
	custom_graph = graph.nx2custom(nx_graph)

	for alg in algorithms:
		first_run = True
		if not enable_gc: gc.disable()
		process = psutil.Process()
		memory_start = process.memory_info_ex().rss

		for r in range(repetitions):
			if alg_setting[alg]['input'] == 'nx':
				input_graph = nx_graph
			elif alg_setting[alg]['input'] == 'custom':
				input_graph = custom_graph
			scc_function = alg_setting[alg]['func']

			time_start = time.clock()
			for m in range(multiplication):
				for component in scc_function(input_graph):
					pass
			stats[alg]['time'].append(time.clock() - time_start)
			if first_run:
				first_run = False
				stats[alg]['memory'] = process.memory_info_ex().rss - memory_start
				if not enable_gc: gc.enable()

	return stats


def compute_vertices_count(graph_size, density):
	vertices = int(round(graph_size * (1.0 - density)))

	#if edges count would be greater than maximum possible
	#create complete/close to complete graph
	if (graph_size - vertices) > (vertices * vertices - 1):
		vertices = int(ceil(sqrt(graph_size)))

	return vertices


def measure_single(graph_size):
	global args
	time_results = []
	memory_results = []

	print('graph size={}:'.format(graph_size), end=' ')
	for density in args.densities:
		vertices = compute_vertices_count(graph_size, density)
		edges = graph_size - vertices

		nx_graph = nx.gnm_random_graph(vertices, edges, directed=True)
		if nx_graph.number_of_nodes() + nx_graph.number_of_edges() != graph_size:
			time_results.append(float('nan'))
			memory_results.append(float('nan'))
			continue
		print('[D={} |V|={} |E|={}]'.format(density, nx_graph.number_of_nodes(), nx_graph.number_of_edges()), end=' ')

		stats = get_stats(args.repetitions, args.multiplication, [args.algorithm], nx_graph, args.garbage_collection)
		time_results.append(round(min(stats[args.algorithm]['time']), 5))
		memory_results.append(stats[args.algorithm]['memory'] / float(2**20))

	print()
	for res in [(time_results, '_time.csv'), (memory_results, '_memory.csv')]:
		with open(args.output + res[1], 'a') as csvfile:
			writer = csv.writer(csvfile)
			row = [graph_size] + res[0]
			writer.writerow(row)


def measure_multi(graph_size):
	global args

	vertices = compute_vertices_count(graph_size, args.density)
	edges = graph_size - vertices

	nx_graph = nx.gnm_random_graph(vertices, edges, directed=True)
	if nx_graph.number_of_nodes() + nx_graph.number_of_edges() != graph_size:
		return

	print('graph size={}: [D={} |V|={} |E|={}]'.format(graph_size, args.density,
		nx_graph.number_of_nodes(), nx_graph.number_of_edges()))

	stats = get_stats(args.repetitions, args.multiplication, args.algorithms, nx_graph, args.garbage_collection)

	#extract minimal time from all measured times
	for key in stats:
		stats[key]['time'] = round(min(stats[key]['time']), 5)

	#write time and memory values into files as CSV
	for res_type in ['time', 'memory']:
		with open(args.output + '_' + res_type + '.csv', 'a') as csvfile:
			writer = csv.writer(csvfile)
			row = [graph_size] + [stats[key][res_type] for key in sorted(stats)]
			writer.writerow(row)


if __name__ == '__main__':
	#create main parser
	parser = argparse.ArgumentParser(description='SCC algorithms time and space complexity measurement.')
	parser.add_argument('-o', '--output', type=str, required=True,
		help='Output files prefix. OUTPUT_time.csv and OUTPUT_memory.csv will be created.')
	parser.add_argument('-s', '--span', type=str, choices=['low', 'mid', 'high'], default='mid',
		help='Graph size span. The bigger span the lower resolution. Default is \'mid\'.')
	parser.add_argument('-r', '--repetitions', type=int, default=3,
		help='Number of repetitions of each measuring. Default is 3 repetitions.')
	parser.add_argument('-m', '--multiplication', type=int, default=1000,
		help='Number of algorithm runs during one measurement. Default is 1000 runs.')
	parser.add_argument('-g', '--garbage-collection', action='store_true',
		help='Enable garbage collection during measuring.')
	parser.add_argument('-c', '--cpus', type=int, default=0,
		help='Number of used CPUs. By default all CPUs are used.')
	subparsers = parser.add_subparsers(
		help='Measurement mode selection.')
	
	# create the parser for the "single" command
	parser_single = subparsers.add_parser('single',
		help='Single algorithm measurement with variable graph size and density.')
	parser_single.add_argument('--algorithm', type=str, choices=alg_setting.keys(), required=True,
		help='Algorithm to measure.')
	parser_single.add_argument('--densities', type=str, default='0.0,0.5,1.0',
		help='Graph densities. Comma separated real numbers from 0.0 to 1.0. Default values are \'0.0,0.5,1.0\'')
	parser_single.set_defaults(func=measure_single)
	
	# create the parser for the "multi" command
	parser_multi = subparsers.add_parser('multi',
		help='Multiple algorithms measurement with variable graph size.')
	parser_multi.add_argument('--algorithms', type=str, default='tarjan,gabow,tarjan_nx',
		help='Algorithms to measure. Comma separated algorithms. Possible values are: '+', '.join(alg_setting.keys()))
	parser_multi.add_argument('--density', type=float, default=0.5,
		help='Graph density. Real number from 0.0 to 1.0. Default value is \'0.5\'.')
	parser_multi.set_defaults(func=measure_multi)
	
	#parse arguments
	args = parser.parse_args()

	########################################################################
	start = 0; step = 0; limit = 0
	if args.span == 'low':
		start = step = 10
		limit = 501
	elif args.span == 'mid':
		start = step = 100
		limit = 5001
	elif args.span == 'high':
		start = step = 500
		limit = 25001

	#sys.setrecursionlimit(10000)

	#process arguments for signle mode
	if args.func == measure_single:
		#check density corectness and remove duplicates
		args.densities = sorted(set([float(x) for x in args.densities.split(',')]))
		for density in args.densities:
			if density < 0.0 or density > 1.0:
				print('error: bad density', density, file = sys.stderr)
				exit(1)
		#write headers into files
		for suffix in ['_time.csv', '_memory.csv']:
			with open(args.output + suffix, 'w') as csvfile:
				writer = csv.writer(csvfile)
				row = ['|V|+|E|'] + args.densities
				writer.writerow(row)

	#process arguments for multi mode
	elif args.func == measure_multi:
		#check density corectness
		if args.density < 0.0 or args.density > 1.0:
			print('error: bad density', args.density, file = sys.stderr)
			exit(1)
		#split, remove duplicates and sort specified algorithms
		args.algorithms = sorted(set(args.algorithms.split(',')))
		for alg in args.algorithms:
			if alg not in alg_setting.keys(): #check input corectness
				print('error: unknown algorithm \'{}\''.format(alg), file = sys.stderr)
				exit(1)
		#write headers into files
		for suffix in ['_time.csv', '_memory.csv']:
			with open(args.output + suffix, 'w') as csvfile:
				writer = csv.writer(csvfile)
				row = ['|V|+|E|'] + args.algorithms
				writer.writerow(row)

	########################################################################
	if args.cpus == 0: #use all the cpus
		args.cpus = multiprocessing.cpu_count()
	elif args.cpus == -1: #use half of the cpus
		args.cpus = multiprocessing.cpu_count() / 2

	#garbage collector causes problem in space complexity measurement
	#it is necessary to turn it off completely when measuring memory
	#gc.disable()
	pool = multiprocessing.Pool(args.cpus)
	pool.map(args.func, range(start, limit, step))
