import csv

class Normalizer():
    def conv(self, i, j, s):
        try:
            s = float(s)
        except ValueError:
            if j in self.col:
                if (self.header and i > 0) or not self.header:
                    self.col.remove(j)
        return s

    def load_csv(self, dataFile, header):
        res = []
        defCol = True
        self.header = header
        with open(dataFile, 'rU') as data:
            reader = csv.reader(data)
            i = 0
            for row in reader:
                if defCol:
                    defCol = False
                    self.col = [x for x in range(len(row))]
                rowRes = []
                j = 0
                for cell in row:
                    cell = self.conv(i, j, cell)
                    rowRes.append(cell)
                    j += 1
                res.append(rowRes)
                i += 1
        if header:
            res.pop(0)

        print self.col
        return res
