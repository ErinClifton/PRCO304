def cmap(mapCen, mapData):
    mapResults = []
    numFeatures = len(mapData[0])
    ##for each data piece
    for dataToMap in mapData:
        eucDists = []
        ##check Square Euclidean Distance to each centroid
        for cen in mapCen:
            SED = 0
            for feature in range(numFeatures):
                dif = cen[feature] - dataToMap[feature]
                SED = SED + (dif * dif)
            eucDists.append(SED)
        ##add the index of the lowest distance (which will be the cetroid ID) to the results
        mapResults.append(eucDists.index(min(eucDists)))
    return(mapResults)

def featureAverage(fData):
    numFData = len(fData)
    sumFData = 0
    for fDataEle in fData:
        sumFData = sumFData + fDataEle
    meanFData = sumFData/numFData
    return(meanFData)
    
def sortDataToCluster(dataToSort, dataIndicies, k):
    clusteredData = []
    ##set up empty results array
    for cluster in range(k):
        clusteredData.append([])
    ##dataIndicies[d] returns the centroid ID of the data stored in dataToSrt[d]
    for d in range(len(dataToSort)):
        clusteredData[dataIndicies[d]].append(dataToSort[d])
    return(clusteredData)

import numpy as np
import time

##read in data from text file, split into lines and turned into floats
f = open("data.txt","r")
data = [[float(num) for num in line.split()] for line in f.readlines()]
f.close()

numdata = len(data) ##length of dataset
features = len(data[0]) ##length of a single data piece

k = 15
centroidID = np.random.permutation(numdata)
centroids = np.random.rand(k,features)
for i in range(k):
    centroids[i] = data[i]

start_time = time.time_ns()

results = cmap(centroids,data)

end_time = time.time_ns()

clusteredData = sortDataToCluster(data,results,k)
##clusteredData[class][data][feature]



##setup empty results
results = []

##for each cluster
for i in range(k):
    ##get number of Data in Cluster (numDiC)
    numDiC = len(clusteredData[i])
    ##for each feature in current cluster
    for j in range(features):
        featureList = []
        ##collect each value of chosen feature from data in cluster
        for m in range(numDiC):
            featureList.append(clusteredData[i][m][j])
        ##if no data in cluster, use centroid instead    
        if (len(featureList)) == 0:
            featureList.append(centroids[i][j])
        ##send off to be calculated
        results.append(featureAverage(featureList))
        
##rebuild centroids from results
newCentroids = centroids
for i in range(k):
    for j in range(features):
        newCentroids[i][j] = results[(features*i) + j]
##check to see if centroids have changed
compare = centroids == newCentroids
if compare.all():
    ##if so stop classifying
    #break
    print('Finished')
else:
    centroids = newCentroids
    ##if not keep classifying

print("time taken: %s" % ((end_time - start_time)/1000000000))
