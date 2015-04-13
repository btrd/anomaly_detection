import csv
import numpy as np

class Normalizer():
    def __init__(self, dataFile, header):
        self.dataFile = dataFile
        self.header = header

    def getCol(self):
        res = []
        i = 0
        with open(self.dataFile, 'rU') as desc:
            reader = csv.reader(desc)
            for row in reader:
                for cell in row:
                    if self.header:
                        res.append(cell)
                    else:
                        res.append(i)
                    i += 1
                return res
            

    def run(self, fields):
        if self.header:
            head = 1
        else:
            head = 0
        self.data = np.loadtxt(open(self.dataFile,"rb"), usecols=fields, delimiter=",", skiprows=head)

    def getData(self):
        return np.array(self.data)
