def performElementwiseFunction(func,dataset1,dataset2=None):
    square = lambda a:a*a # 2
    product = lambda a,b:a*b # P
    addition = lambda a,b:a+b # A
    
    results = []
    if not(dataset2):
        if func == '2':
            for data in dataset1:
                results.append(square(data))
        elif func == 'S':
            results = 0
            for data in dataset1:
                results = addition(results,data)
    else:
        import itertools
        zipData = zip(dataset1,dataset2)
        if func == '2':

        elif func == 'P':
            for zData in zipData:
                results.append(product(zData[1],zData[2]))
        elif func == 'A':
            for zData in zipData:
                results.append(addition(zData[1],zData[2]))
    return results

if __name__ == '__main__':
    import dispy, socket, time
    import numpy as np
    # fetch the IP address of the client
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("10.0.0.1", 80)) # doesn't matter if 8.8.8.8 can't be reached
    cluster = dispy.JobCluster(performElementwiseFunction,ip_addr=s.getsockname()[0], nodes='10.0.0.*')


    data = np.random.randint(0,100,40)
    results = []
    numJobs = 1
    jobs = []

    for i in range(numJobs):
        # schedule execution of 'addElem' on a node (running 'dispynode')
        # with a parameter (random number in this case)
        start = time.time_ns()
        job = cluster.submit('S',data)
        job.id = i # optionally associate an ID to job (if needed later)
        jobs.append(job)
    # cluster.wait() # waits for all scheduled jobs to finish

    for job in jobs:
        n = job() # waits for job to finish and returns results
        end = time.time_ns()
        if not(n):
            # do nothing
            time.sleep(0)
        else:
            results = [*results, *n]
            print('Executed job %s in %s seconds' % (job.id, job.end_time - job.start_time))
            print('job %s actually took %s seconds' % (job.id, ((end-start)/1000000000)))
        # other fields of 'job' that may be useful:
        # print(job.stdout, job.stderr, job.exception, job.ip_addr, job.start_time, job.end_time)
    cluster.print_status()
    cluster.close()
    

    print(results)
