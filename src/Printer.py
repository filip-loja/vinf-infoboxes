
from src.indexFields import fieldTypes

class Printer:

    printConfig = {
        'keys': list(fieldTypes.keys()),
        'names': ['ID', 'Name', 'Type', 'Country name', 'Population', 'Density', 'Area', 'Elevation', 'Leader name'],
        'paddings': [8,  25,     15,     25,             12,           10,       8,      9,           15]
    }

    def __init__(self, searcher, fieldsToPrint):
        self.processFieldsToPrint(fieldsToPrint)
        self.printOutputHeader()
        i = 1
        if len(searcher.get()) == 0:
            print('Nothing found :(')
        else:
            for doc in searcher.get():
                self.printDoc(doc, i)
                i += 1
        print('')


    def processFieldsToPrint(self, fieldsToPrint):
        if list(fieldsToPrint) == self.printConfig['keys']:
            return

        i = 0
        removeCount = 0
        fieldsToCheck = self.printConfig['keys'].copy()
        for field in fieldsToCheck:
            if field not in fieldsToPrint:
                self.printConfig['keys'].pop(i - removeCount)
                self.printConfig['names'].pop(i - removeCount)
                self.printConfig['paddings'].pop(i - removeCount)
                removeCount += 1
            i += 1


    def printOutputHeader(self):
        output = '#'.ljust(5, ' ')
        i = 0
        for key in self.printConfig.get('names'):
            padding = int(self.printConfig.get('paddings')[i])
            output += ' | ' + key.ljust(padding, ' ')
            i += 1
        print(output)
        headerLength = sum(list(self.printConfig.get('paddings')))
        output = '-'.ljust(headerLength - 1 + 5 + 3 * len(self.printConfig.get('paddings')), '-')
        print(output)


    def printDoc(self, doc, index):
        output = (str(index) + '.').ljust(5, ' ')
        i = 0
        for key in self.printConfig.get('keys'):
            value = doc.get(key) or '-'
            padding = int(self.printConfig.get('paddings')[i])
            output += ' | ' + value.ljust(padding, ' ')
            i += 1
        print(output)
