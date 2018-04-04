from collections import namedtuple
Item = namedtuple("Item", ['index', 'value', 'weight', 'density'])

# test values
n = 3
K = 9
values = [5, 6, 3]
weights = [4, 5, 2]

'''
n = 4
K = 11
values = [8, 10, 15, 4]
weights = [4, 5, 8, 3]
'''

items = []

for i in range(0, n):
    items.append(Item(i, values[i], weights[i], float(values[i])/float(weights[i])))

sorted_items = sorted(items, key=lambda item: -item.density)
assert sorted_items[0].density >= sorted_items[1].density
assert sorted_items[1].density >= sorted_items[2].density

print(sorted_items)

upper_bound_table = {}



def knapsack_solver(i, upstream_value, path_to_here, remaining_capacity):

	# We're looking at item i (0 is the first item)
	this_item = sorted_items[i]

	if i == n-1:
		if this_item.weight <= remaining_capacity:
			path_to_here.append(1)
			value = upstream_value + this_item.value
			return value, path_to_here
		else:
			path_to_here.append(0)
			value = upstream_value
			return value, path_to_here



	# Otherwise, operate recursively
	accept_path = path_to_here
	accept_path.append(1)
	accept_upper_bound = get_upper_bound(accept_path, upstream_value, remaining_capacity)
	reject_path = path_to_here
	reject_path.append(0)
	reject_upper_bound = get_upper_bound(reject_path, upstream_value, remaining_capacity)

	if this_item.weight > remaining_capacity:
		# If the accept branch gives a better best estimate
		assert accept_upper_bound != reject_upper_bound
		if accept_upper_bound > reject_upper_bound:
			accept_value, accept_path = knapsack_solver(i+1, upstream_value+this_item.value, accept_path, remaining_capacity-this_item.weight)
			return accept_value, accept_path
		else:
			reject_value, reject_path = knapsack_solver(i+1, upstream_value, reject_path, remaining_capacity)
			return reject_value, reject_path

	# Else if it doesn't fit we have to reject it
	reject_value, reject_path = knapsack_solver(i+1, upstream_value, reject_path, remaining_capacity)
	return reject_value, reject_path




def get_upper_bound(path, upstream_value, remaining_capacity):
	# add or get the value from the dictionary
	path_str = ''
	for c in range(len(path)):
		path_str += str(path[c])
	if path_str not in upper_bound_table:
		upper_bound = compute_upper_bound(i, upstream_value, remaining_capacity)
		upper_bound_table[path_str] = upper_bound
	else:
		upper_bound = upper_bound_table[path_str]
	return upper_bound


def compute_upper_bound(i, upstream_value, remaining_capacity):
	value_from_here = 0
	for item in sorted_items[i:]:
		if item.weight <= remaining_capacity:
			value_from_here += item.value
			remaining_capacity -= item.weight
		else:
			value_from_here += item.density*remaining_capacity
	upper_bound = upstream_value + value_from_here
	return upper_bound



best_value, path = knapsack_solver(0, 0, [], K)
print(best_value)
print(path)


# a trivial greedy algorithm for filling the knapsack
# it takes items in-order until the knapsack is full
'''
value = 0
weight = 0
taken = [0]*len(items)


for item in items:
    if weight + item.weight <= capacity:
        taken[item.index] = 1
        value += item.value
        weight += item.weight

# prepare the solution in the specified output format
output_data = str(value) + ' ' + str(0) + '\n'
output_data += ' '.join(map(str, taken))
print(output_data)
'''
