def extract_relationships_from_folder(folder_path):
    relationships = []

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                try:
                    json_data = json.load(file)
                    relationship = extract_relationship(json_data)
                    if relationship:
                        relationships.append(relationship)
                except json.JSONDecodeError:
                    print(f"Error decoding JSON file: {file_path}")
                except KeyError:
                    print(f"Missing key in JSON file: {file_path}")

    return relationships


def extract_relationship(json_data):
    relationship = None

    if 'objects' in json_data and isinstance(json_data['objects'], list):
        for obj in json_data['objects']:
            if obj.get('type') == 'relationship':
                relationship = {
                    'id': obj.get('id'),
                    'type': obj.get('relationship_type'),
                    'source_ref': obj.get('source_ref'),
                    'target_ref': obj.get('target_ref')
                }
                break

    return relationship

# Example usage
folder_path = "F:\\Projects\\CTI\\enterprise-attack\\relationship"
relationships = extract_relationships_from_folder(folder_path)

for relationship in relationships:
    print('ID:', relationship['id'])
    print('Type:', relationship['type'])
    print('Source Ref:', relationship['source_ref'])
    print('Target Ref:', relationship['target_ref'])
    print('---')

print(len(relationships))
