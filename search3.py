from whoosh import index
from whoosh.fields import Schema, TEXT, ID
from whoosh import index
import os, os.path
from whoosh import index
from whoosh import qparser
from whoosh.qparser import QueryParser
import sys
import configparser

def index_search(dirname, search_fields, search_query,numResults):
    ix = index.open_dir(dirname)
    schema = ix.schema
    numOutput = int(numResults)
    
    og = qparser.OrGroup.factory(0.9)
    mp = qparser.MultifieldParser(search_fields, schema, group = og)

    
    q = mp.parse(search_query)
    
    
    with ix.searcher() as s:
        results = s.search(q, terms=True, limit = 10)
        print("Search Results: ")
        # print(results[])
        for i in range(int(numResults)):
            docwithpath = results[i]['path']
            textcontent = results[i]['textdata']
            print(docwithpath,"\n",textcontent)
            
        
        # print(results[0:10])
        # docwithpath = results[0]['path']
        # textcontent = results[0]['textdata']
        # print(docwithpath,"\n",textcontent)
        
config = configparser.RawConfigParser()
config.read('config.properties')
myQuery = config.get('ParameterSearch','myQuery')
indexdir = config.get('ParameterSearch','indexdir')
numResults = config.get('ParameterSearch','numResults')
    
results_dict = index_search(indexdir, ['title','content'], myQuery, numResults)


