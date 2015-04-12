import numpy as np

class Cluster():
    def __init__(self, fields):
        self.observations = []
        self.centroid = []
        self.fields = fields

    def getCentroid(self):
        return self.centroid

    def getObservations(self):
        return self.observations

    def addObservation(self, observation):
        self.observations.append(observation)

    def updateCentroid(self):
        array = np.array(self.observations)
        delFields = []
        for i in xrange(0, len(array[0])):
            if i not in self.fields:
                delFields.append(i)
        array = np.delete(array, delFields, -1)
        array = array.astype(np.float)
        self.centroid = array.mean(axis=0).tolist()

    def deleteObservation(self, obs):
        self.observations.remove(obs)

    def equals(self, other):
        return (self.observations == other.observations) and (self.centroid == other.centroid)
