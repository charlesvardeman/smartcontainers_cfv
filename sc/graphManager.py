import rdflib
from rdflib import RDF, Literal, URIRef

class graphManager:
	"""docstring for """
	def __init__(self):
		# initial graphManager
		self.graphlist = dict()
		self.graphmeta = dict()

	def addGraph(self,graph):
		# add one sub-graph to the graph manager 
		name = graph.name
		self.graphlist[name] = graph
		self.graphmeta[name] = graph.metadata

	def deleteGraph(self,graph):
		name = graph.name
		#delete one subgraph to the graph manager
		del self.graphlist[name]
		del self.graphmeta[name]

	def Merge(self):
		graph = rdflib.ConjunctiveGraph()
		for each in self.graphlist:
			for eachtriple in each:
				graph.add(eachtriple)
				
