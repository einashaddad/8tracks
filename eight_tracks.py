import pyquery

MAX_DEGREE = 10000
MAX_ERRORS = 1000
MAX_NODES  = 10000000

def get_followers(username):
    '''
    Returns a list of users following username [follower1, follower2, ...]
    '''
    page = pyquery.PyQuery(url='http://8tracks.com/users/%s/followers?page=1&per_page=%d' % (username, MAX_DEGREE))
    followers = page('a.propername')[:-1]
    return [pyquery.PyQuery(f).attr('href') for f in followers]

def get_following(username):
    '''
    Returns a list of users followed by username [following1, following2, ...]
    '''
    page = pyquery.PyQuery(url='http://8tracks.com/users/%s/following?page=1&per_page=%d' % (username, MAX_DEGREE))
    following = page('a.propername')[:-1]
    return [pyquery.PyQuery(f).attr('href') for f in following]

def download_data(seed_user='/hey-hey-love'):
    '''
    Downloads the follower-following graph from 8tracks starting from
    an initial seed_user. Writes the output to a file.

    '''

    to_process = set([seed_user])
    visited = set()
    edges = []

    with open('8tracks.edges', 'w') as fout: # just open a file to write our edges to

        n_processed = 0
        n_errors = 0
        while to_process and n_processed < MAX_NODES:
            if n_errors > MAX_ERRORS: 
                print 'serious errors'
                break
            try:
                user = to_process.pop()
                
                print 'processing', user

                followers = get_followers(user)
                following = get_following(user)

                visited.add(user)

                new_edges = [(f, user) for f in followers] + [(user, f) for f in following]
                edges += new_edges

                # write the edges every time we donwload new ones so we don't lose our progress
                for edge in new_edges: 
                    fout.write('%s\t%s\n' % edge)

                def is_visited(user):
                    return user not in visited

                to_process.update(filter(is_visited, followers+following))
            except:
                n_errors += 1

            n_processed += 1
    print 'processed: ', n_processed
    print 'errors: ', n_errors

if __name__ == '__main__':
    download_data()