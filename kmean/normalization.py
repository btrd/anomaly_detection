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

    def run(self, fields, fieldClass):
        if self.header:
            head = 1
        else:
            head = 0
        fields.append(fieldClass)

        classes = self.runClasses(fieldClass)

        classes_map = dict([(s, i) for i, s in enumerate(classes)])
        class2id = lambda s: classes_map.get(s, -1)

        self.data = np.loadtxt(open(self.dataFile,"rb"), usecols=fields, delimiter=",", converters={fieldClass:class2id}, skiprows=head)

        return self.data

    def runClasses(self, fieldClass):
        self.classes = []
        with open(self.dataFile, 'rU') as desc:
            reader = csv.reader(desc)
            for row in reader:
                if row[fieldClass] not in self.classes:
                    self.classes.append(row[fieldClass])
        if self.header:
            self.classes.pop(0)
        return self.classes

    def getColFloat(self):
        title = []
        res = []
        floats = []
        i = 0
        with open(self.dataFile, 'rU') as desc:
            reader = csv.reader(desc)
            line = reader.next()
            for cell in line:
                if self.header:
                    title.append(cell)
                else:
                    title.append(i)
                i += 1

            line = reader.next()
            for cell in line:
                try: 
                    float(cell)
                    floats.append(True)
                except ValueError:
                    floats.append(False)
                    
            i = 0
            for elem in title:
                if floats[i]:
                    res.append((i,elem))
                i += 1
            return res
