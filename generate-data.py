import sklearn.datasets as dataset
numdata = 100000
features = 7
centers = 15
data = dataset.make_blobs(n_samples=numdata, n_features=features, centers=centers)
f=open("data.txt","w")
for a in data[0]:
    tempstr = ""
    for x in a:
        tempstr = tempstr + str(x) + " "
    tempstr = tempstr + "\r\n"
    f.write(tempstr)
f.close()
