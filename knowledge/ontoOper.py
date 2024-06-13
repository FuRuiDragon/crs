from csv import DictReader
from itertools import groupby
from pprint import pprint
import json

import rdflib
from rdflib import Graph, URIRef, Literal, Namespace, RDF
from rdflib.plugins.sparql.results.jsonresults import JSONResultSerializer
from rdflib.query import Result, ResultException, ResultParser, ResultSerializer


# get caterorgy anc its concepts from domain Onto
def get_Ontoconcepts():
    g = rdflib.Graph()
    g.parse("data/origin/mergedOnto.ttl", format='turtle')

    results = g.query("""
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    
    SELECT  ?category ?concept
        WHERE { ?concept rdfs:subClassOf ?category }
    """).serialize(destination="data/concepts_de.csv", format="csv")

    return csv2json()


# save them as a json file
def csv2json():
    csv_File = 'data/concepts_de.csv'
    json_file = 'data/concept_de.json'

    text = open(csv_File, "r")
    text = ''.join([i for i in text]).replace("aiquiz:Studienbrief#", "").replace('_', " ")
    x = open(csv_File, "w")
    x.writelines(text)
    x.close()

    with open(csv_File) as csvfile:
        r = DictReader(csvfile, skipinitialspace=True)
        data = [dict(d) for d in r]

        groups = []
        uniquekeys = []

        for k, g in groupby(data, lambda r: (r['category'])):
            groups.append({
                "category": k,
                "concepts": [{k: v for k, v in d.items() if k not in ['category']} for d in list(g)]
            })
            uniquekeys.append(k)
    print('result!')
    pprint(groups)

    with open(json_file, 'w', encoding="utf-8") as jsonfile:
        jsonfile.write(json.dumps(groups, indent=4, ensure_ascii=False))
    return groups
