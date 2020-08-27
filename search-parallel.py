def binSearch(tar, searchList):
    results = []
    for i in range(len(searchList)):
        if (searchList[i] == tar):
            results.append(i)
    return results

def binContains(tar, searchList):
    results = False
    for ele in searchList:
        if ele == tar:
            results = True
            break
    return results

if __name__ == '__main__':
    import dispy, socket, time
    import numpy as np
    
    # fetch the IP address of the client
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("10.0.0.2", 80))
    # doesn't matter if IP cannot be reached, only that the socket exists
    
    cluster = dispy.JobCluster(binSearch,ip_addr=s.getsockname()[0], nodes=['10.0.0.3','10.0.0.4','10.0.0.5','10.0.0.6'])
    data = np.random.randint(0,4000,500000)
    numJobs = 16
    
    jobData = np.array_split(data,numJobs)
    jobs = []
    results = []
    
    searchTarget = 50
    
    for D in jobData:
        job = cluster.submit(searchTarget, D)
        jobs.append(job)
        
    for job in jobs:
        result = job()
        results = [*results, *result]
        
    print(results)
    cluster.print_status()
    cluster.close()
    