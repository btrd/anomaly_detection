import csv
from collections import OrderedDict

class Normalizer():
    def conv(self, s):
        print "conv" + str(s)
        try:
            s = float(s)
        except ValueError:
            pass    
        return s

    def load_csv(self, dataFile, header):
        print "load_csv"
        res = []
        with open(dataFile, 'rU') as data:
            reader = csv.reader(data)
            for row in reader:
                rowRes = []
                for cell in row:
                    cell = self.conv(cell)
                    rowRes.append(cell)
                res.append(rowRes)
        if header:
            res.pop(0)
        return res
