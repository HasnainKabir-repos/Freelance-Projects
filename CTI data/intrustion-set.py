import json
import os

def extract_threat_actors_from_folder(folder_path):
    threat_actors = []

    # Iterate over each file in the folder
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)

        # Check if the file is a JSON file
        if file_name.endswith('.json'):
            with open(file_path, 'r') as json_file:
                try:
                    json_data = json.load(json_file)
                    threat_actor = extract_threat_actor(json_data)
                    threat_actors.append(threat_actor)
                except json.JSONDecodeError:
                    print(f"Error parsing JSON file: {file_path}")

    return threat_actors

def extract_threat_actor(json_data):
    threat_actor = {}

    if 'objects' in json_data and isinstance(json_data['objects'], list):
        for obj in json_data['objects']:
            if obj.get('type') == 'intrusion-set':
                threat_actor['id'] = obj.get('id')
                threat_actor['name'] = obj.get('name')
                #threat_actor['aliases'] = obj.get('aliases', [])
                #threat_actor['description'] = obj.get('description')
                # Add more attributes as needed

    return threat_actor


# Provide the path to the folder containing the JSON files
folder_path = 'F:\Projects\CTI\enterprise-attack\intrusion-set'

# Extract threat actors from the folder
threat_actors = extract_threat_actors_from_folder(folder_path)

# Print the extracted threat actors
for threat_actor in threat_actors:
    print(threat_actor)
print(len(threat_actors))