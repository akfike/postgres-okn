import psycopg2
import pandas as pd
from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import XSD

# Connect to PostgreSQL and fetch data
conn = psycopg2.connect(
    dbname="temp_db",
    user="postgres",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Query to fetch data from the incident_type table
query = "SELECT * FROM incident_type;"
cursor.execute(query)

# Fetch all rows from the executed query
rows = cursor.fetchall()

# Get column names
colnames = [desc[0] for desc in cursor.description]

# Convert to DataFrame
df = pd.DataFrame(rows, columns=colnames)

# Close the connection
cursor.close()
conn.close()

# Create a new RDF graph
g = Graph()

# Define namespaces
n = Namespace("http://sail.ua.edu/okn/nsduh#")

# Add data to the graph
for index, row in df.iterrows():
    incident_type = URIRef(f"{n}incident_type/{row['incident_type_id']}")
    g.add((incident_type, RDF.type, n.IncidentType))
    g.add((incident_type, n.incidentTypeName, Literal(row['incident_type_name'], datatype=XSD.string)))
    g.add((incident_type, n.sourceDataset, Literal(row['source_dataset'], datatype=XSD.integer)))
    g.add((incident_type, n.year, Literal(row['year'], datatype=XSD.integer)))

# Define the namespace bindings
g.bind("sail", n)

# Serialize the graph in Turtle format
g.serialize("incident_type.ttl", format="turtle")

print("Turtle file has been created successfully.")
