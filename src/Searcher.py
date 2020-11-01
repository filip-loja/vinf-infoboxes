
from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import IndexWriter, DirectoryReader
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher
from src.indexFields import fieldTypes

class Searcher:
    fieldTypes = fieldTypes

    indexPath = None
    reader = None
    indexSearcher = None
    analyzer = None
    query = None
    results = []


    def __init__(self, indexPath, query):
        self.indexPath = indexPath
        self.query = query.get()

        indexDirectory = SimpleFSDirectory(Paths.get(self.indexPath))
        self.reader = DirectoryReader.open(indexDirectory)
        self.indexSearcher = IndexSearcher(self.reader)
        self.analyzer = StandardAnalyzer()

        self.search()
        self.reader.close()


    def get(self):
        return self.results


    def search(self):
        hits = self.indexSearcher.search(self.query, 1000)
        for hit in hits.scoreDocs:
            doc = self.indexSearcher.doc(hit.doc)
            self.processDocument(doc)


    def processDocument(self, doc):
        fieldKeys = self.fieldTypes.keys()
        record = {}
        for key in fieldKeys:
            value = doc.get(key) or None
            if value is not None:
                record[key] = value
        self.results.append(record)

