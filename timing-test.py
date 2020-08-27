def timeFunc():
    import time,socket
    time.sleep(1)
    return socket.gethostname()


if __name__ == '__main__':
    import dispy, socket, time
    import numpy as np
    # fetch the IP address of the client
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("10.0.0.1", 80)) # doesn't matter if 8.8.8.8 can't be reached
    cluster = dispy.JobCluster(timeFunc,ip_addr=s.getsockname()[0], nodes='10.0.0.*')

    numJobs = 16
    starts = []
    ends = []

    results = []
    jobs = []

    for i in range(numJobs):
        job = cluster.submit()
        starts.append(time.time_ns())
        job.id = i # optionally associate an ID to job (if needed later)
        jobs.append(job)
    # cluster.wait() # waits for all scheduled jobs to finish


    for i in range(numJobs):
        host = job()
        ends.append(time.time_ns())
        print('Dispy calculated %s executed job %s in %s seconds' % (host, jobs[i].id, jobs[i].end_time - jobs[i].start_time))
        # other fields of 'job' that may be useful:
        # print(job.stdout, job.stderr, job.exception, job.ip_addr, job.start_time, job.end_time)
        print('Real time taken calculated as: %s seconds' % ((ends[i] - starts[i]) / 1000000000))
    cluster.print_status()
    cluster.close()

    print('Overall time taken: %s seconds' % ((ends[len(ends)-1] - starts[0]) / 1000000000))
