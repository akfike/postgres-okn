from rdflib import Graph, Namespace, RDF, RDFS, URIRef

# Define namespaces
SAIL = Namespace("http://sail.ua.edu/okn/nsduh/incident_type#")
RDF_NS = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
RDFS_NS = Namespace("http://www.w3.org/2000/01/rdf-schema#")

# Create a new graph
g = Graph()

# Bind prefixes to namespaces
g.bind("sail", SAIL)
g.bind("rdf", RDF_NS)
g.bind("rdfs", RDFS_NS)

# Define classes
g.add((SAIL.Person, RDF_NS.type, RDFS_NS.Class))
g.add((SAIL.Crime, RDF_NS.type, RDFS_NS.Class))
g.add((SAIL.Substance, RDF_NS.type, RDFS_NS.Class))

# Define instances of Crime
crimes = [
    "MotorVehicleTheft", "Burglary", "LarcenyOrTheft", "AggravatedAssault",
    "ForcibleRape", "Murder", "Homicide", "NonnegligentManslaughter",
    "OtherAssault", "Robbery", "Arson", "DrivingUnderInfluence",
    "PossessionOfTobacco", "ProstitutionOrCommercializedSex", "SexualOffense",
    "Fraud", "PossessingStolenGoods", "Vandalism"
]

for crime in crimes:
    g.add((SAIL[crime], RDF_NS.type, SAIL.Crime))

# Define instances of Substance
substances = [
    "Alcohol", "Marijuana", "Cocaine", "Heroin", "Hallucinogens", "Inhalants", "Methamphetamine"
]

for substance in substances:
    g.add((SAIL[substance], RDF_NS.type, SAIL.Substance))

# Define properties
properties = [
    "arrestedAndBookedFor", "underTheInfluenceOf"
]

for prop in properties:
    g.add((SAIL[prop], RDF_NS.type, RDF_NS.Property))

# Define relationships
g.add((SAIL.Person, SAIL.arrestedAndBookedFor, SAIL.Crime))
g.add((SAIL.Person, SAIL.underTheInfluenceOf, SAIL.Substance))

# Serialize the graph to a turtle file
with open("ontology.ttl", "w") as f:
    f.write(g.serialize(format='turtle'))
