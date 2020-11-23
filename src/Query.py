
import json

from java.lang import Integer, Double
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.search import PhraseQuery, FuzzyQuery, PrefixQuery, BooleanQuery, BooleanClause
from org.apache.lucene.index import Term
from org.apache.lucene.search.spans import SpanNearQuery, SpanMultiTermQueryWrapper
from org.apache.lucene.document import IntPoint, DoublePoint
from src.indexFields import fieldTypes

class Query:
    rawQuery = None
    parsedQuery = None
    analyzer = None

    fieldTypes = fieldTypes


    def __init__(self, queryFile):
        self.analyzer = StandardAnalyzer()

        with open(queryFile) as file:
            self.rawQuery = json.load(file)
        self.parse()


    def get(self):
        return self.parsedQuery


    def parse(self):
        if self.isGroup(self.rawQuery):
            self.parsedQuery = self.processGroup(self.rawQuery)
        else:
            self.parsedQuery = self.processRule(self.rawQuery)


    def isGroup(self, expression):
        return 'group' in expression


    def processGroup(self, group):
        conditions = group.get('conditions', None)
        groupType = group.get('group', 'and').lower()

        if conditions is None or len(conditions) == 0:
            raise ValueError('Conditions must not by empty!')

        for index, expression in enumerate(conditions):
            if self.isGroup(expression):
                conditions[index] = self.processGroup(expression)
            else:
                conditions[index] = self.processRule(expression)

        return self.transformGroup(groupType, conditions)


    def transformGroup(self, groupType, conditions):
        operator = BooleanClause.Occur.MUST if groupType == 'and' else BooleanClause.Occur.SHOULD
        builder = BooleanQuery.Builder()
        for condition in conditions:
            builder.add(condition, operator)
        return builder.build()


    def processRule(self, rule):
        field = rule.get('field')
        term = rule.get('term')

        if field is None or term is None:
            return None

        isPrefix = rule.get('prefix', False)
        isFuzzy = rule.get('fuzzy', False)

        isInt = field in ('id', 'population') and isinstance(term, list)
        isDouble = field in ('population_density', 'area_km2', 'elevation_m') and isinstance(term, list)

        if isInt:
            term1 = Integer.MIN_VALUE if term[0] == '-' else int(term[0])
            term2 = Integer.MAX_VALUE if term[1] == '-' else int(term[1])
            return IntPoint.newRangeQuery(field, term1, term2)

        if isDouble:
            term1 = Double.MIN_VALUE if term[0] == '-' else (term[0] * 1.00)
            term2 = Double.MAX_VALUE if term[1] == '-' else (term[1] * 1.00)
            return DoublePoint.newRangeQuery(field, term1, term2)

        term = str(term)

        if isPrefix:
            subTerms = term.split()
            if len(subTerms) > 1:
                queries = []
                for subTerm in subTerms:
                    queries.append(SpanMultiTermQueryWrapper(PrefixQuery(Term(field, subTerm))))
                # vsetky query musia byt matchnute a na poradi zalezi
                return SpanNearQuery(queries, 0, True)
            else:
                return PrefixQuery(Term(rule['field'], rule['term']))

        if isFuzzy:
            subTerms = term.split()
            if len(subTerms) > 1:
                queries = []
                for subTerm in subTerms:
                    queries.append(SpanMultiTermQueryWrapper(FuzzyQuery(Term(field, subTerm))))
                # vsetky query musia byt matchnute a na poradi zalezi
                return SpanNearQuery(queries, 0, True)
            else:
                return FuzzyQuery(Term(field, term))

        return QueryParser(field, self.analyzer).parse(term)
