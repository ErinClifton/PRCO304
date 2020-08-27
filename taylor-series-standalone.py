def taylorarctan(indicies,x):
    import math
    sum = 0
    lastIndex = len(indicies) - 1
    for n in range(indicies[0],indicies[lastIndex]):
        middle = ((2*n)+1)
        sum = sum + ((-1)**n)*((x**(middle)) / (middle))
    return sum


import math, time
import numpy as np

precision = 131072
indicies = list(range(precision))
numJobs = 16
Time = 0
nums = (-0.9999999999,0.9999999999,0.0000000001,0.7853194857,-0.82,0.4792378463)
joblist = np.array_split(indicies,numJobs)

for x in nums:
    results = 0
    start_time = time.time_ns()

    for job in joblist:
        results = results + taylorarctan(job,x)
    
    end_time = time.time_ns()
    Time = ((end_time - start_time)/1000000000)
        
    print("Arctan of %s" % x)
    print("Taylor Approximation at %s precision: %s" % (precision, results))
    realResults = np.arctan(x)
    print("Function Results: %s" % realResults)
    difference = realResults - results
    dPercentage = (1-abs(difference/realResults)) * 100
    print("Similarity: %s %% " % dPercentage)
    print("Time taken: %s" % Time)
    print("")