from rdflib import Literal, BNode, Namespace, URIRef, Graph, Dataset, RDF, RDFS, XSD
import rdflib.resource
from provmodified import Entity
import provmodified as prov

DOCKER = Namespace("http://www.example.org/ns/docker#")
PROV = Namespace("http://www.w3.org/ns/prov#")

ds = Dataset(default_union=True)
ds.bind("docker", DOCKER)
ds.bind("prov", PROV)
default_graph = ds

def bind_ns(prefix, namespace):
    ds.namespace_manager.bind(prefix, Namespace(namespace))

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

               
