from rdflib import Literal, BNode, Namespace, URIRef, Graph, Dataset, RDF, RDFS, XSD
import rdflib.resource

"""
@newfield iri: IRI
"""

PROV = Namespace("http://www.w3.org/ns/prov#")

ds = Dataset(default_union=True)
ds.bind("prov", PROV)
default_graph = ds
#print type(default_graph)


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
        return bundle.serialize(format='json-ld', indent=4).decode()
    elif format == "nt":
        return bundle.serialize(format='nt').decode()
    else:
        return bundle.serialize(format=format, encoding="UTF-8").decode(encoding="UTF-8")


def bind_ns(prefix, namespace):
    ds.namespace_manager.bind(prefix, Namespace(namespace))
    #for each in ds.namespace_manager.namespaces():
    #    print each


def _absolutize(uri):
    if ":" in uri:
        (prefix, qname) = uri.split(":")
        for (p, ns) in ds.namespace_manager.namespaces():
            if prefix == p:
                uri = ns+qname
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


class Resource(rdflib.resource.Resource):

    def __init__(self, id=None, bundle=default_graph):
        if id is None:
            super(Resource,self).__init__(bundle, BNode())
        else:
            print id
            super(Resource,self).__init__(bundle, URIRef(id))

    @classmethod
    def ensure_type(cls, resource):
        """
        Ensure that resource is of python type 'cls'
        """
        if not isinstance(resource, cls):
            return cls(resource)
        else:
            return resource

    def get_resources(self, clz, prop):
        """
        Return a list of values of the property 'prop' as objects of type 'clz'.
        """
        return [clz.ensure_type(resource) for resource in self.graph.objects(self.identifier, prop)]

    def get_literals(self, prop):
        """
        Return a list of values of the property 'prop' as python native literals.
        """
        return [literal.toPython() for literal in self.graph.objects(self.identifier, prop)]

    def set_label(self, label):
        """
        Set RDF label of resource
        """
        self.add(RDFS.label, Literal(label))

    def get_label(self):
        """
        Return RDFS label of resource
        """
        return self.get_literals(RDFS.label)

    def add_type(self, rdf_type):
        """
        Add RDF type of resource
        """
        self.add(RDF.type, rdf_type)


