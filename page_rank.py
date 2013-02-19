'''
This is an implementation of PageRank derrived from the CS 101 course on Udacity. 
'''

import operator

def demo(): 
	'''
	Simple Demo of the functionality
	'''
	with open('./8tracks.sample', 'r') as f:
		lines = [line.strip() for line in f.readlines()]
		edges = [tuple(line.split('\t')) for line in lines]
	graph = change_graph(edges)
	ranks = compute_ranks(graph)
	disp_popular(ranks)
	genre_ranks = conditional_page_rank(graph, '/arabic')

def load_genre_data(filename):
	'''
	Returns a dictionary of users as key and the user's genre as the values
	- {user: [genre1, genre2, ...], user2: [genre1, genre2, ...]}
	'''
	with open(filename, 'r') as f:
		users = [line.strip() for line in f.readlines()]
		genres = [user.split('\t') for user in users] #genres is a list of lists [[user, genre1 genre2], [user2, genre genre2]]
		genres.pop(0) #this removes the initial newline in the file
		return {genre[0]: set(genre[1].split()) for genre in genres if len(genre) > 1}

def make_subgraph(graph, specified_genre):
	'''
	Makes a subgraph of the original graph, including the user only if associated with given genre
	'''
	genres_dict = load_genre_data('genre.info')
	return {k:v for k, v in graph.items() \
		if k in genres_dict and specified_genre in genres_dict[k]}

def conditional_page_rank(graph, genre):
	'''
	Runs page rank on the new subgraph accoring to the genre selected
	'''
	subgraph = make_subgraph(graph, genre)
	ranks = compute_ranks(subgraph)
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
	with open('popular.ranks', 'w') as f:

		sorted_users = sorted(ranks.iteritems(), key=operator.itemgetter(1))
		sorted_users.reverse()
		# top 10
		if len(ranks) < 10:
			for i in xrange(len(ranks)):
				f.write(sorted_users[i][0]) 
		else:
			for i in xrange(10):
				f.write(sorted_users[i][0])

if __name__ == '__main__':
    demo()

