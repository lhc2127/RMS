
"""Module to handle the routes.

Author: Nick Machairas, 2022
"""


from os import minor
from flask import render_template
from app import app
from app.forms import SearchForm
from elasticsearch import Elasticsearch
from pymongo import MongoClient

# establish elasticsearch connection
es_connection = Elasticsearch(hosts=["localhost"],
                     port=9200, 
                     http_auth=('elastic', '23Watten!'),  
                     ca_certs='/Users/leannecheng/Documents/Spring 2022/5400 Managing Data/Assignment 4 ElasticSearch or Neo4j/http_ca.crt', #put full path 
                     use_ssl=True, 
                     verify_certs=True)

# establish pymongo connection 
from pymongo import MongoClient
client = MongoClient('localhost',27017) 
db = client.apan5400

# queries 
@app.route('/', methods=['GET', 'POST'])
def home():
    """Render the home page."""
    form = SearchForm()
    search_results = None
    if form.validate_on_submit():
        location = form.location.data
        diagnosis = form.diagnosis.data
        severity = form.severity.data
        index_name = "facilities" 

        resp = es_connection.search(index=index_name, query={
            "bool": {
                "must": [
                    {
                        "match": {
                            "Diagnosis_Description": diagnosis
                        }
                    },
                    {
                        "match": {
                            "Severity_Description": severity
                        }
                    },
                ],
                "should": [
                    {
                        "match": {
                             "Facility_City": location
                        }
                    },
                    {
                        "match": {
                             "Facility_Name_x": location
                        }
                    }
                ]
            }
        })
        
        hits = resp["hits"]["hits"]
        ids = []
        for hit in hits:
            ids.append(hit["_source"]["id"])

        query = {
            "id":{"$in":ids}
        }

#        query = {
#            "$and": [
#                {"id": {"$in": ids}},
#                {"year": 2017} # will only return one result because other facilities did not publish cost for every year
#    ]
#}

        search_results = db.collection.find(query, sort=[("MeanCost", -1)])
    return render_template(
        "home.html", form=form, search_results=search_results) #returns results in home.html file 



