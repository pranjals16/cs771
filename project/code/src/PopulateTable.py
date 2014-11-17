'''
Created on Aug 7, 2011

@author: ehtsham
'''
import gzip
import MySQLdb

class PopulateTable:
    def getTableCreationQuery(self,dbName):
        if dbName=='Movielens':
            return '''Create table if not exists Watched(uID Integer,mID Integer,
                        rating real, primary key (uID,mID))'''
    def getInsertionQuery(self,dbName):
        if dbName == 'Movielens':
            return '''Insert into Watched(uID,mID,rating) 
                        values(%s,%s,%s) '''
    
    def fillDB(self,dbName):
        try:
            conn = MySQLdb.connect(user='root',passwd='pranjal',db=dbName)
            curs = conn.cursor()
            query1 = self.getTableCreationQuery(dbName)
            query2 = self.getInsertionQuery(dbName)
            
            # Create the table
            curs.execute(query1)
            
            # Fill up the table
            i=0
            for record in self.getNextGeneralRecord(dbName):
                try:
                    curs.execute(query2,record)
                    i+=1
                    if i%10000 == 0:
                        print 'entered %dth  record in %s'%(i,dbName)
                except StandardError as e:
                    print e
            
            conn.commit()
            conn.close()
        
        except StandardError as e:
            print e
            conn.commit()
            conn.close()
            
        
    def getNextGeneralRecord(self,dbName):
        if dbName == 'Movielens':
            path = '/home/pranjal/cs771/project/ml-100k/'
            movies={}
            for line in open(path+'/u.item','rU'):
                (id,title) = line.split('|')[0:2]
                movies[id] = title
            
            for line in open(path+'/u80.data'):
                (user,movieid,rating)=line.split('\t')[0:3]
                yield (int(user),movieid,float(rating))
        
        
    def fillNetflixdb(self):
        try:
            conn = MySQLdb.connect(user='root',passwd='enter your password',db='Netflix')
            curs = conn.cursor()
            curs.execute('''Create Table if not exists Watched_test1(
                            uID Integer,
                            mID Integer,
                            rating Real,
                            date Date,
                            Primary Key(uID,mID))''')
            
            query='''Insert 
                     Into Watched_test(uID,mID,rating,date) 
                     Values(%s,%s,%s,%s)'''
            i=0;
            for record in self.getNextRecord():
                curs.execute(query,record)
                i+=1
                if i==10000:
                    print 'Entering %d record ...'% i
                    break
            
            conn.commit()
            conn.close()
            print 'done!'
        except StandardError as e:
            print e
        
    def getNextRecord(self):
        
        """
        1:
        1488844,3,2005-09-6
        
        """
        
        f = gzip.open('/mnt/workspace/NetFlix/data/sample-query-sol.gz', 'r')
        record = []
        for line in f:
            line = line.strip()
            if(line.endswith(':')):
                mID = int(line.strip(':'))
            
            else:
                tokens = line.split(',')
                uID = int(tokens[0])
                rating = float(tokens[1])
                date = [int(d) for d in tokens[2].split('-')]
                record.append(uID)
                record.append(mID)
                record.append(rating)
                record.append(MySQLdb.Date(date[0],date[1],date[2]))
                yield record
                record=[]

def main():
    t = PopulateTable()
    #t.fillNetflixdb()
    t.fillDB('Movielens')

    
    
    
if __name__ == '__main__':
    main()
    
        

