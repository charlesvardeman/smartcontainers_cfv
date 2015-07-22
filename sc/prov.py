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
            #print id
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


class Bundle(Entity):
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
