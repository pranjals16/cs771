'''
Created on Aug 7, 2011

@author: ehtsham
'''
import MySQLdb
class RecommendationEngine:
    
    def buildDict(self,curs):
        userDict={}
        for row in curs.fetchall():
            userDict[row[1]]=row[2]
        return userDict
        
    def getRecommendations(self,uID,dbName='Netflix',tb1Name='Watched',
                           tb2Name='ItemMatch'):
        try:
            conn = MySQLdb.connect(user='root',passwd='pranjal',db=dbName)
            curs = conn.cursor()
            query1 =  'select * from %s'%tb1Name+' where uID=%s'
            query2 =  'select * from %s'%tb2Name+' where mID=%s'
            curs.execute(query1,uID)
            
            dictUID = self.buildDict(curs)
            similaritySum={}
            totalScores = {}
            for (movie,rating) in dictUID.items():
                curs.execute(query2,movie)
                dictSimilarItems = self.buildDict(curs)
                for (simMovie,similarity) in dictSimilarItems.items():
                    if simMovie in dictUID: continue
                    totalScores.setdefault(simMovie,0)
                    totalScores[simMovie]+=similarity*rating
                    
                    similaritySum.setdefault(simMovie,0)
                    similaritySum[simMovie]+=similarity
            
            rankings = [(movie,score/similaritySum[movie]) 
                        for movie,score in totalScores.items()]
            
            def myFunc(tuple):
                return tuple[1]
            
            rankings = sorted(rankings, key = myFunc, reverse=True)
            return rankings
        except StandardError as e:
            print e
            conn.close()

def main():
    r =  RecommendationEngine()
    rankings = r.getRecommendations(uID = 87,dbName='Movielens');
    print rankings[0:5]
if __name__ == '__main__':
    main()
            
                
                
