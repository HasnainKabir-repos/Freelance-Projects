def extract_ttps_from_folder(folder_path):
    ttps = []

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path) and filename.endswith('.json'):
            with open(file_path, 'r') as file:
                json_data = json.load(file)
                ttps.extend(extract_ttps(json_data))

    return ttps

def extract_ttps(json_data):
    ttps = []

    if 'objects' in json_data and isinstance(json_data['objects'], list):
        for obj in json_data['objects']:
            if obj.get('type') == 'attack-pattern':
                ttp = {
                    'id': obj.get('id'),
                    'name': obj.get('name'),
                    'external_id': obj['external_references'][0].get('external_id')
                }
                ttps.append(ttp)

    return ttps


# Example usage
folder_path = "F:\\Projects\\CTI\\enterprise-attack\\attack-pattern"
ttps = extract_ttps_from_folder(folder_path)

# Print the extracted TTPs
for ttp in ttps:
    print('ID:', ttp['id'])
    print('Name:', ttp['name'])
    print('External_id:', ttp['external_id'])
    print('---')
    
print(len(ttps))