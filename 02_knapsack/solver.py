#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import time
from copy import copy
from collections import namedtuple
Item = namedtuple("Item", ['index', 'value', 'weight', 'density'])

sys.setrecursionlimit(20000)

def solve_it(input_data):
	# Modify this code to run your optimization algorithm

	t0 = time.time()

	# parse the input
	lines = input_data.split('\n')

	firstLine = lines[0].split()
	item_count = int(firstLine[0])
	capacity = int(firstLine[1]) # Total capacity

	items = []

	for i in range(1, item_count+1):
	    line = lines[i]
	    parts = line.split()
	    items.append(Item(i-1, int(parts[0]), int(parts[1]), float(parts[0])/float(parts[1])))

	n = item_count
	value = 0	#initial value of items taken
	#weight = capacity	#initial weight capacity
	i = 0
	taken = [0]*len(items)

	sorted_items = sorted(items, key=lambda item: -item.density)
	assert sorted_items[0].density >= sorted_items[1].density
	assert sorted_items[1].density >= sorted_items[2].density

	'''
	# DEBUG sort check
	for item in sorted_items:
		print(item)
	'''

	global best
	best = 0  #global best_value
	global best_path
	best_path = []
	#global visited
	#visited = -1 #global tracker

	def knapsack(i,V,W,path_to_here):
		# V is the value to this point
		# W is capacity left at this call

		#print('path is ')
		#print(map(str,path_to_here))
		#print('')

		# DEBUG check the setting of the global variable
		#global visited
		#visited += 1
		#print('node ' + str(visited) ) # + ': best = ' + str(best))

		global best
		global best_path

		# kickback if item doesn't fit
		if W < 0:
			return -1

		# kickback at leaf node
		if i==n:
			if V > best:
				# global best wuz here
				best = V
				best_path = path_to_here
				#print('best set to ' + str(best))
				#print('net weight = ' + str(capacity-W))
				#print('best_path now: ')
				#print(map(str,best_path))
				#print(" ")
			return V

		# check the bound
		#print("value now = " +str(V) )
		#print("remaining = " +str(W) )

		# bound = sorted_items[i].density*W
		bound = get_bound(i,V,W)

		#print("bound = " +str(bound) )
		#print("best = " +str(best) )
		#print(" ")
		if bound < best:
			return -1

		# return the best solution recursively
		take_path = copy(path_to_here)
		take_path.append(1)
		take_value = knapsack(i+1, V+sorted_items[i].value, W-sorted_items[i].weight, take_path)
		reject_path = copy(path_to_here)
		reject_path.append(0)
		reject_value = knapsack(i+1, V, W, reject_path)
		return max(take_value, reject_value)

	def get_bound(i,V,W):
		bound = 0
		remaining_capacity = W
		for k in range(i,n):
			if sorted_items[k].weight <= remaining_capacity:
				bound += sorted_items[k].value
				remaining_capacity -= sorted_items[k].weight
			elif remaining_capacity > 0:
				bound += sorted_items[k].density*remaining_capacity
				remaining_capacity = 0
			else:
				break
		bound += V
		return bound

	# call the function
	path_to_here = []
	value = knapsack(i,value,capacity,path_to_here)

	assert len(best_path) == len(taken)
	for k in range(len(best_path)):
		if best_path[k] == 1:
			taken[sorted_items[k].index] = 1

	'''
	#naive implementation
	for item in items:
	    if weight + item.weight <= capacity:
	        taken[item.index] = 1
	        value += item.value
	        weight += item.weight
	'''

	'''
	# following approach is modified from
	# https://www.geeksforgeeks.org/knapsack-problem/
	# and some C++ code I found
	V = [[-1 for x in range(K+1)] for y in range(n+1)]
	keep = [[0 for x in range(K+1)] for y in range(n+1)]
	for i in range(n+1):
		for w in range(K+1):
			if i==0 or w==0:
				V[i][w] = 0
			elif items[i-1].weight <= w:
				V[i][w] = max(items[i-1].value+V[i-1][w-items[i-1].weight], V[i-1][w])
				keep[i][w] = 1
			else:
				V[i][w] = V[i-1][w]

	# Backtrack
	remaining_capacity = K
	for i in reversed(range(1,n+1)):
		if (keep[i][remaining_capacity]==1):
			taken[items[i-1].index] = 1
			remaining_capacity -= items[i-1].weight

	value = V[n][K]
	'''


	# DEBUG print the run time
	t1 = time.time()
	total = t1-t0
	#print('time: ' + str(total) + ' seconds')


	# prepare the solution in the specified output format
	output_data = str(value) + ' ' + str(1) + '\n'
	output_data += ' '.join(map(str, taken))
	return output_data

	#return value # DEBUG -- when complete, use the above output data format


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')
