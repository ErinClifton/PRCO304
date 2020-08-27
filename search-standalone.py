def binSearch(tar, searchList):
    results = []
    for i in range(len(searchList)):
        if (searchList[i] == tar):
            results.append(i)
    return results

import time
import numpy as np

# dataset of random integers
data = np.random.randint(0,4000,500000)
numToSearchFor = 50

# Search returns all indexs where the search value is found
start = time.time_ns()
SearchResult = binSearch(numToSearchFor, data)
end = time.time_ns()

print((end-start)/1000000000)