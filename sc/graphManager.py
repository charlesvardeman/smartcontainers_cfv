import rdflib
from rdflib import RDF, Literal, URIRef
from rdflib.namespace import DC, FOAF

class graphManager:
	"""docstring for """
	def __init__(self):
		# initial graphManager
		self.graphdict = dict()

	def returnList(self):
		return self.graphdict

	def addGraph(self,graph):
		# add one sub-graph to the graph manager 
		name = "newtest"
		self.graphdict[name] = graph

	def deleteGraph(graph):
		name = "newtest"
		#delete one subgraph to the graph manager
		del self.graphdict[name]

	def updateGraph(graph):
		#update graph in the dictionary
		name = "newtest"
		self.update({name, graph})
