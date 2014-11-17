'''
Created on Aug 7, 2011

@author: ehtsham
'''
import gzip;

def buildList():
    f=gzip.open('/mnt/workspace/NetFlix/data/sample-train.gz', 'r');
    movies = []
    for l in f:
        l=l.strip()
        if(l.endswith(':')):
            movies.append(l.strip(':'))
    f.close()
    return movies
def main():
    movies=buildList();
    print len(movies)

if __name__ == '__main__':
    main()


