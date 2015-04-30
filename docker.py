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
    print cmd
    p = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    data = json.loads(stdout)
    return data[0]
    
def get_type(data):
    if "Container" in data.keys():
        return "Image"
    elif "Image" in data.keys(): 
        return "Container"
    else:
        return "NONE"

def get_id(data):
    if "Id" in data.keys():
        return data["Id"]
    else:
        return "NONE"
        
def get_container(data):
    if "Container" in data.keys():
        return data["Container"]
    else:
        return "NONE"
        
def get_image(data):
    if "Image" in data.keys():
        return data["Image"]
    else:
        return "NONE"

def get_parentImage(data):
    if "Parent" in data.keys():
        return data["Parent"]
    else:
        return "NONE"

def returnGraph():
    return default_graph

def serialize(format="xml", bundle=default_graph):
    if format == "json-ld":
        return bundle.serialize(format='json-ld', indent=4).decode()
    elif format == "nt":
        return bundle.serialize(format='nt').decode()
    else:
        return bundle.serialize(format=format, encoding="UTF-8").decode(encoding="UTF-8")

class Image(Entity):

        jsondata = []
        id = 0
        
        def __init__(self, id=None, bundle=default_graph):
                super(Image,self).__init__(id,bundle)
                self.add_type(DOCKER.Image)
                
        def __init__(self, arg, id=None, bundle=default_graph):
                super(Image, self).__init__(id, bundle)
                self.add_type(DOCKER.Image)
                jsondata = inspect_json(arg)
                id = get_id(jsondata)
                
                for key in jsondata.keys():
                        if key!="Parent":
                            #if jsondata[key] != "":
                                #self.set_was_derived_from(URIRef("test:"+jsondata[key]))
                            self.add(URIRef(DOCKER+key),Literal(jsondata[key]))
                        
        def set_was_derived_from(self,object):
                #object = DOCKER.Image(object)
                self.add(PROV.wasDerivedFrom, object)
                if isinstance(object, BNode):
                        return
                else:
                        object.add(PROV.hadDerivation, self)
                
        def check_by_id(inputid):
                if self.id == inputid:
                        return true  
                else:
                        return false            
                
               
