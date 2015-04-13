import numpy as np
import copy as copy
import math

class Cluster():
    def __init__(self, name, length):
        self.length = length
        tmpArr = []
        for x in xrange(0,self.length):
            tmpArr.append(0)
        self.centroid = np.array([tmpArr])
        tmpArr.append(0)
        self.observations = np.array([tmpArr])
        self.initObs = True
        self.name = name

    def addObservation(self, observation, dist):
        observation[observation.shape[0]-1] = dist
        arrayObs = np.array([observation])
        self.observations = np.append(self.observations, arrayObs, axis=0)
        if self.initObs:
            self.initObs = False
            self.observations = np.delete(self.observations, 0, 0)

    def updateDist(self):
        for i in xrange(0,self.observations.shape[0]):
            observation = self.observations[i]
            dist = self.distanceToCentroid(observation)
            observation[observation.shape[0]-1] = dist
            self.observations[i] = observation

    def updateCentroid(self):
        if self.observations.shape[0] > 0:
            self.centroid = np.mean(self.observations, axis=0)

    def deleteObservation(self, delObs):
        self.observations = np.delete(self.observations, delObs, 0)

    def getAnomalies(self, n):
        s = self.observations.shape[0]
        nAnomaly = s * n /100
        nNormal = s - nAnomaly
        if nAnomaly > 0:
            res = np.split(self.observations, [nNormal])
        else:
            res = self.observations, []
        return res

    def sortObservations(self):
        self.observations = self.observations[np.argsort(self.observations[:,-1])]

    def distanceToCentroid(self, obs):
        res = 0
        for i in xrange(0, len(self.centroid)):
            res += ((obs[i] - self.centroid[i]) ** 2)

        return math.sqrt(res)