'''class Bundle(Entity):
    """
    A bundle is a named set of provenance descriptions, and is itself an Entity, so allowing provenance of provenance
    to be expressed.
    @iri: http://www.w3.org/ns/prov#Bundle
    @see: http://www.w3.org/TR/prov-o/#Bundle
    """

    def __init__(self, id=None, bundle=default_graph):
        Entity().__init__(id=id, bundle=bundle)
        self.add_type(PROV.Bundle)


class Collection(Entity):
    """
    A collection is an entity that provides a structure to some constituents, which are themselves entities. These
    constituents are said to be member of the collections.
    @iri: http://www.w3.org/ns/prov#Collection
    @see: http://www.w3.org/TR/prov-o/#Collection
    """

    def __init__(self, id=None, bundle=default_graph):
        Entity().__init__(id=id, bundle=bundle)
        self.add_type(PROV.Collection)

    def set_had_member(self, entity):
        """
        Specify a member entity of this collection.
        @iri: http://www.w3.org/ns/prov#hadMember
        """
        entity = Entity.ensure_type(entity)
        self.set_was_influenced_by(entity)
        self.add(PROV.hadMember, entity)
        if using_inverse_properties():
            entity.add(PROV.wasMemberOf, self)

    def get_had_member(self):
        """
        Return all entities that were members of this collection.
        @iri: http://www.w3.org/ns/prov#hadMember
        """
        return self.get_resources(Entity, PROV.hadMember)

    def get_member_count(self):
        """
        Return a count of the members in this collection.
        """
        return len(self.graph.objects(self.identifier, PROV.hadMember))


class EmptyCollection(Collection):
    """
    An empty collection is a collection without members.
    @iri: http://www.w3.org/ns/prov#EmptyCollection
    @see: http://www.w3.org/TR/prov-o/#EmptyCollection
    """

    def __init__(self, id=None, bundle=default_graph):
        Collection().__init__(id=id, bundle=bundle)
        self.add_type(PROV.EmptyCollection)

    def set_had_member(self, entity):
        """
        do nothing (no members allowed for an empty collection)
        """
        pass

    def get_had_member(self):
        """
        Return an empty list
        """
        return []


class Plan(Entity):
    """
    A plan is an entity that represents a set of actions or steps intended by one or more agents to achieve some goals.
    @iri: http://www.w3.org/ns/prov#Plan
    @see: http://www.w3.org/TR/prov-o/#Plan
    """

    def __init__(self, id=None, bundle=default_graph):
        Entity().__init__(id=id, bundle=bundle)
        self.add_type(PROV.Plan)


class Location(Resource):
    """
    A location can be an identifiable geographic place (ISO 19112), but it can also be a non-geographic place such as a
    directory, row, or column. As such, there are numerous ways in which location can be expressed, such as by a
    coordinate, address, landmark, and so forth.
    @iri: http://www.w3.org/ns/prov#Location
    @see: http://www.w3.org/TR/prov-o/#Location
    """

    def __init__(self, id=None, bundle=default_graph):
        Resource().__init__(id=id, bundle=bundle)
        self.add_type(PROV.Location)
'''
'''
class Agent(Resource):
    """
    An agent is something that bears some form of responsibility for an activity taking place, for the existence of an
    entity, or for another agent's activity.
    @iri: http://www.w3.org/ns/prov#Agent
    @see: http://www.w3.org/TR/prov-o/#Agent
    """

    def __init__(self, id=None, bundle=default_graph):
        Resource().__init__(id=id, bundle=bundle)
        self.add_type(PROV.Agent)

    def set_was_influenced_by(self, resource):
        """
        Specify a resource that influenced this agent.
        @iri: http://www.w3.org/ns/prov#wasInfluencedBy
        """
        self.add(PROV.wasInfluencedBy, resource)

    def get_was_influenced_by(self):
        """
        Return all resources that influenced this agent.
        @iri: http://www.w3.org/ns/prov#wasInfluencedBy
        """
        return self.get_resources(Resource, PROV.wasInfluencedBy)

    def set_acted_on_behalf_of(self, agent):
        """
        Specify an agent that this agent acted on behalf of (i.e. was delegate for).
        @iri: http://www.w3.org/ns/prov#actedOnBehalfOf
        """
        agent = Agent.ensure_type(agent)
        self.set_was_influenced_by(agent)
        self.add(PROV.actedOnBehalfOf, agent)
        if using_inverse_properties():
            agent.add(PROV.hadDelegate, self)

    def get_acted_on_behalf_of(self):
        """
        Return all agents this agent has acted on behalf of.
        @iri: http://www.w3.org/ns/prov#actedOnBehalfOf
        """
        return self.get_resources(Agent, PROV.actedOnBehalfOf)

    def delegation(self, agent, id=None, role=None):
        """
        Specify an agent that this agent acted on behalf of (i.e. was delegate for).
        Return delegation relationship which can be used to further qualify the relationship.
        @iri: http://www.w3.org/ns/prov#qualifiedDelegation
        """
        delegation = Delegation(id)
        delegation.set_agent(agent)
        if role is not None:
            delegation.set_had_role(role)
        self.add(PROV.qualifiedDelegation, delegation)
        if using_inverse_properties():
            delegation.add(PROV.qualifiedDelegationOf, self)
        self.set_acted_on_behalf_of(agent)
        return delegation

    def get_delegation(self):
        """
        Return all delegation relationships for this agent.
        @iri: http://www.w3.org/ns/prov#qualifiedDelegation
        """
        return self.get_resources(Delegation, PROV.qualifiedDelegation)

    def set_at_location(self, location):
        """
        Specify a location for this agent.
        @iri: http://www.w3.org/ns/prov#atLocation
        """
        location = Location.ensure_type(location)
        self.add(PROV.atLocation, location)
        if using_inverse_properties():
            location.add(PROV.locationOf, self)

    def get_at_location(self):
        """
        Return all locations for this agent.
        @iri: http://www.w3.org/ns/prov#atLocation
        """
        return self.get_resources(Location, PROV.atLocation)


class Person(Agent):
    """
    Person agents are people.
    @iri: http://www.w3.org/ns/prov#Person
    @see: http://www.w3.org/TR/prov-o/#Person
    """

    def __init__(self, id=None, bundle=default_graph):
        Agent().__init__(id=id, bundle=bundle)
        self.add_type(PROV.Person)


class Organization(Agent):
    """
    An organization is a social or legal institution such as a company, society, etc.
    @iri: http://www.w3.org/ns/prov#Organization
    @see: http://www.w3.org/ns/prov#Organization
    """

    def __init__(self, id=None, bundle=default_graph):
        Agent().__init__(id=id, bundle=bundle)
        self.add_type(PROV.Organization)


class SoftwareAgent(Agent):
    """
    A software agent is running software.
    @iri: http://www.w3.org/ns/prov#SoftwareAgent
    @see: http://www.w3.org/TR/prov-o/#SoftwareAgent
    """

    def __init__(self, id=None, bundle=default_graph):
        Agent().__init__(id=id, bundle=bundle)
        self.add_type(PROV.SoftwareAgent)


class InstantaneousEvent(Resource):
    """
    The PROV data model is implicitly based on a notion of instantaneous events (or just events), that mark transitions
    in the world. Events include generation, usage, or invalidation of entities, as well as starting or ending of
    activities. This notion of event is not first-class in the data model, but it is useful for explaining its other
    concepts and its semantics.
    @iri: http://www.w3.org/ns/prov#InstantaneousEvent
    @see: http://www.w3.org/TR/prov-o/#InstantaneousEvent
    """

    def __init__(self, id=None, bundle=default_graph):
        Resource().__init__(id=id, bundle=bundle)
        self.add_type(PROV.InstantaneousEvent)

    def set_at_location(self, location):
        """
        Specify a location for this event.
        @iri: http://www.w3.org/ns/prov#atLocation
        """
        location = Location.ensure_type(location)
        self.add(PROV.atLocation, location)
        if using_inverse_properties():
            location.add(PROV.locationOf, self)

    def get_at_location(self):
        """
        Return all locations for this event.
        @iri: http://www.w3.org/ns/prov#atLocation
        """
        return self.get_resources(Location, PROV.atLocation)

    def set_at_time(self, datetime):
        """
        Specify a datetime for this event.
        @iri: http://www.w3.org/ns/prov#atTime
        """
        self.add(PROV.atTime, Literal(datetime, datatype=XSD.dateTime))

    def get_at_time(self):
        """
        Return the datetime for this event.
        @iri: http://www.w3.org/ns/prov#atTime
        """
        return Literal(self.value(PROV.atTime), datatype=XSD.dateTime).toPython()

    def set_had_role(self, role):
        """
        specify the role associated with this event.
        @iri: http://www.w3.org/ns/prov#hadRole
        """
        role = Role.ensure_type(role)
        self.add(PROV.hadRole, role)

    def get_had_role(self):
        """
        Return all roles associated with this event.
        @iri: http://www.w3.org/ns/prov#hadRole
        """
        return self.get_resources(Role, PROV.hadRole)


class Influence(Resource):
    """
    Influence is the capacity of an entity, activity, or agent to have an effect on the character, development, or
    behavior of another by means of usage, start, end, generation, invalidation, communication, derivation,
    attribution, association, or delegation.
    @iri: http://www.w3.org/ns/prov#Influence
    @see: http://www.w3.org/TR/prov-o/#Influence
    """

    def __init__(self, id=None, bundle=default_graph):
        Resource().__init__(id=id, bundle=bundle)
        self.add_type(PROV.Influence)

    def set_had_role(self, role):
        """
        Specify the role associated with this influence.
        @iri: http://www.w3.org/ns/prov#hadRole
        """
        role = Role.ensure_type(role)
        self.add(PROV.hadRole, role)

    def get_had_role(self):
        """
        Return all roles associated with this influence.
        @iri: http://www.w3.org/ns/prov#hadRole
        """
        return self.get_resources(Role, PROV.hadRole)

    def set_had_activity(self, activity):
        """
        Specify the *optional* activity of this influence, which used, generated, invalidated,
        or was the responsibility of some entity.
        @iri: @iri: http://www.w3.org/ns/prov#hadActivity
        """
        activity = Activity.ensure_type(activity)
        self.add(PROV.hadActivity, activity)

    def get_had_activity(self):
        """
        Return the activity of this influence which used, generated, invalidated,
        or was the responsibility of some entity.
        @iri: @iri: http://www.w3.org/ns/prov#hadActivity
        """
        return self.get_resources(Activity, PROV.hadActivity)


class ActivityInfluence(Influence):
    """
    ActivityInfluence is the capacity of an activity to have an effect on the character, development, or behavior of
    another by means of generation, invalidation, communication, or other.
    @iri: http://www.w3.org/ns/prov#ActivityInfluence
    @see: http://www.w3.org/TR/prov-o/#ActivityInfluence
    """

    def __init__(self, id=None, bundle=default_graph):
        Influence().__init__(id=id, bundle=bundle)

    def set_activity(self, activity):
        """
        Specify the activity that had an effect on the character, development, or behavior of another by means of
        generation, invalidation, communication, or other.
        @iri: http://www.w3.org/ns/prov#activity
        """
        activity = Activity.ensure_type(activity)
        self.add(PROV.activity, activity)
        self.add(PROV.influencer, activity)

    def get_activity(self):
        """
        Return the activity that had an effect on the character, development, or behavior of another by means of
        generation, invalidation, communication, or other.
        @iri: http://www.w3.org/ns/prov#activity
        """
        return self.get_resources(Activity, PROV.activity)


class AgentInfluence(Influence):
    """
    AgentInfluence is the capacity of an agent to have an effect on the character, development, or behavior of another
    by means of attribution, association, delegation, or other.
    @iri: http://www.w3.org/ns/prov#AgentInfluence
    @see: http://www.w3.org/TR/prov-o/#AgentInfluence
    """

    def __init__(self, id=None, bundle=default_graph):
        Influence().__init__(id=id, bundle=bundle)

    def set_agent(self, agent):
        """
        Specify the agent that had an effect on the character, development, or behavior of another by means
        of attribution, association, delegation, or other.
        @iri: http://www.w3.org/ns/prov#agent
        """
        agent = Agent.ensure_type(agent)
        self.add(PROV.agent, agent)
        self.add(PROV.influencer, agent)

    def get_agent(self):
        """
        Return the agent that had an effect on the character, development, or behavior of another by means
        of attribution, association, delegation, or other.
        @iri: http://www.w3.org/ns/prov#agent
        """
        return self.get_resources(Agent, PROV.agent)


class EntityInfluence(Influence):
    """
    EntityInfluence is the capacity of an entity to have an effect on the character, development, or behavior of
    another by means of usage, start, end, derivation, or other.
    @iri: http://www.w3.org/ns/prov#EntityInfluence
    @see: http://www.w3.org/TR/prov-o/#EntityInfluence
    """

    def __init__(self, id=None, bundle=default_graph):
        Influence().__init__(id, bundle=bundle)

    def set_entity(self, entity):
        """
        Specify the entity that had an effect on the character, development, or behavior of another
        by means of usage, start, end, derivation, or other.
        @iri: http://www.w3.org/ns/prov#entity
        """
        entity = Entity.ensure_type(entity)
        self.add(PROV.entity, entity)
        self.add(PROV.influencer, entity)

    def get_entity(self):
        """
        Return the entity that had an effect on the character, development, or behavior of another
        by means of usage, start, end, derivation, or other.
        @iri: http://www.w3.org/ns/prov#entity
        """
        self.get_resources(Entity, PROV.entity)


class Generation(InstantaneousEvent, ActivityInfluence):
    """
    Generation is the completion of production of a new entity by an activity. This entity did not exist before
    generation and becomes available for usage after this generation.
    @iri: http://www.w3.org/ns/prov#Generation
    @see: http://www.w3.org/TR/prov-o/#Generation
    """

    def __init__(self, id=None, bundle=default_graph):
        InstaneousEvent.__init__(id=id, bundle=bundle)
        self.add_type(PROV.Generation)


class Start(InstantaneousEvent, EntityInfluence):
    """
    Start is when an activity is deemed to have been started by an entity, known as trigger. The activity did not exist
    before its start. Any usage, generation, or invalidation involving an activity follows the activity's start. A
    start may refer to a trigger entity that set off the activity, or to an activity, known as starter, that generated
    the trigger.
    @iri: http://www.w3.org/ns/prov#Start
    @see: http://www.w3.org/TR/prov-o/#Start
    """

    def __init__(self, id=None, bundle=default_graph):
        InstaneousEvent.__init__(id, bundle=bundle)
        self.add_type(PROV.Start)


class End(InstantaneousEvent, EntityInfluence):
    """
    End is when an activity is deemed to have been ended by an entity, known as trigger. The activity no longer exists
    after its end. Any usage, generation, or invalidation involving an activity precedes the activity's end. An end may
    refer to a trigger entity that terminated the activity, or to an activity, known as ender that generated the
    trigger.
    @iri: http://www.w3.org/ns/prov#End
    @see: http://www.w3.org/TR/prov-o/#End
    """

    def __init__(self, id=None, bundle=default_graph):
        InstaneousEvent.__init__(id=id, bundle=bundle)
        self.add_type(PROV.End)


class Invalidation(InstantaneousEvent, ActivityInfluence):
    """
    Invalidation is the start of the destruction, cessation, or expiry of an existing entity by an activity. The entity
    is no longer available for use (or further invalidation) after invalidation. Any generation or usage of an entity
    precedes its invalidation.
    @iri: http://www.w3.org/ns/prov#Invalidation
    @see: http://www.w3.org/TR/prov-o/#Invalidation
    """

    def __init__(self, id=None, bundle=default_graph):
        InstantaneousEvent.__init__(id=id, bundle=bundle)
        self.add_type(PROV.Invalidation)


class Communication(ActivityInfluence):
    """
    Communication is the exchange of an entity by two activities, one activity using the entity generated by the other.
    @iri: http://www.w3.org/ns/prov#Communication
    @see: http://www.w3.org/TR/prov-o/#Communication
    """

    def __init__(self, id=None, bundle=default_graph):
        ActivityInfluence.__init__(id=id, bundle=bundle)
        self.add_type(PROV.Communication)


class Usage(InstantaneousEvent, EntityInfluence):
    """
    Usage is the beginning of utilizing an entity by an activity. Before usage, the activity had not begun to utilize
    this entity and could not have been affected by the entity.
    @iri: http://www.w3.org/ns/prov#Usage
    @see: http://www.w3.org/TR/prov-o/#Usage
    """

    def __init__(self, id=None, bundle=default_graph):
        InstantaneousEvent.__init__(id=id, bundle=bundle)
        self.add_type(PROV.Usage)


class Derivation(EntityInfluence):
    """
    A derivation is a transformation of an entity into another, an update of an entity resulting in a new one, or the
    construction of a new entity based on a pre-existing entity.
    @iri: http://www.w3.org/ns/prov#Derivation
    @see: http://www.w3.org/TR/prov-o/#Derivation
    """

    def __init__(self, id=None, bundle=default_graph):
        EntityInfluence.__init__(id=id, bundle=bundle)
        self.add_type(PROV.Derivation)

    def set_had_usage(self, usage):
        """
        Specify the *optional* usage involved in an entity's derivation.
        @iri: http://www.w3.org/ns/prov#hadUsage
        """
        usage = Usage.ensure_type(usage)
        self.add(PROV.hadUsage, usage)

    def get_had_usage(self):
        """
        Return all usages involved in an entity's derivation.
        @iri: http://www.w3.org/ns/prov#hadUsage
        """
        return self.get_resources(Usage, PROV.hadUsage)

    def set_had_generation(self, generation):
        """
        Specify the *optional* generation involved in an entity's derivation.
        @iri: http://www.w3.org/ns/prov#hadGeneration
        """
        generation = Generation.ensure_type(generation)
        self.add(PROV.hadGeneration, generation)

    def get_had_generation(self):
        """
        Return all generations involved in an entity's derivation.
        @iri: http://www.w3.org/ns/prov#hadGeneration
        """
        return self.get_resources(Generation, PROV.hadGeneration)


class Revision(Derivation):
    """
    A revision is a derivation for which the resulting entity is a revised version of some original. The implication
    here is that the resulting entity contains substantial content from the original. Revision is a particular case of
    derivation.
    @iri: http://www.w3.org/ns/prov#Revision
    @see: http://www.w3.org/TR/prov-o/#Revision
    """

    def __init__(self, id=None, bundle=default_graph):
        Derivation.__init__(id=id, bundle=bundle)
        self.add_type(PROV.Revision)


class PrimarySource(Derivation):
    """
    A primary source for a topic refers to something produced by some agent with direct experience and knowledge about
    the topic, at the time of the topic's study, without benefit from hindsight. Because of the directness of primary
    sources, they 'speak for themselves' in ways that cannot be captured through the filter of secondary sources. As
    such, it is important for secondary sources to reference those primary sources from which they were derived, so
    that their reliability can be investigated. A primary source relation is a particular case of derivation of
    secondary materials from their primary sources. It is recognized that the determination of primary sources can be
    up to interpretation, and should be done according to conventions accepted within the application's domain.
    @iri: http://www.w3.org/ns/prov#PrimarySource
    @see: http://www.w3.org/TR/prov-o/#PrimarySource
    """

    def __init__(self, id=None, bundle=default_graph):
        Derivation.__init__(id=id, bundle=bundle)
        self.add_type(PROV.PrimarySource)


class Quotation(Derivation):
    """
    A quotation is the repeat of (some or all of) an entity, such as text or image, by someone who may or may not be
    its original author. Quotation is a particular case of derivation.
    @iri: http://www.w3.org/ns/prov#Quotation
    @see: http://www.w3.org/TR/prov-o/#Quotation
    """

    def __init__(self, id=None, bundle=default_graph):
        Derivation.__init__(id=id, bundle=bundle)
        self.add_type(PROV.Quotation)


class Delegation(AgentInfluence):
    """
    Delegation is the assignment of authority and responsibility to an agent (by itself or by another agent) to carry
    out a specific activity as a delegate or representative, while the agent it acts on behalf of retains some
    responsibility for the outcome of the delegated work. For example, a student acted on behalf of his supervisor, who
    acted on behalf of the department chair, who acted on behalf of the university; all those agents are responsible in
    some way for the activity that took place but we do not say explicitly who bears responsibility and to what degree.
    @iri: http://www.w3.org/ns/prov#Delegation
    @see: http://www.w3.org/TR/prov-o/#Delegation
    """

    def __init__(self, id=None, bundle=default_graph):
        AgentInfluence.__init__(id=id, bundle=bundle)
        self.add_type(PROV.Delegation)


class Association(AgentInfluence):
    """
    An activity association is an assignment of responsibility to an agent for an activity, indicating that the agent
    had a role in the activity. It further allows for a plan to be specified, which is the plan intended by the agent
    to achieve some goals in the context of this activity.
    @iri: http://www.w3.org/ns/prov#Association
    @see: http://www.w3.org/TR/prov-o/#Association
    """

    def __init__(self, id=None, bundle=default_graph):
        AgentInfluence.__init__(id=id, bundle=bundle)
        self.add_type(PROV.Association)

    def set_had_plan(self, plan):
        """
        Specify the plan used by the agent in the context of the activity association.
        @iri: http://www.w3.org/ns/prov#hadPlan
        """
        plan = Plan.ensure_type(plan)
        self.add(PROV.hadPlan, plan)
        if using_inverse_properties():
            plan.add(PROV.wasPlanOf, self)

    def get_had_plan(self):
        """
        Return the plan used by the agent in the context of the activity association.
        @iri: http://www.w3.org/ns/prov#hadPlan
        """
        return self.get_resources(Plan, PROV.hadPlan)


class Attribution(AgentInfluence):
    """
    Attribution is the ascribing of an entity to an agent. When an entity e is attributed to agent ag, entity e was
    generated by some unspecified activity that in turn was associated to agent ag. Thus, this relation is useful when
    the activity is not known, or irrelevant.
    @iri: http://www.w3.org/ns/prov#Attribution
    @see: http://www.w3.org/TR/prov-o/#Attribution
    """

    def __init__(self, id=None, bundle=default_graph):
        AgentInfluence.__init__(id=id, bundle=bundle)
        self.add_type(PROV.Attribution)


class Role(Resource):
    """
    A role is the function of an entity or agent with respect to an activity, in the context of a usage, generation,
    invalidation, association, start, and end.
    @iri: http://www.w3.org/ns/prov#Role
    @see: http://www.w3.org/TR/prov-o/#Role
    """

    def __init__(self, id=None, bundle=default_graph):
        Resource.__init__(id=id, bundle=bundle)
        self.add_type(PROV.Role)
'''

