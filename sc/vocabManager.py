import rdflib.resource

class VocabPluginRegistry(type):
    plugins = []
    def __init__(cls, name, bases, attrs):
        if name != 'IPlugin':
            IPluginRegistry.plugins.append(cls)

class VocabPlugin(object, metaclass=IPluginRegistry):
    def __init__(self, post=None, db=None):
        """ Initialize the plugin. Optinally provide the db.Post that is
            being processed and the db.DB it belongs to.
        """
        self.post = post
        self.db = db

    """ Plugin classes inherit from IPlugin. The methods below can be
        implemented to provide services.
    """
    def get_role_hook(self, role_name):
        """ Return a function accepting role contents.
            The function will be called with a single argument - the role
            contents, and should return what the role gets replaced with.
            None if the plugin doesn't provide a hook for this role.
        """
        return None


