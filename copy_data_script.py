# SCRIPT TO READ AND COPY DATA IN CSV FILE
from cassandra.cluster import Cluster
import csv

# Connect to your Cassandra or ScyllaDB cluster
cluster = Cluster(['172.18.0.2'])
session = cluster.connect('carepet')

# Define the CSV file name
output_csv = 'output2.csv'

# Create a list of sensor IDs you want to query
sensor_ids = ['04fcb5ca-2eb9-4d97-b142-6320264aa440', '83b4e224-54fd-4020-8167-c6132230bf9b']

# Open the CSV file for writing
with open(output_csv, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['sensor_id', 'ts', 'value'])  # Add header row

    # Query and write data for each sensor ID
    for sensor_id in sensor_ids:
        query = f"SELECT * FROM carepet.measurement WHERE sensor_id = {sensor_id} ORDER BY ts ASC"
        result = session.execute(query)
        for row in result:
            csv_writer.writerow([row.sensor_id, row.ts, row.value])

# Close the Cassandra/ScyllaDB session
cluster.shutdown()
