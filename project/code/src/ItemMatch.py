'''
Created on Aug 7, 2011

@author: ehtsham
'''
from __future__ import division
import MySQLdb

class ItemMatch:
    def buildDict(self,curs):
        dictmID = {}
        for row in curs.fetchall():
            dictmID[int(row[0])] = float(row[2])
        
        return dictmID
        
    def getSimilarity(self,curs,mID,otherMovie):
        query = 'select * from Watched where mID=%s'
        curs.execute(query,mID)
        dictmID = self.buildDict(curs)
        curs.execute(query,otherMovie)
        dictOtherMovie = self.buildDict(curs)
        si={}
        for item in dictmID:
            if item in dictOtherMovie:
                si[item]=1
        
        if len(si)==0: return 0
        sumOfSquares= sum([pow(dictmID[item]-dictOtherMovie[item],2) for item in si])
        return 1/(1+sumOfSquares)        
                
    def getTopMatches(self,mID,curs):
        similarities =[(mID,otherMovie,self.getSimilarity(curs,mID,otherMovie))
                        for otherMovie in range(1,1683) 
                        if otherMovie != mID]
        return similarities
    
    def buildItemMatchdb(self,dbName='Netflix'):
        try:
            conn = MySQLdb.connect(user='root',passwd='pranjal',db=dbName)
            curs = conn.cursor()
            curs.execute(''' Create table if not exists ItemMatch(mID Integer, oID Integer,
                            similarity real, primary key(mID,oID))''')
            
            for mID in range(1,1683):
                similarities = self.getTopMatches(mID,curs)
                curs.executemany(''' Insert into ItemMatch(mID,oID,similarity)
                                values(%s,%s,%s) ''', similarities)
                conn.commit()
                print 'records added for %d ...'%mID
            
            conn.close()
        except StandardError as e:
            print e
            conn.close()
    
def main():
    itemMatcher = ItemMatch()
    itemMatcher.buildItemMatchdb('Movielens')

if __name__ == '__main__':
    main()

    
