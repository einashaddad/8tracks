'''
This is an implementation of PageRank derrived from the CS 101 course on Udacity. 
'''

import operator

def demo(): 
	'''
	Simple Demo of the functionality
	'''
	with open('./8tranks.sample2', 'r') as f:
		lines = [line.strip() for line in f.readlines()]
		edges = [tuple(line.split('\t')) for line in lines]
	graph = change_graph(edges)
	ranks = compute_ranks(graph)
	disp_popular(ranks)

def change_graph(edges):
	'''
	Changes the graph from the form /follower /user to a dictionary where the 
	keys are the users and the values are the followers of each user.
	''' 
	graph = {}
	for edge in edges:
		if edge[1] not in graph:
			graph[edge[1]] = [edge[0]]
		else:
			graph[edge[1]].append(edge[0])
	return graph

def compute_ranks(graph):
	'''
	Computes the ranks of each user using the PageRank algorithm.
	'''
	d = 0.8 # damping factor
	numloops = 10
    
	ranks = {}
	nusers = len(graph)
	for user in graph:
		ranks[user] = 1.0 / nusers
    
	for i in range(0, numloops):
		print 'iteration: %d' % i
		newranks = {}
		# computes page rank for "user"
		for user in graph:
			newrank = (1 - d) / nusers

			for node in graph:
				if node in graph[user]:
					newrank = newrank + d * (ranks[node] / len(graph[node]))

			newranks[user] = newrank
		ranks = newranks
	return ranks

def disp_popular(ranks):
	'''
	Displays a sorted representation of the dictionary of ranks and prints the 10 highest
	ranked users.
	'''
	sorted_users = sorted(ranks.iteritems(), key=operator.itemgetter(1))
	sorted_users.reverse()
	# top 10
	if len(ranks) < 10:
		for i in xrange(len(ranks)):
			print sorted_users[i][0]
	else:
		for i in xrange(10):
			print sorted_users[i][0]

if __name__ == '__main__':
    demo()

