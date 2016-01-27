from rdflib import Literal, BNode, Namespace, URIRef, Graph, Dataset, RDF, RDFS, XSD
from rdflib.namespace import FOAF
from rdflib.serializer import Serializer
import rdflib.resource
import uuid

# Create a default dataset graph.
ds = Dataset(default_union=True)

# JSON-LD serializer requires an explicit context.
# https://github.com/RDFLib/rdflib-jsonld
# context = {"@vocab": "http://purl.org/dc/terms/", "@language": "en"}

context = {"prov": "http://www.w3.org/ns/prov#",
           "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
           "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
           "xsd": "http://www.w3.org/2001/XMLSchema#",
           "dc": "http://purl.org/dc/terms"}

# Define some namespaces
PROV = Namespace("http://www.w3.org/ns/prov#")
ORE = Namespace("http://www.openarchives.org/ore/terms/")
OWL = Namespace("http://www.w3.org/2002/07/owl#")
DC = Namespace("http://purl.org/dc/terms/")
UUIDNS = Namespace("urn:uuid:")
# Need to handle DOI
# http://bitwacker.com/2010/02/04/dois-uris-and-cool-resolution/

ds.bind("prov", PROV)
default_graph = ds

# Generate URI's for docker instance
dockerEntityuuid = str(uuid.uuid4())
dockerEntityURI = rdflib.URIRef(UUIDNS.dockerEntityuuid)
dockerActivityuuid = str(uuid.uuid4())
dockerActivityURI = rdflib.URIRef(UUIDNS.dockerActvityuuid)

# Add entity triples first
ds.add( (UUIDNS[dockerEntityuuid], RDF.type, PROV.Entity) )
ds.add( (UUIDNS[dockerEntityuuid], PROV.wasGeneratedBy, UUIDNS[dockerActivityuuid]) )

# Add activity triples next


# Add agent info last.


# Add docker information objects.




# Main function just prints the graph right now for testing:
def main():
    print "--- start: turtle ---"
    print ds.serialize(format="turtle")
    print "--- end: turtle ---\n"
    print "-- start: json-ld ---"
    print ds.serialize(format='json-ld', context=context, indent=4)
    print "--- end: json-ld ---"

if __name__ == "__main__":
    main()
