import random
import math
import json
import numpy as np
from normalization import Normalizer
from cluster import Cluster

class KMeanClusterer():

    def __init__(self, observations, k, n):
        self.FIELDSNOTUSE = 2
        self.clusterNumber = k
        self.clusters = []
        self.observations = observations
        self.n = n
        self.initialization()

        while self.assignement():
            for c in self.clusters:
                c.updateCentroid()

        for cluster in self.clusters:
            cluster.sortObservations()
            normal, anomaly = cluster.getAnomaly(self.n)

    def initialization(self):
        for i in xrange(0, self.clusterNumber):
            c = Cluster(i, len(self.observations[0]))
            self.clusters.append(c)

        i = 0
        for obs in self.observations:
            obs = np.append(obs, 0)
            self.clusters[i % self.clusterNumber].addObservation(obs, 0)
            i += 1

        for c in self.clusters:
            c.updateCentroid()
            c.updateDist()

    def assignement(self):
        res = False
        for clu in self.clusters:
            delObs = []
            for i in xrange(0, clu.observations.shape[0]):
                obs = clu.observations[i]
                dist, nearestCluster = self.nearestCluster(obs)
                if not nearestCluster.name == clu.name:
                    nearestCluster.addObservation(obs, dist)
                    delObs.append(i)
                    res = True
            clu.deleteObservation(delObs)
        return res

    def nearestCluster(self, obs):
        res = self.clusters[0]
        minDist = self.computeDistance(obs, res.centroid)
        for cluster in self.clusters:
            newDist = self.computeDistance(obs, cluster.centroid)
            if newDist < minDist:
                minDist = newDist
                res = cluster
        return newDist, res

    def computeDistance(self, obs, centroid):
        res = 0
        for i in xrange(0, len(centroid) - self.FIELDSNOTUSE):
            res += ((obs[i] - centroid[i]) ** 2)

        return math.sqrt(res)

    def jsonify(self):
        #doesn't work anymore
        origin = []
        for i in xrange(0, len(self.observations[0] )):
            origin.append(0)

        res = '{"centroids":['
        for i in xrange(0, self.clusterNumber):
            if i != 0:
                res += ','
            dist = self.computeDistance(origin, self.clusters[i].centroid)
            res += '{"data":' + json.dumps(self.clusters[i].centroid) + ', "cluster":' + str(i) + ', "value":' + str(dist) + '}'
        res += '],"observations":['
        notPrems = False
        for i in xrange(0, self.clusterNumber):
            for obs in self.clusters[i].observations:
                if notPrems:
                    res += ','
                notPrems = True
                dist = self.computeDistance(obs, self.clusters[i].centroid)
                res += '{"data":' + json.dumps(obs) + ', "cluster":' + str(i) + ', "value":' + str(dist) + '}'
        res += '],"N":' + str(self.n) + '}'
        return json.loads(res)

if __name__ == "__main__":

    # datafile = "kddcup.data_10_percent.csv"
    # fields = [0, 4, 5, 6]
    # header = False
    # fieldClass = 41

    # datafile = "kddcup.data_1000.csv"
    # fields = [0, 4, 5, 6]
    # header = False
    # fieldClass = 41

    datafile = "iris.csv"
    fields = [0, 1, 2, 3]
    fieldClass = 4
    header = True

    norm = Normalizer(datafile, header)
    res = norm.run(fields, fieldClass)
    classes = norm.classes
    # kMeanClusterer = KMeanClusterer(res, 3, 50)
