import datetime
import json
import os
import glob

from java.nio.file import Paths
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import IndexOptions, IndexWriter, IndexWriterConfig
from org.apache.lucene.document import Document, Field, FieldType, IntPoint, DoublePoint
from src.indexFields import fieldTypes

class Indexer:
    filePath = None
    indexPath = None

    lineCount = 0
    loaderRange = 0
    currentLoader = 0
    processedLineCount = 0

    writer = None
    basicField = None

    fieldTypes = fieldTypes
    includedFields = []

    def __init__(self, inputFile, indexFolder):
        startTime = datetime.datetime.now()
        print('Indexing started')

        self.basicField = FieldType()
        self.basicField.setStored(True)
        self.basicField.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)

        self.includedFields = self.fieldTypes.keys()
        self.filePath = inputFile
        self.indexPath = indexFolder

        self.purgeIndexFolder()
        self.initIndexWriter()
        self.readFile()
        self.writer.close()

        endTime = datetime.datetime.now()
        secondsFloat = (endTime - startTime).total_seconds()
        seconds = int(secondsFloat)
        milliseconds = round((secondsFloat - seconds) * 1000, 4)
        print('\nTotal execution time {}s {}ms'.format(seconds, milliseconds))


    def purgeIndexFolder(self):
        files = glob.glob(self.indexPath + '*')
        for f in files:
            os.remove(f)
        print('Index directory purged')


    def initIndexWriter(self):
        fsDir = SimpleFSDirectory(Paths.get(self.indexPath))
        writerConfig = IndexWriterConfig(StandardAnalyzer())
        self.writer = IndexWriter(fsDir, writerConfig)


    def readFile(self):
        try:
            file = open(self.filePath, 'r')
            with file:
                line = file.readline().strip()
                self.loadLineCount(int(line))

                self.processedLineCount = 1
                line = file.readline().strip()
                while line:
                    self.processLine(line)
                    self.processedLineCount += 1
                    self.showLoader()
                    line = file.readline().strip()
            file.close()
        except IOError:
            print('File ' + self.filePath + ' could not be opened!')


    def loadLineCount(self, lineCount):
        self.lineCount = lineCount
        self.loaderRange = round(lineCount / 20)


    def showLoader(self):
        l = round(self.processedLineCount / self.loaderRange)
        if l > self.currentLoader:
            self.currentLoader = l
            print('\rGenerating index  ...  %d%%' % (self.currentLoader * 5), end='')


    def processLine(self, line):
        record = json.loads(line)
        keys = record.keys()
        doc = Document()

        for key in keys:
            if key not in self.includedFields:
                continue

            filedType = self.fieldTypes.get(key)
            value = record.get(key)
            if value is None:
                continue

            doc.add(Field(key, value, self.basicField))

            if filedType == 'IntPoint':
                doc.add(IntPoint(key, int(value)))

            if filedType == 'DoublePoint':
                doc.add(DoublePoint(key, value * 1.00))

        self.writer.addDocument(doc)
