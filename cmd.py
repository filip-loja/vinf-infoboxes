import lucene

from src.CmdHandler import CmdHandler
from src.Indexer import Indexer
from src.Searcher import Searcher
from src.Query import Query
from src.Printer import Printer

lucene.initVM()
moduleName = CmdHandler().getModule()

indexFolder = './index/'
indexInputFile = './data/infobox.txt'
queryInputFile = './data/query.json'

if moduleName == 'indexer':
    Indexer(indexInputFile, indexFolder)
elif moduleName == 'searcher':
    query = Query(queryInputFile)
    searcher = Searcher(indexFolder, query)
    Printer(searcher)
