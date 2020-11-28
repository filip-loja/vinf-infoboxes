
from java.nio.file import Paths
from java.util import HashSet
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import IndexWriter, DirectoryReader
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher

class Searcher:
    indexPath = None
    reader = None
    indexSearcher = None
    analyzer = None
    query = None
    results = []
    maxHits = 1000

    fieldsToFetch = None
    fieldsToFetchSet = None


    def __init__(self, indexPath, query, maxHits):
        self.indexPath = indexPath
        self.query = query.get()
        self.fieldsToFetch = query.fieldsToFetch

        if maxHits is not None:
            self.maxHits = maxHits

        indexDirectory = SimpleFSDirectory(Paths.get(self.indexPath))
        self.reader = DirectoryReader.open(indexDirectory)
        self.indexSearcher = IndexSearcher(self.reader)
        self.analyzer = StandardAnalyzer()

        self.computeFieldSet()
        self.search()
        self.reader.close()


    def get(self):
        return self.results


    def computeFieldSet(self):
        self.fieldsToFetchSet = HashSet()
        for field in self.fieldsToFetch:
            self.fieldsToFetchSet.add(field)


    def search(self):
        hits = self.indexSearcher.search(self.query, self.maxHits)
        for hit in hits.scoreDocs:
            doc = self.indexSearcher.doc(hit.doc, self.fieldsToFetchSet)
            self.processDocument(doc)


    def processDocument(self, doc):
        record = {}
        for key in self.fieldsToFetch:
            value = doc.get(key) or None
            if value is not None:
                record[key] = value
        self.results.append(record)

