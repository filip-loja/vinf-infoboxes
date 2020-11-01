
import sys

class CmdHandler:

    modules = ('indexer', 'searcher')
    moduleName = None

    def __init__(self):
        if len(sys.argv) == 1:
            raise Exception('Module name is undefined!')

        self.moduleName = sys.argv[1]
        if self.moduleName not in self.modules:
            raise Exception('Module name is invalid! The following modules are allowed: ' + ', '.join(self.modules))


    def getModule(self):
        return self.moduleName
