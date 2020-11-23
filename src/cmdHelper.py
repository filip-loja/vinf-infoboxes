
import os
import sys
import json

modules = ('indexer', 'searcher')


def getCmdArg(index, default):
    try:
        return sys.argv[index + 1]
    except IndexError:
        return default


def parseCmd():
    moduleNames = ', '.join(modules)

    moduleName = getCmdArg(0, None)
    configPath = getCmdArg(1, 'config.json')

    if moduleName is None:
        raise Exception('Module name not specified! The following modules are allowed: ' + moduleNames)

    if moduleName not in modules:
        raise Exception('Unknown module name! The following modules are allowed: ' + moduleNames)

    with open(os.path.abspath(configPath)) as file:
        config = json.load(file)

    if config.get('indexPath', None) is None:
        raise Exception('Path to index folder is not set!')

    if config.get('queryFile') is None:
        raise Exception('Path to query file is not set!')

    config['moduleName'] = moduleName

    return config
