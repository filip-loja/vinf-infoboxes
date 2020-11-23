import time
import json
import glob
import os

from java.nio.file import Paths
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import IndexOptions, IndexWriter, IndexWriterConfig
from org.apache.lucene.document import Document, Field, FieldType, IntPoint, DoublePoint

from src.indexFields import fieldTypes
from src.timer import printExecutionTime

class Indexer:
    filePath = None
    indexPath = None

    lineCount = 0
    loaderRange = 0
    currentLoader = 0
    processedLineCount = 0
    lastProgress = -1

    writer = None
    basicField = None

    fieldTypes = fieldTypes
    includedFields = []

    def __init__(self, inputFile, indexFolder):
        startTime = time.time()
        print('Indexing started')

        self.basicField = FieldType()
        self.basicField.setStored(True)
        self.basicField.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)

        self.includedFields = self.fieldTypes.keys()
        self.filePath = inputFile
        self.indexPath = indexFolder

        self.lineCount = self.loadLineCount()
        self.purgeIndexFolder()
        self.initIndexWriter()
        self.readFile()
        self.writer.close()

        print('\nIndexing finished')
        printExecutionTime(startTime)


    def purgeIndexFolder(self):
        files = glob.glob(self.indexPath + '*')
        for f in files:
            os.remove(f)
        print('Index directory purged')


    def loadLineCount(self):
        try:
            count = 0
            file = open(self.filePath, 'r')
            with file:
                line = file.readline()
                count += 1
                while line:
                    line = file.readline()
                    count += 1
            file.close()
            return count
        except:
            return None


    def initIndexWriter(self):
        fsDir = SimpleFSDirectory(Paths.get(self.indexPath))
        writerConfig = IndexWriterConfig(StandardAnalyzer())
        self.writer = IndexWriter(fsDir, writerConfig)


    def readFile(self):
        try:
            file = open(self.filePath, 'r')
            with file:
                self.processedLineCount = 1
                line = file.readline().strip()
                while line:
                    self.processLine(line)
                    self.processedLineCount += 1
                    self.showProgress()
                    line = file.readline().strip()
            file.close()
        except IOError:
            print('File ' + self.filePath + ' could not be opened!')


    def showProgress(self):
        if self.lineCount is None:
            return

        progress = int(self.processedLineCount / self.lineCount * 100)
        if progress > self.lastProgress:
            self.lastProgress = progress
            print('\rGenerating index  ...  %d%%' % self.lastProgress, end='')


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
