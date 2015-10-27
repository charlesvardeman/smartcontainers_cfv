__author__ = 'dahuo2013'

from rdflib import Literal, BNode, Namespace, URIRef, Graph, Dataset, RDF, RDFS, XSD
import rdflib.resource

ACT = Namespace("http://descartes-core.org/ontologies/activities/1.0/ActivityPattern#")

context = {"prov": "http://www.w3.org/ns/prov#",
           "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
           "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
           "xsd": "http://www.w3.org/2001/XMLSchema#"}

ds = Dataset(default_union=True)
ds.bind("act", ACT)
default_graph = ds

config = {
    "useInverseProperties": False
}


def set_use_inverse_properties(flag=False):
    config["useInverseProperties"] = flag


def using_inverse_properties():
    return config["useInverseProperties"]


def clear_graph(bundle=default_graph):
    bundle.remove((None, None, None))


def serialize(format="xml", bundle=default_graph):
    if format == "json-ld":
        return bundle.serialize(format='json-ld', context=context, indent=2).decode()
    elif format == "nt":
        return bundle.serialize(format='nt').decode()
    else:
        return bundle.serialize(format=format, encoding="UTF-8").decode(encoding="UTF-8")


def ns(prefix, namespace):
    ns_obj = Namespace(namespace)
    ds.namespace_manager.bind(prefix, ns_obj)
    return ns_obj


def _absolutize(uri):
    if ":" in uri:
        (prefix, qname) = uri.split(":")
        for (p, ns) in ds.namespace_manager.namespaces():
            if prefix == p:
                uri = ns + qname
                break
    return uri


def bundle_entity(bundle):
    if not isinstance(bundle, Graph):
        raise TypeError
    return Bundle(bundle.identifier)


def bundle(id):
    uri = URIRef(_absolutize(id))
    b = ds.graph(identifier=uri)
    Bundle(id=uri, bundle=b)
    return b


