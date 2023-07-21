"""
Database: 
neuprint-examples.janelia.org


Download MBON-18 (bodyID = 5813020828)
1- morphology
2- synapse locations

See email from Stuart Berg (7/24) for code example
Documentaion at
https://connectome-neuprint.github.io/neuprint-python/docs/index.html

"""

# Load python library to access neuprint database
from neuprint import Client, fetch_synapses, fetch_synapse_connections, SynapseCriteria as SC
import csv
import pandas as pd
import statistics
import json

# Create the client to access the mushroom body database
c = Client('neuprint.janelia.org', dataset='hemibrain:v1.2.1', token='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImthdnlhYXZlbGxpYW5naXJpQGdtYWlsLmNvbSIsImxldmVsIjoibm9hdXRoIiwiaW1hZ2UtdXJsIjoiaHR0cHM6Ly9saDMuZ29vZ2xldXNlcmNvbnRlbnQuY29tL2EvQUFUWEFKeVRXUzZPem9QSGw4OFFxQldzQkxwdDRxRUMyZS1KUmxzckpCMEs9czk2LWM_c3o9NTA_c3o9NTAiLCJleHAiOjE4MjE0ODU3ODd9.XK8GXQc9si-O4EIWRqiepcOlpvqs-kKhBdKxw90OU7s')
version = c.fetch_version()
print('Version = '+str(version))

# SYNAPSES 

# Simple output, all synapses ending on our neuron 
syn_df = fetch_synapses(5813020828)
print(syn_df[990:1000])

# More details: show both pre-synaptic and post-synaptic cell IDs
syn_more = fetch_synapse_connections(target_criteria=5813020828)
print('The total number of syanpses found is = '+str(len(syn_more)))

print(syn_more[:10])

# Want to take only those synapses whose presynaptic partners are Kenyon Cells
# Search the pre-synaptic bodyID using the list of KC Tbar ids determined from the original paper
# Read in list of KC Tbar ids - copied over from the "Takemura paper files" folder
KC_IDs = []
with open('Kc-MBON.csv', mode='r') as KC_file:
    csv_reader = csv.reader(KC_file, delimiter=',')
    for row in csv_reader:
        KC_IDs.append(int(row[0]))

# Fetch synapses w/ presynaptic KC and post-synaptic MBON
syn_KCs = fetch_synapse_connections(source_criteria=KC_IDs, target_criteria=5813020828)



# Want to collect relevant coordinates in a dictionary sorting by KC
coordinates = {}
for KC in KC_IDs:
    coordinates[str(KC)] = []

# can select a row using loc: 
# syn_KCs.loc[5,:]

# Factor to adjust from pixels to um coordinates
factor = 8*(10**(-3))

for i in range(len(syn_KCs)):
    x = int(syn_KCs.loc[i, 'x_post'])
    y = int(syn_KCs.loc[i, 'y_post'])
    z = int(syn_KCs.loc[i, 'z_post'])
    x_scaled = factor * x
    y_scaled = factor * y
    z_scaled = factor * z
    coordinates[str(syn_KCs.loc[i,'bodyId_pre'])].append([x_scaled, y_scaled, z_scaled])

lengths = []
for ID, coords in coordinates.items():
    lengths.append(len(coords))

print("The Total number of KC>MBON synapses is = "+str(len(syn_KCs)))   # SHould be 12770
print("The total number of presynaptic KCs is = "+str(len(coordinates)))  # Should be 948
print("The average number of KC>MBON synapses per KC is = "+str(statistics.mean(lengths)))   # Should be 13.47

# All looks good, now just need to export synapses as json for use in model


# SAVE THE SYNAPSE DATA
# Put coordinates dictionary into json
coordinates_json = json.dumps(coordinates, indent = 4)


# Export to file
with open('synapse_coordinates_scaled.json', 'w') as output: 
    output.write(coordinates_json)
output.close()
print('Finished writing synapses to file') 

