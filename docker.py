#!/usr/bin/python
from rdflib import Literal, BNode, Namespace, URIRef, Graph, Dataset, RDF, RDFS, XSD
import rdflib.resource
from provmodified import Entity
import provmodified as prov
import json
import subprocess, shlex

DOCKER = Namespace("http://www.example.org/ns/docker#")
PROV = Namespace("http://www.w3.org/ns/prov#")

ds = Dataset(default_union=True)
ds.bind("docker", DOCKER)
ds.bind("prov", PROV)
default_graph = ds

def bind_ns(prefix, namespace):
    ds.namespace_manager.bind(prefix, Namespace(namespace))
    
def parse_json_byfile(filename):
    with open(filename) as data_file:    
        data = json.load(data_file)
    return data[0]

def inspect_json(cmd):
    p = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    data = json.loads(stdout)
    return data[0]

def serialize(format="xml", bundle=default_graph):
    if format == "json-ld":
        return bundle.serialize(format='json-ld', indent=4).decode()
    elif format == "nt":
        return bundle.serialize(format='nt').decode()
    else:
        return bundle.serialize(format=format, encoding="UTF-8").decode(encoding="UTF-8")

class Image(Entity):
        def __init__(self, id=None, bundle=default_graph):
                super(Image,self).__init__(id,bundle)
                self.add_type(DOCKER.Image)
                
        def __init__(self, arg, id=None, bundle=default_graph):
                super(Image, self).__init__(id, bundle)
                self.add_type(DOCKER.Image)
                jsondata = inspect_json(arg)
                #print jsondata
                #jsondata = parse_json_byfile(filename)
                #print type(DOCKER.Comment)
                #print DOCKER.Comment
                for key in jsondata.keys():
                        #print key
                        #print jsondata[key]
                        self.add(URIRef(DOCKER+key),Literal(jsondata[key]))  
