import sys
import os
import re
from sets import Set
import math
import pickle
import matplotlib.pyplot as plt

#os.system('./../dataset/mku.sh')
#print "DONE"

def split(string):
    stringenders = re.compile('[|\t\n]*')
    stringlist = stringenders.split(string)
    return stringlist[0:len(stringlist)-1]

def getdata(filename):
    f = open('./../dataset/'+filename)
    lines = f.readlines()
    f.close()
    dataarray = []
    for i in range(len(lines)):
        dataarray.append(split(lines[i]))
    return dataarray

#def Cosine_Similarity
#def Pearson_cofficient

def Euclidean_Similarity(i,j,dictaux):
    commonmovielist = set(dictaux[i].keys()).intersection(set(dictaux[j].keys()))
    ans = 0.0
    for k in commonmovielist:
        ans = ans + pow(int(dictaux[i][k])-int(dictaux[j][k]),2)

    if (ans==0.0):
        return 1000000000000
    return math.sqrt(ans)

def compute_similarity(userinfo,maindict):
    similarity = [[10000000 for x in xrange(len(userinfo))] for x in xrange(len(userinfo))] 
    for i in range(len(userinfo)-1):
        for j in range(i+1,len(userinfo)):
            temp = 1/(1+Euclidean_Similarity(userinfo[i][0],userinfo[j][0],maindict))
            similarity[i][j] = temp
            similarity[j][i] = temp
    return similarity            

def k_similar_users(i,similarity,k):
    similarusers = []
    for p in range(len(userinfo)):
        j = userinfo[p][0]
        if(j!=i):
            similarusers.append([j,similarity[int(i)-1][int(j)-1]])
    similarusers = sorted(similarusers,key=lambda a:a[1])
    return similarusers[0:k]


def k_watched_users(i,similarity,dictaux,movie,k):
    similarusers = []
    for j in range(len(userinfo)):
        if (j!=i):
            if (movie in dictaux[userinfo[j][0]]):
                similarusers.append([userinfo[j][0],float(dictaux[userinfo[j][0]][movie])])
    similarusers = sorted(similarusers,key=lambda a:a[1])
    if (len(similarusers)<k):
        return similarusers
    return similarusers[0:k]            

def predict1(users,data,movie,dictaux):
    numerator = 0.0
    denominator = 0.0
    for j in range(len(users)):
        if (movie in dictaux[users[j][0]]):
            numerator = numerator + users[j][1]*float(dictaux[users[j][0]][movie])
        denominator = denominator + users[j][1]
    if (denominator == 0):
        return 0
    return numerator/denominator

def build_dict(data,userinfo):
    main = dict()
    for i in range(len(userinfo)):
        helper=dict()
        for j in range(len(data)):
            if(data[j][0]==userinfo[i][0]):
                helper[data[j][1]] = data[j][2]
        main[userinfo[i][0]] = helper
    return main


userinfo = getdata('u.user')


for i in range(2,6):
    u1base = getdata('u'+str(i)+'.base')
    u1test = getdata('u'+str(i)+'.test')

    #uncomment these lines and comment the below 4
    #for one time calculation and storage of everything
    #
    #then you can again comment these and uncomment those for fast processing
    '''
    print 'building_dictionary'
    maindict = build_dict(u1base,userinfo)
    print 'building_similarity matrix'
    similarity = compute_similarity(userinfo,maindict)
    print 'done'
    output = open('initialdata'+str(i)+'.pkl','wb')
    pickle.dump(maindict,output)
    pickle.dump(similarity,output,-1)
    output.close()
    '''
    pkl_file = open('initialdata'+str(i)+'.pkl','rb')
    maindict = pickle.load(pkl_file)
    similarity = pickle.load(pkl_file)
    pkl_file.close()


    #ans = 0

    #for i in range(len(u1test)):
    #    similaruseri = k_similar_users(u1test[i][0],similarity,20)
    #    x = predict1(similaruseri,u1base,u1test[i][1],maindict)
    #    ans = ans + pow( x - int(u1test[i][2]),2)

    #print math.sqrt(ans/len(u1test))

    arr = []
    arr2 = []
    for k in range(1,251):
        print 'U'+str(i)+' --> iteration for k = '+str(k)
        ans = 0
        for j in range(len(u1test)):
            similaruseri = k_watched_users(u1test[j][0],similarity,maindict,u1test[j][1],k)
            x = predict1(similaruseri,u1base,u1test[j][1],maindict)
            ans = ans + pow( x - int(u1test[j][2]),2)
        arr.append(math.sqrt(ans/len(u1test)))
        arr2.append(k)
    plt.figure()    
    plt.plot(arr2,arr)
    plt.title('Root Mean Square vs K nearest neighbours in UBCF')
    plt.xlabel('K')
    plt.ylabel('RMSE')
    plt.savefig('K_watched_users_datasplit_'+str(i)+'.png')

    



    
