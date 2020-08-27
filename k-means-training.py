def cmap(mapCen, mapData):
    mapResults = []
    numFeatures = len(mapData[0])
    ##for each data piece
    for dataToMap in mapData:
        eucDists = []
        ##iterate through each centroid
        for cen in mapCen:
            ##find the Squared Euclidean Distance to the data piece
            SED = 0
            for feature in range(numFeatures):
                dif = cen[feature] - dataToMap[feature]
                SED = SED + (dif * dif)
            eucDists.append(SED)
        ##record the centroid with the shortest distance
        mapResults.append(eucDists.index(min(eucDists)))
    return(mapResults)

def sortDataToCluster(dataToSort, dataIndicies, k):
    clusteredData = []
    ##set up empty results array
    for cluster in range(k):
        clusteredData.append([])
    ##dataIndicies[d] returns the centroid ID of the data stored in dataToSrt[d]
    for d in range(len(dataToSort)):
        clusteredData[dataIndicies[d]].append(dataToSort[d])
    return(clusteredData)

if __name__ == '__main__':
    import dispy, socket, time
    import numpy as np
    import matplotlib.pyplot as plt
    
    ##fetch the IP address of the client
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("10.0.0.2", 80)) ##doesn't matter if 8.8.8.8 can't be reached
    
    ##read in data from text file, split into lines and turned into floats
    f = open("data.txt","r")
    data = [[float(num) for num in line.split()] for line in f.readlines()]
    f.close()

    numdata = len(data) ##length of dataset
    features = len(data[0]) ##length of a single data piece

    ##set k
    k = 7
    
    ##choose random centroids from available data
    centroidID = np.random.permutation(numdata)
    centroids = np.empty((k,features))
    for i in range(k):
        centroids[i] = data[centroidID[i]]
    
    ##repeat cycle x number of times to train centroids
    numtrials = 10
    numNodes = 32 ##usually total number of core on network, maybe 2 times the number if feeling generous)
    numtrialtaken = 0
    
    for trialNum in range(numtrials):
        ## reset cluster for fresh use
        cluster = dispy.JobCluster(cmap,ip_addr=s.getsockname()[0], nodes=['10.0.0.3','10.0.0.4','10.0.0.5','10.0.0.6'])
        
        ##split each data piece into its own job
        numJobs = numNodes
        results = []
        jobData = np.array_split(data,numJobs)
        starts = []
        ends = []
        jobs = []
        
        ##new method writing direct into job list, however, it doesnt allow for adding a jobID to the job
        #jobs = [cluster.submit(centroids,jobData[i]) for i in range(numJobs)]

        for i in range(numJobs):
            ##schedule execution of 'cmap' on a node (running 'dispynode')
            ##with parameters (centroids of classes, batch of data to be classified)
            starts.append(time.time_ns())
            job = cluster.submit(centroids,jobData[i])
            job.id = i 
            jobs.append(job)

        for job in jobs:
            n = job() ##get job results
            ends.append(time.time_ns())
            ##.append would create a sublist. Dereferencing arrays when combine prevents this
            if n is not None:
                results = [*results, *n]
            print('Executed cmap job %s in %s seconds' % (job.id, job.end_time - job.start_time))
        cluster.print_status()
        ##MUST be called before new cluster defined
        cluster.close()
        
        for i in range(len(starts)):
            print('Job %s completed in real time of %s' %(i, ((ends[i] - starts[i])/1000000000)))

        ##sort data into clusters. This can be done as simple assignment into a list so parallelizing this would be worthless
        clusteredData = sortDataToCluster(data,results,k)
        ##clusteredData[class][data][feature]
        
        ##setup empty results
        results = []
        
        ##do feature averaging client side. Doing it server side results in speedup < 1 due to network latency
        ##for each cluster
        for i in range(k):
            numDiC = len(clusteredData[i])
            ##for each feature in chosen cluster
            for j in range(features):
                featureSum = 0
                featureAvg = 0
                ##collect each value of chosen feature from data in cluster
                for m in range(numDiC):
                    featureSum = featureSum + clusteredData[i][m][j]
                ##if no data in cluster, use centroid instead    
                if (featureSum == 0):
                    featureAvg = centroids[i][j]
                else:
                    featureAvg = featureSum/numDiC
                ##store result
                results.append(featureAvg)
                
        ##rebuild centroids from results
        newCentroids = centroids
        for i in range(k):
            for j in range(features):
                newCentroids[i][j] = results[(features*i) + j]
        ##check to see if centroids have changed
        compare = centroids == newCentroids
        if compare.all():
            ##if so stop classifying
            numtrialtaken = trialNum
            trialNum = numtrials - 1 ##exit the loop
        else:
            ##if not keep classifying
            centroids = newCentroids
    
    ##display results for 2D data in 7 or fewer clusters
    if ((k <= 7) and (features == 2)):
        colors = ['blue','green','red','yellow','orange','brown','purple']
        centroidsx = []
        centroidsy = []
        ##plot each cluster
        for a in range(k):
            tempX = []
            tempY = []
            for d in clusteredData[a]:
                tempX.append(d[0])
                tempY.append(d[1])
            lbl = 'class ' + str(a)
            plt.scatter(tempX, tempY, label = lbl, color = colors[a], marker = '*')
        ##plot centroids
        for c in range(k):
            plt.scatter(centroids[c][0], centroids[c][1], color = 'black', marker = '.', s = 50)
        ##plot graph labels
        plt.xlabel('Feature 1')
        plt.ylabel('Feature 2')
        titlestr = 'Classification of data after ' + str(numtrialtaken) + ' k-means trials'
        plt.title(titlestr)
        plt.legend()
        
        ##show figure
        plt.show()
