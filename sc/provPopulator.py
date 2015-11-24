from kleio import prov
import rdflib
from rdflib import RDF, Literal, URIRef

class provPopulator(object):
	"provPopulator creates prov provenance from docker"
	def __init__(self):
		self.graph = prov

	def clearGraph(self):
		self.graph.clear_graph()

	def newNameSpace(self, shortname, longurl):
		self.graph.ns(shortname, longurl)

	def newImageEntity(self,id):
		return self.graph.Entity("urn:docker:"+id)

	def newContainerActivity(self,id):
		return self.graph.Activity("urn:docker:"+id)

	def newSoftwareAgent(self,name):
		return self.graph.SoftwareAgent(name)

	def newPerson(self,url):
		return self.graph.Person(url)

	def serialize(self,format):
		return self.graph.serialize(format=format)
		
	def newLabel(self, object, content):
		return object.set_label(content)

	def newEntity(self,entityid):
		return self.graph.Entity(entityid)

	def newActivity(self,activityid):
		return self.graph.Activity(activityid)
