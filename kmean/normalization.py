import csv

class Normalizer():
    def conv(self, i, j, s):
        try:
            s = float(s)
        except ValueError:
            if j in self.colFloat:
                if (self.header and i > 0) or not self.header:
                    self.colFloat.remove(j)
        return s

    def __init__(self, dataFile, header):
        self.data = []
        defCol = True
        self.header = header
        with open(dataFile, 'rU') as desc:
            reader = csv.reader(desc)
            i = 0
            for row in reader:
                if defCol:
                    defCol = False
                    self.colFloat = [x for x in range(len(row))]
                rowRes = []
                j = 0
                for cell in row:
                    cell = self.conv(i, j, cell)
                    rowRes.append(cell)
                    j += 1
                self.data.append(rowRes)
                i += 1
        if header:
            self.data.pop(0)

    def getColFloat(self):
        return self.colFloat

    def getData(self):
        return self.data
