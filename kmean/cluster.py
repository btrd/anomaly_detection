import numpy as np

class Cluster():
    def __init__(self, fields):
        self.observations = []
        self.centroid = []
        self.fields = fields

    def addObservation(self, observation):
        self.observations.append(observation)

    def updateCentroid(self):
        arrayObs = np.array(self.observations)
        delFields = []
        for i in xrange(0, len(arrayObs[0])):
            if i not in self.fields:
                delFields.append(i)
        arrayObs = np.delete(arrayObs, delFields, -1)
        arrayObs = arrayObs.astype(np.float)
        self.centroid = arrayObs.mean(axis=0).tolist()

    def deleteObservation(self, obs):
        self.observations.remove(obs)

    def equals(self, other):
        return (self.observations == other.observations) and (self.centroid == other.centroid)

    def sortObservations(self):
        arrayObs = np.array(self.observations)
        for obs in arrayObs:
            obs.append(distanceToCentroid(obs))
        arrayObs[arrayObs[:,-1].argsort()]

    def distanceToCentroid(self, obs):
        res = 0
        i = 0
        for f in self.fields:
            res += ((obs[f] - self.centroid[i]) ** 2)
            i += 1

        return math.sqrt(res)