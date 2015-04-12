import random
import math
import numpy as np
from normalization import Normalizer
from cluster import Cluster

class KMeanClusterer():

    def __init__(self, observations, fields, k, n):
        self.clusterNumber = k
        self.clusters = []
        self.datafile = datafile
        self.observations = observations
        self.fields = fields

        self.initialization()

        while self.assignement():
            for c in self.clusters:
                c.updateCentroid()

    def initialization(self):
        for x in xrange(0, self.clusterNumber):
            c = Cluster(self.fields)
            self.clusters.append(c)

        i = 0
        for obs in self.observations:
            self.clusters[i % self.clusterNumber].addObservation(obs)
            i += 1

        for c in self.clusters:
            c.updateCentroid()

    def assignement(self):
        res = False
        for c in self.clusters:
            obs = c.getObservations()
            for o in obs:
                nearestCluster = self.nearestCluster(o)
                if not nearestCluster.equals(c):
                    nearestCluster.addObservation(o)
                    c.deleteObservation(o)
                    res = True
        return res

    def nearestCluster(self, obs):
        res = self.clusters[0]
        minDist = self.computeDistance(obs, res.getCentroid())
        for cluster in self.clusters:
            newDist = self.computeDistance(obs, cluster.getCentroid())
            if newDist < minDist:
                minDist = newDist
                res = cluster
        return res

    def computeDistance(self, obs, centroid):
        res = 0
        i = 0
        for f in self.fields:
            res += ((obs[f] - centroid[i]) ** 2)
            i += 1

        return math.sqrt(res)

    def testIris(self):
        i = 0
        for c in self.clusters:
            setosa = 0.0
            versicolor = 0.0
            virginica = 0.0
            for o in c.getObservations():
                if o[4] == "Iris-setosa":
                    setosa += 1
                elif o[4] == "Iris-versicolor":
                    versicolor += 1
                elif o[4] == "Iris-virginica":
                    virginica += 1
            nO = len(c.getObservations())
            print "Cluster: " + str(i)
            i += 1
            print "setosa: " + str(setosa/nO*100) + "%"
            print "versicolor: " + str(versicolor/nO*100) + "%"
            print "virginica: " + str(virginica/nO*100) + "%"
            print ""

if __name__ == "__main__":
    datafile = "kddcup.data_10_percent.csv"
    fields = [0, 4, 5, 6]

    #datafile = "iris.csv"
    #fields = [0, 1, 2, 3]

    norm = Normalizer()
    iris_data = norm.load_csv(datafile, False)

    kMeanClusterer = KMeanClusterer(iris_data, fields, 3, 0)
    kMeanClusterer.testIris()
