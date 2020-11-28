import lucene
import json

from src.cmdHelper import parseCmd
from src.Indexer import Indexer
from src.Searcher import Searcher
from src.Query import Query
from src.Printer import Printer

lucene.initVM()
config = parseCmd()

if config['moduleName'] == 'index':
    Indexer(config['sourceFile'], config['indexPath'])
elif config['moduleName'] == 'search':
    query = Query(config['queryFile'])
    searcher = Searcher(config['indexPath'], query, config['maxHits'])
    if config['printOutput']:
        Printer(searcher, query.fieldsToFetch)
    if config['outputFile'] is not None:
        with open(config['outputFile'], 'w+') as outputFile:
            json.dump(searcher.get(), outputFile, indent=2)
            print('Search results saved to "' + config['outputFile'] +'" file.')
    else:
        print('Output file not specified! Search results were not saved.')
