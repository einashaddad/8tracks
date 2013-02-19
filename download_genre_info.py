import pyquery
import urllib

def get_genres(username):
	'''
	For a given user, get_genres returns a list of genres associated with the user.
	'''
    page = pyquery.PyQuery(url='http://8tracks.com%s' % username)
    genres = page('a.tag')[:-1]
    return [pyquery.PyQuery(g).attr('href')[8:] for g in genres] #/explore/instrumental -- just instrumental

def get_users(filename):
	'''
	Opens the existing file with the graph and returns a set of users.
	'''
	with open(filename, 'r') as f:
		edges = [line.strip().split('\t') for line in f.readlines()]

		users = set()
		for u, v in edges:
			users.add(u)
			users.add(v)

		return users

def download_genre_data(users, filename='genre.info'):
	'''
	Downloads the genres associated with each user. 
	Writes the user \t genre1 genre2 genre3 to a file
	'''
	with open(filename, 'w') as fout:
		for user in users:
			try:		
				genres = get_genres(user)
				fout.write('\n%s\t' % user)
				for genre in genres:
					fout.write('%s ' % urllib.unquote_plus(genre))
			except:
				n_errors =+ 1
	print '# errors' % n_errors

if __name__ == '__main__':
	users = get_users('8tracks.edges')
	download_genre_data(users, 'genre.info')