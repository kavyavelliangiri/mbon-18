from neuprint import Client, fetch_synapses

c = Client('neuprint.janelia.org', 'hemibrain:v1.2.1', token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImthdnlhYXZlbGxpYW5naXJpQGdtYWlsLmNvbSIsImxldmVsIjoibm9hdXRoIiwiaW1hZ2UtdXJsIjoiaHR0cHM6Ly9saDMuZ29vZ2xldXNlcmNvbnRlbnQuY29tL2EvQUFUWEFKeVRXUzZPem9QSGw4OFFxQldzQkxwdDRxRUMyZS1KUmxzckpCMEs9czk2LWM_c3o9NTA_c3o9NTAiLCJleHAiOjE4MTQ5MzA1NTV9.0AwtioiQp4McVbAa4BIMr4B8DcLPb4tkbDELvW0gpYs')

#gradually increase heal param until 'more than one tree', then increase more
swc = c.fetch_skeleton(5813020828, heal = 200, export_path = 'original-MBON18-structure.swc', format='swc')


syn_df = fetch_synapses(5813020828)

print(syn_df[:10])