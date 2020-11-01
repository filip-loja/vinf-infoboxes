
from src.indexFields import fieldTypes

class Printer:

    printConfig = {
        'keys': fieldTypes.keys(),
        'names': ('ID', 'Name', 'Type', 'Country name', 'Population', 'Density', 'Area', 'Elevation', 'Leader name'),
        'paddings': (6, 20, 10, 25, 12, 10, 8, 9, 15)
    }

    def __init__(self, searcher):
        self.printOutputHeader()
        i = 1
        for doc in searcher.get():
            self.printDoc(doc, i)
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
