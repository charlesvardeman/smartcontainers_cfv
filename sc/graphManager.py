import rdflib
from rdflib import RDF, Literal, URIRef

class graphPluginRegistry(type):
    plugins = []
    global_graph = rdflib.ConjunctiveGraph()
    def __init__(cls, name, bases, attrs):
        if name != 'graphPlugin':
            graphPluginRegistry.plugins.append(cls)

class graphPlugin(object, metaclass=GraphPluginRegistry):
    def __init__(self, post=None, db=None):
        """ Initialize the plugin. Optinally provide the db.Post that is
            being processed and the db.DB it belongs to.
        """
        self.post = post
        self.db = db



class graphPlugin:
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
				
