#!/usr/bin/python
from rdflib import Literal, BNode, Namespace, URIRef, Graph, Dataset, RDF, RDFS, XSD
import rdflib.resource
from provmodified import Entity
import provmodified as prov
import json
import subprocess, shlex
import collections

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
    #print cmd
    p = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    data = json.loads(stdout)
    return data[0]
    
def create_container(cmd):
    #print cmd
    p = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    return stdout

def run(cmd):
    #print cmd
    p = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    return stdout
    
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
        
def get_parentid(id):
    data = inspect_json("docker inspect "+str(id))
    get_parentImage(data)

def returnGraph():
    return default_graph
    
def convert(data):
    if isinstance(data, basestring):
        return str(data)
    elif isinstance(data, collections.Mapping):
        return dict(map(convert, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convert, data))
    else:
        return data

def serialize(format="xml", bundle=default_graph):
    if format == "json-ld":
        return bundle.serialize(format='json-ld', indent=0).decode()
    elif format == "nt":
        return bundle.serialize(format='nt').decode()
    else:
        return bundle.serialize(format=format, encoding="UTF-8").decode(encoding="UTF-8")

class Image(Entity):

        parent = ""
        container = ""
                
        # Image object initialization         
        def __init__(self, id, bundle=default_graph):
        
                super(Image, self).__init__("urn:sc:"+str(id)+"#image", bundle)
                self.add_type(DOCKER.Image)
                          
                jsondata = inspect_json("docker inspect "+str(id))
                print jsondata
                selfid = get_id(jsondata)
                self.add(URIRef(DOCKER+"id"), Literal(selfid))
                
                for key in jsondata.keys():
                        if key =="Parent":
                            content = str(jsondata[key])
                            print content
                            self.parent = content
                            print self.parent
                        elif key == "Container":
                            content = str(jsondata[key])
                            print content
                            self.container = content
                            print self.container
                        else:
                            continue
                        
        def set_parent(self,parentobject):
                self.add(DOCKER.hasParent, parentobject)
                if isinstance(object, BNode):
                        return
                else:
                        parentobject.add(DOCKER.hasChild, self)
                        
        def set_was_derived_from(self,object):
                self.add(PROV.wasDerivedFrom, object)
                if isinstance(object, BNode):
                        return
                else:
                        object.add(PROV.hadDerivation, self)
                        
class Container(Entity):

        image = ""
                
        # Image object initialization         
        def __init__(self, id, bundle=default_graph):
        
                super(Container, self).__init__("urn:sc:"+str(id), bundle)
                self.add_type(DOCKER.Container)
                          
                jsondata = inspect_json("docker inspect "+str(id))
                print jsondata
                selfid = get_id(jsondata)
                self.add(URIRef(DOCKER+"id"), Literal(selfid))
                
                for key in jsondata.keys():
                        if key =="Image":
                            content = str(jsondata[key])
                            print content
                            self.image = content
                            print self.image
                        else:
                            continue
                        
        def set_was_derived_from(self,object):
                self.add(PROV.wasDerivedFrom, object)
                if isinstance(object, BNode):
                        return
                else:
                        object.add(PROV.hadDerivation, self)
                           