class Entity(Resource):

    def __init__(self, id=None, bundle=default_graph):
        super(Entity, self).__init__(id,bundle)
        #print self._graph
        #print self._identifier
        #print type(self._graph)
        #self.add_type(PROV.Entity)

    def set_was_influenced_by(self, resource):
        """
        Specify the resource that influenced this entity.
        @iri: http://www.w3.org/ns/prov#wasInfluencedBy
        """
        resource = Resource.ensure_type(resource)
        self.add(PROV.wasInfluencedBy, resource)
        resource.add(PROV.influenced, self)

    def get_was_influenced_by(self):
        """
        Return all resources that influenced this entity.
        @iri: http://www.w3.org/ns/prov#wasInfluencedBy
        """
        return self.get_resources(Resource, PROV.wasInfluencedBy)

    def set_was_attributed_to(self, agent):
        """
        Specify the agent this entity was attributed to.
        @iri: http://www.w3.org/ns/prov#wasAttributedTo
        """
        agent = Agent.ensure_type(agent)
        self.set_was_influenced_by(agent)
        self.add(PROV.wasAttributedTo, agent)
        if using_inverse_properties():
            agent.add(PROV.contributed, self)

    def get_was_attributed_to(self):
        """
        Return all agents this entity was attributed to.
        @iri: http://www.w3.org/ns/prov#wasAttributedTo
        """
        return self.get_resources(Agent, PROV.wasAttributedTo)

    def attribution(self, agent, id=None):
        """
        Specify the agent this entity was attributed to.
        Return attribution relationship which can be used to further qualify the relationship.
        @iri: http://www.w3.org/ns/prov#qualifiedAttribution
        """
        attribution = Attribution(id)
        self.add(PROV.qualifiedAttribution, attribution)
        if using_inverse_properties():
            attribution.add(PROV.qualifiedAttributionOf, self)
        attribution.set_agent(agent)
        self.set_was_attributed_to(agent)
        return attribution

    def get_attribution(self):
        """
        Return all attribution relationships of this entity.
        @iri: http://www.w3.org/ns/prov#qualifiedAttribution
        """
        return self.get_resources(Attribution, PROV.qualifiedAttribution)

    def set_was_generated_by(self, activity):
        """
        Specify the activity that generated this agent.
        @iri: http://www.w3.org/ns/prov#wasGeneratedBy
        """
        activity = Activity.ensure_type(activity)
        self.set_was_influenced_by(activity)
        self.add(PROV.wasGeneratedBy, activity)
        activity.add(PROV.generated, self)

    def get_was_generated_by(self):
        """
        Return all activities this entity was generated by.
        @iri: http://www.w3.org/ns/prov#wasGeneratedBy
        """
        return self.get_resources(Activity, PROV.wasGeneratedBy)

    def generation(self, activity, id=None, datetime=None, role=None):
        """
        Specify the activity that generated this agent.
        Return generation relationship which can be used to further qualify the relationship.
        @iri: http://www.w3.org/ns/prov#qualifiedGeneration
        """
        generation = Generation(id)
        self.add(PROV.qualifiedGeneration, generation)
        if using_inverse_properties():
            generation.add(PROV.qualifiedGenerationOf, self)
        generation.set_activity(activity)
        if datetime is not None:
            generation.set_at_time(datetime)
        if role is not None:
            generation.set_had_role(role)
        self.set_was_generated_by(activity)
        return generation

    def get_generation(self):
        """
        Return all generation relationships of this entity.
        @iri: http://www.w3.org/ns/prov#qualifiedGeneration
        """
        return self.get_resources(Generation, PROV.qualifiedGeneration)

    def set_was_derived_from(self, entity):
        """
        Specify the entity this entity was derived from.
        @iri: http://www.w3.org/ns/prov#wasDerivedFrom
        """
        entity = Entity.ensure_type(entity)
        self.set_was_influenced_by(entity)
        self.add(PROV.wasDerivedFrom, entity)
        if using_inverse_properties():
            entity.add(PROV.hadDerivation, self)

    def get_was_derived_from(self):
        """
        Return all entities this entity was derived from.
        @iri: http://www.w3.org/ns/prov#wasDerivedFrom
        """
        return self.get_resources(Entity, PROV.wasDerivedFrom)

    def derivation(self, entity, id=None):
        """
        Specify the entity this entity was derived from.
        Return derivation relationship which can be used to further qualify the relationship.
        @iri: http://www.w3.org/ns/prov#qualifiedDerivation
        """
        derivation = Derivation(id)
        self.add(PROV.qualifiedDerivation, derivation)
        if using_inverse_properties():
            derivation.add(PROV.qualifiedDerivationOf, self)
        derivation.set_entity(entity)
        self.set_was_derived_from(entity)
        return derivation

    def get_derivation(self):
        """
        Return all Derivation relationships of this entity.
        @iri: http://www.w3.org/ns/prov#qualifiedDerivation
        """
        return self.get_resources(Derivation, PROV.qualifiedGeneration)

    def set_was_revision_of(self, entity):
        """
        Specify the entity this entity was a revision of.
        @iri: http://www.w3.org/ns/prov#wasRevisionOf
        """
        entity = Entity.ensure_type(entity)
        self.set_was_derived_from(entity)
        self.add(PROV.wasRevisionOf, entity)
        if using_inverse_properties():
            entity.add(PROV.hadRevision, self)

    def get_was_revision_of(self):
        """
        Return all entities this entity was a revision of.
        @iri: http://www.w3.org/ns/prov#wasRevisionOf
        """
        return self.get_resources(Entity, PROV.wasRevisionOf)

    def revision(self, entity, id=None):
        """
        Specify the entity this entity was a revision of.
        Return revision relationship which can be used to further qualify the relationship.
        @iri: http://www.w3.org/ns/prov#qualifiedRevision
        """
        entity = Entity.ensure_type(entity)
        revision = Revision(id)
        revision.set_entity(entity)
        self.add(PROV.qualifiedRevision, revision)
        if using_inverse_properties():
            revision.add(PROV.revisedEntity, self)
        self.set_was_revision_of(entity)
        return revision

    def get_revision(self):
        """
        Return all Revision relationships of this entity.
        @iri: http://www.w3.org/ns/prov#qualifiedRevision
        """
        return self.get_resources(Revision, PROV.qualifiedRevision)

    def set_was_quoted_from(self, entity):
        """
        Specify the entity this entity was quoted from.
        @iri: http://www.w3.org/ns/prov#wasQuotedFrom
        """
        entity = Entity.ensure_type(entity)
        self.set_was_derived_from(entity)
        self.add(PROV.wasQuotedFrom, entity)
        if using_inverse_properties():
            entity.add(PROV.quotedAs, self)

    def get_was_quoted_from(self):
        """
        Return all entities this entity was quoted from.
        @iri: http://www.w3.org/ns/prov#wasQuotedFrom
        """
        return self.get_resources(Entity, PROV.wasQuotedFrom)

    def quotation(self, entity, id=None):
        """
        Specify the entity this entity was quoted from.
        Return quotation relationship which can be used to further qualify the relationship.
        @iri: http://www.w3.org/ns/prov#qualifiedQuotation
        """
        entity = Entity.ensure_type(entity)
        quotation = Quotation(id)
        quotation.set_entity(entity)
        self.add(PROV.qualifiedQuotation, quotation)
        if using_inverse_properties():
            quotation.add(PROV.qualifiedQuotationOf, self)
        self.set_was_quoted_from(entity)
        return quotation

    def get_quotation(self):
        """
        Return all quotation relationships of this entity.
        @iri: http://www.w3.org/ns/prov#qualifiedQuotation
        """
        return self.get_resources(Quotation, PROV.qualifiedQuotation)

    def set_had_primary_source(self, entity):
        """
        Specify the primary source of this entity.
        @iri: http://www.w3.org/ns/prov#hadPrimarySource
        """
        entity = Entity.ensure_type(entity)
        self.set_was_derived_from(entity)
        self.add(PROV.hadPrimarySource, entity)
        if using_inverse_properties():
            entity.add(PROV.wasPrimarySourceOf, self)

    def get_had_primary_source(self):
        """
        Return all entities that are a primary source for this entity.
        @iri: http://www.w3.org/ns/prov#hadPrimarySource
        """
        return self.get_resources(Entity, PROV.hadPrimarySource)

    def primary_source(self, entity, id=None):
        """
        Specify the primary source of this entity.
        Return primary source relationship which can be used to further qualify the relationship.
        @iri: http://www.w3.org/ns/prov#qualifiedPrimarySource
        """
        entity = Entity.ensure_type(entity)
        primary_source = PrimarySource(id)
        primary_source.set_entity(entity)
        self.add(PROV.qualifiedPrimarySource, primary_source)
        if using_inverse_properties():
            primary_source.add(PROV.qualifiedSourceOf, self)
        self.set_had_primary_source(entity)
        return primary_source

    def get_primary_source(self):
        """
        Return all primary source relationships of this entity.
        @iri: http://www.w3.org/ns/prov#qualifiedPrimarySource
        """
        return self.get_resources(PrimarySource, PROV.qualifiedPrimarySource)

    def set_was_invalidated_by(self, activity):
        """
        Specify the activity that invalidated this entity.
        @iri: http://www.w3.org/ns/prov#wasInvalidatedBy
        """
        activity = Activity.ensure_type(activity)
        self.set_was_influenced_by(activity)
        self.add(PROV.wasInvalidatedBy, activity)
        activity.add(PROV.invalidated, self)

    def get_was_invalidated_by(self):
        """
        Return all activities that invalidated this entity.
        @iri: http://www.w3.org/ns/prov#wasInvalidatedBy
        """
        return self.get_resources(Activity, PROV.wasInvalidatedBy)

    def invalidation(self, activity, id=None, datetime=None):
        """
        Specify the activity that invalidated this entity.
        Return invalidation relationship which can be used to further qualify the relationship.
        @iri: http://www.w3.org/ns/prov#qualifiedInvalidation
        """
        activity = Activity.ensure_type(activity)
        invalidation = Invalidation(id)
        invalidation.set_activity(activity)
        if datetime is not None:
            invalidation.set_at_time(datetime)
        self.add(PROV.qualifiedInvalidation, invalidation)
        if using_inverse_properties():
            invalidation.add(PROV.qualifiedInvalidationOf, self)
        self.set_was_invalidated_by(activity)
        return invalidation

    def get_invalidation(self):
        """
        Return all invalidation relationships of this entity.
        @iri: http://www.w3.org/ns/prov#qualifiedInvalidation
        """
        return self.get_resources(Invalidation, PROV.qualifiedInvalidation)

    def set_alternate_of(self, entity):
        """
        Specify an alternate of this entity.
        @iri: http://www.w3.org/ns/prov#alternateOf
        """
        entity = Entity.ensure_type(entity)
        self.add(PROV.alternateOf, entity)
        entity.add(PROV.alternateOf, self)

    def get_alternate_of(self):
        """
        Return all entities that are alternates of this entity.
        @iri: http://www.w3.org/ns/prov#alternateOf
        """
        return self.get_resources(Entity, PROV.alternateOf)

    def set_specialization_of(self, entity):
        """
        Specify an specialization of this entity.
        @iri: http://www.w3.org/ns/prov#specializationOf
        """
        entity = Entity.ensure_type(entity)
        self.set_alternate_of(entity)
        self.add(PROV.specializationOf, entity)
        if using_inverse_properties():
            entity.add(PROV.generalizationOf, self)

    def get_specialization_of(self):
        """
        Return all entities that that this entity is a specialization of.
        @iri: http://www.w3.org/ns/prov#specializationOf
        """
        return self.get_resources(Entity, PROV.specializationOf)

    def set_at_location(self, location):
        """
        Specify a location for this entity.
        @iri: http://www.w3.org/ns/prov#atLocation
        """
        location = Location.ensure_type(location)
        self.add(PROV.atLocation, location)
        if using_inverse_properties():
            location.add(PROV.locationOf, self)

    def get_at_location(self):
        """
        Return all locations for this entity.
        @iri: http://www.w3.org/ns/prov#atLocation
        """
        return self.get_resources(Location, PROV.atLocation)

    def set_generated_at_time(self, datetime):
        """
        Specify a generation datetime for this entity.
        @iri: http://www.w3.org/ns/prov#generatedAtTime
        """
        self.set(PROV.generatedAtTime, Literal(datetime, datatype=XSD.dateTime))

    def get_generated_at_time(self):
        """
        Return the datetime at which this entity was generated.
        @iri: http://www.w3.org/ns/prov#generatedAtTime
        """
        return Literal(self.value(PROV.generatedAtTime), datatype=XSD.dateTime).toPython()

    def set_invalidated_at_time(self, datetime):
        """
        Specify an invalidation datetime for this entity.
        @iri: http://www.w3.org/ns/prov#invalidatedAtTime
        """
        self.set(PROV.invalidatedAtTime, Literal(datetime, datatype=XSD.dateTime))

    def get_invalidated_at_time(self):
        """
        Return the datetime at which this entity was invalidated.
        @iri: http://www.w3.org/ns/prov#invalidatedAtTime
        """
        return Literal(self.value(PROV.invalidatedAtTime), datatype=XSD.dateTime).toPython()

    def set_value(self, value):
        """
        Specify a value for this entity.
        @iri: http://www.w3.org/ns/prov#value
        """
        self.set(PROV.value, Literal(value))

    def get_value(self):
        """
        Return the value for this entity.
        @iri: http://www.w3.org/ns/prov#value
        """
        return Literal(self.value(PROV.value)).toPython()
        
