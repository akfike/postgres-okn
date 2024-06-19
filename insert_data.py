import psycopg2
import pandas as pd


# Create Table Query
# CREATE TABLE incident_type (
#     incident_type_id SERIAL PRIMARY KEY,
#     incident_type_name VARCHAR(56) NOT NULL,
#     source_dataset SMALLINT NOT NULL,
#     year SMALLINT NOT NULL
# );
# Define your data
data = {
    'incident_type_name': [
        'Motor vehicle theft', 
        'Larceny or theft', 
        'Burglary or breaking and entering',
        'Serious violent offense', 
        'Simple assault or battery', 
        'Robbery', 
        'Arson',
        'DUI of alcohol or drugs', 
        'Drunkenness or liquor law violations', 
        'Tobacco possession',
        'Possession, manufacture, or sale of drugs', 
        'Other sexual offense (not prostitution or rape)',
        'Fraud, possessing stolen goods, or vandalism', 
        'Weapons laws violation', 
        'Violation of court order/probation/parole, perjury', 
        'Disorderly conduct',
        'Unspecified crimes against persons/property/society', 
        'Traffic violations',
        'Trespass of real property', 
        'Family offenses, nonviolent', 
        'Intimidation', 
        'Evading/hindering/obstructing police',
        'Child endangerment/neglect/abandonment', 
        'Harassment; intimidation not specified', 
        'Hit and run/leaving the scene of an accident'
    ],
    'source_dataset': [1]*25,  # Adjusted to match the length of incident_type_name
    'year': [2022]*25  # Adjusted to match the length of incident_type_name
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="temp_db",
    user="postgres",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Define the SQL insert statement
insert_query = """
INSERT INTO incident_type (incident_type_name, source_dataset, year)
VALUES (%s, %s, %s)
RETURNING incident_type_id;
"""

# Iterate over the rows of the dataframe and insert data into PostgreSQL
for index, row in df.iterrows():
    cursor.execute(insert_query, (row['incident_type_name'], row['source_dataset'], row['year']))
    incident_type_id = cursor.fetchone()[0]  # Get the generated incident_type_id
    print(f"Inserted {row['incident_type_name']} with ID {incident_type_id}")

# Commit the transaction
conn.commit()

# Close the connection
cursor.close()
conn.close()
