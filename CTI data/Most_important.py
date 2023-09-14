
node_queries = []
relationship_queries = []
processed_names = set()
processed_ttps = set()
processed_malware = set()

for item in qu:
    if 'name' in item:
        name = item['name']
        if name not in processed_names:
            node_query = f"CREATE (:Threat_actor {{name: '{name}'}})"
            node_queries.append(node_query)
            processed_names.add(name)

    if 'ttp' in item:
        ttp = item['ttp']
        if ttp not in processed_ttps:
            node_query = f"CREATE (:TTP {{ttp: '{ttp}'}})"
            node_queries.append(node_query)
            processed_ttps.add(ttp)

        relationship_query = f"MATCH (n:Threat_actor {{name: '{item['name']}'}}), (t:TTP {{ttp: '{ttp}'}})\nCREATE (n)-[:USES]->(t);"
        relationship_queries.append(relationship_query)

    elif 'malware' in item:
        malware = item['malware']
        if malware not in processed_malware:
            node_query = f"CREATE (:Malware {{malware: '{malware}'}})"
            node_queries.append(node_query)
            processed_malware.add(malware)

        relationship_query = f"MATCH (n:Threat_actor {{name: '{item['name']}'}}), (m:Malware {{malware: '{malware}'}})\nCREATE (n)-[:USES]->(m);"
        relationship_queries.append(relationship_query)


for query in node_queries + relationship_queries:
    print(query)