class Activity(Resource):
    """
    An activity is something that occurs over a period of time and acts upon or with entities; it may include
    consuming, processing, transforming, modifying, relocating, using, or generating entities.
    @iri: http://www.w3.org/ns/prov#Activity
    @see: http://www.w3.org/TR/prov-o/#Activity
    """

    def __init__(self, id=None, bundle=default_graph):
        super(Activity,self).__init__(id, bundle)
        self.add_type(PROV.Activity)

    def set_influenced(self, entity):
        """
        Specify an entity that was influenced by this activity.
        @iri: http://www.w3.org/ns/prov#influenced
        """
        entity = Entity.ensure_type(entity)
        self.add(PROV.influenced, entity)

    def get_influenced(self):
        """
        Return all entities that were influenced by this activity.
        @iri: http://www.w3.org/ns/prov#influenced
        """
        return self.get_resources(Entity, PROV.influenced)

    def set_was_influenced_by(self, resource):
        """
        Specify a resource that influenced this activity.
        @iri: http://www.w3.org/ns/prov#wasInfluencedBy
        """
        self.add(PROV.wasInfluencedBy, resource)
        resource.add(PROV.influenced, self)

    def get_was_influenced_by(self):
        """
        Return all resources that influenced this activity.
        @iri: http://www.w3.org/ns/prov#wasInfluencedBy
        """
        return [self.graph.objects(self.identifier, PROV.influenced)]

    def set_used(self, entity):
        """
        Specify an entity that was used by this activity.
        @iri: http://www.w3.org/ns/prov#used
        """
        entity = Entity.ensure_type(entity)
        self.set_was_influenced_by(entity)
        self.add(PROV.used, entity)
        if using_inverse_properties():
            entity.add(PROV.wasUsedBy, self)

    def get_used(self):
        """
        Return all entities used by this activity.
        @iri: http://www.w3.org/ns/prov#used
        """
        return self.get_resources(Entity, PROV.used)

    def usage(self, entity, id=None, datetime=None, role=None, location=None):
        """
        Specify an entity that was used by this activity.
        Return usage relationship which can be used to further qualify the relationship.
        @iri: http://www.w3.org/ns/prov#qualifiedUsage
        """
        usage = Usage(id)
        usage.set_entity(entity)
        if datetime is not None:
            usage.set_at_time(datetime)
        if role is not None:
            usage.set_had_role(role)
        if location is not None:
            usage.set_at_location(location)
        self.add(PROV.qualifiedUsage, usage)
        if using_inverse_properties():
            usage.add(PROV.qualifiedUsingActivity, self)
        self.set_used(entity)
        return usage

    def get_usage(self):
        """
        Return all usage relationships of this activity.
        @iri: http://www.w3.org/ns/prov#qualifiedUsage
        """
        return self.get_resources(Usage, PROV.qualifiedUsage)

    def set_generated(self, entity):
        """
        Specify an entity that was generated by this activity.
        @iri: http://www.w3.org/ns/prov#generated
        """
        entity = Entity.ensure_type(entity)
        self.set_influenced(entity)
        self.add(PROV.generated, entity)
        entity.add(PROV.wasGeneratedBy, self)

    def get_generated(self):
        """
        Return all entities generated by this activity.
        @iri: http://www.w3.org/ns/prov#generated
        """
        return self.get_resources(Entity, PROV.generated)

    def set_invalidated(self, entity):
        """
        Specify an entity that was invalidated by this activity.
        @iri: http://www.w3.org/ns/prov#invalidated
        """
        entity = Entity.ensure_type(entity)
        self.set_influenced(entity)
        self.add(PROV.invalidated, entity)
        entity.add(PROV.wasInvalidatedBy, self)

    def get_invalidated(self):
        """
        Return all entities invalided by this activity.
        @iri: http://www.w3.org/ns/prov#invalidated
        """
        return self.get_resources(Entity, PROV.invalidated)

    def set_was_informed_by(self, activity):
        """
        Specify an activity that informed this activity.
        @iri: http://www.w3.org/ns/prov#wasInformedBy
        """
        activity = Activity.ensure_type(activity)
        self.set_was_influenced_by(activity)
        self.add(PROV.wasInformedBy, activity)
        if using_inverse_properties():
            activity.add(PROV.informed, activity)

    def get_was_informed_by(self):
        """
        Return all activities that informed this activity.
        @iri: http://www.w3.org/ns/prov#wasInformedBy
        """
        return self.get_resources(Activity, PROV.wasInformedBy)

    def communication(self, activity, id=None, role=None):
        """
        Specify an activity that informed this activity.
        Return communication relationship which can be used to further qualify the relationship.
        @iri: http://www.w3.org/ns/prov#qualifiedCommunication
        """
        communication = Communication(id)
        communication.set_activity(activity)
        if role is not None:
            communication.set_had_role(role)
        self.add(PROV.qualifiedCommunication, communication)
        if using_inverse_properties():
            communication.add(PROV.qualifiedCommunicationOf, self)
        self.set_was_informed_by(activity)
        return communication

    def get_communication(self):
        """
        Return all communication relationships for this activity.
        @iri: http://www.w3.org/ns/prov#qualifiedCommunication
        """
        return self.get_resources(Communication, PROV.qualifiedCommunication)

    def set_was_associated_with(self, agent):
        """
        Specify an agent that was associated with this activity.
        @iri: http://www.w3.org/ns/prov#wasAssociatedWith
        """
        agent = Agent.ensure_type(agent)
        self.set_was_influenced_by(agent)
        self.add(PROV.wasAssociatedWith, agent)
        if using_inverse_properties():
            agent.add(PROV.wasAssociateFor, self)

    def get_was_associated_with(self):
        """
        Return all agents associated with this activity
        @iri: http://www.w3.org/ns/prov#wasAssociatedWith
        """
        return self.get_resources(Agent, PROV.wasAssociatedWith)

    def association(self, agent, id=None, plan=None, role=None):
        """
        Specify an agent that was associated with this activity.
        Return association relationship which can be used to further qualify the relationship.
        @iri: http://www.w3.org/ns/prov#qualifiedAssociation
        """
        association = Association(id)
        association.set_agent(agent)
        if role is not None:
            association.set_had_role(role)
        if plan is not None:
            association.set_had_plan(plan)
        self.add(PROV.qualifiedAssociation, association)
        if using_inverse_properties():
            association.add(PROV.qualifiedAssociationOf, self)
        self.set_was_associated_with(agent)
        return association

    def get_association(self):
        """
        Return all association relationships for this activity.
        @iri: http://www.w3.org/ns/prov#qualifiedAssociation
        """
        return self.get_resources(Association, PROV.qualifiedAssociation)

    def set_was_started_by(self, entity):
        """
        Specify the entity that started this activity.
        @iri: http://www.w3.org/ns/prov#wasStartedBy
        """
        entity = Entity.ensure_type(entity)
        self.set_was_influenced_by(entity)
        self.add(PROV.wasStartedBy, entity)
        if using_inverse_properties():
            entity.add(PROV.started, self)

    def get_was_started_by(self):
        """
        Return all entities that started this activity.
        @iri: http://www.w3.org/ns/prov#wasStartedBy
        """
        return self.get_resources(Entity, PROV.wasStartedBy)

    def start(self, entity, id=None, datetime=None, location=None):
        """
        Specify the entity that started this activity.
        Return start relationship which can be used to further qualify the relationship.
        @iri: http://www.w3.org/ns/prov#qualifiedStart
        """
        entity = Entity.ensure_type(entity)
        start = Start(id)
        start.set_entity(entity)
        if datetime is not None:
            start.set_at_time(datetime)
        if location is not None:
            start.set_at_location(location)
        self.add(PROV.qualifiedStart, start)
        if using_inverse_properties():
            start.add(PROV.qualifiedStartOf, self)
        self.set_was_started_by(entity)
        return start

    def get_start(self):
        """
        Return all start relationships for this activity.
        @iri: http://www.w3.org/ns/prov#qualifiedStart
        """
        return self.get_resources(Start, PROV.qualifiedStart)

    def set_was_ended_by(self, entity):
        """
        Specify the entity that ended this activity.
        @iri: http://www.w3.org/ns/prov#wasEndedBy
        """
        entity = Entity.ensure_type(entity)
        self.set_was_influenced_by(entity)
        self.add(PROV.wasEndedBy, entity)
        if using_inverse_properties():
            entity.add(PROV.ended, self)

    def get_was_ended_by(self):
        """
        Return all entities that ended this activity.
        @iri: http://www.w3.org/ns/prov#wasEndedBy
        """
        return self.get_resources(Entity, PROV.wasEndedBy)

    def end(self, entity, id=None, datetime=None, location=None):
        """
        Specify the entity that ended this activity.
        Return end relationship which can be used to further qualify the relationship.
        @iri: http://www.w3.org/ns/prov#qualifiedEnd
        """
        entity = Entity.ensure_type(entity)
        end = End(id)
        end.set_entity(entity)
        if datetime is not None:
            end.set_at_time(datetime)
        if location is not None:
            end.set_at_location(location)
        self.add(PROV.qualifiedEnd, end)
        if using_inverse_properties():
            end.add(PROV.qualifiedEndOf, self)
        self.set_was_ended_by(entity)
        return end

    def get_end(self):
        """
        Return all end relationships for this activity.
        @iri: http://www.w3.org/ns/prov#qualifiedEnd
        """
        return self.get_resources(End, PROV.qualifiedEnd)

    def set_at_location(self, location):
        """
        Specify a location for this activity.
        @iri: http://www.w3.org/ns/prov#atLocation
        """
        location = Location.ensure_type(location)
        self.add(PROV.atLocation, location)
        if using_inverse_properties():
            location.add(PROV.locationOf, self)

    def get_at_location(self):
        """
        Return all locations for this activity.
        @iri: http://www.w3.org/ns/prov#atLocation
        """
        return self.get_resources(Location, PROV.atLocation)

    def set_started_at_time(self, datetime):
        """
        Specified a start datetime for this activity.
        @iri: http://www.w3.org/ns/prov#startedAtTime
        """
        self.set(PROV.startedAtTime, Literal(datetime, datatype=XSD.dateTime))

    def get_started_at_time(self):
        """
        Return the start datetime for this activity.
        @iri: http://www.w3.org/ns/prov#startedAtTime
        """
        return Literal(self.value(PROV.startedAtTime), datatype=XSD.dateTime).toPython()

    def set_ended_at_time(self, datetime):
        """
        Specify a end datetime for this activity.
        @iri: http://www.w3.org/ns/prov#endedAtTime
        """
        self.set(PROV.endedAtTime, Literal(datetime, datatype=XSD.dateTime))

    def get_ended_at_time(self):
        """
        Return the end datetime for this activity.
        @iri: http://www.w3.org/ns/prov#endedAtTime
        """
        return Literal(self.value(PROV.endedAtTime), datatype=XSD.dateTime).toPython()
