def get_entity_name_enterprise():
    entity_data = []
    
    for relationship in relationships:
        if relationship['source_ref'].startswith('intrusion-set'):
            threat_actor_id = relationship['source_ref']
            
            for threat_actor in threat_actors:
                if threat_actor['id'] == threat_actor_id:
                    threat_actor_name = threat_actor['name']
                    break
                    
            if relationship['target_ref'].startswith('attack-pattern'):
                for ttp in ttps:
                    if ttp['id'] == relationship['target_ref']:
                        ttp_id = ttp['external_id']
                        if threat_actor_name.startswith('APT'):
                            entity_data.append({
                                'name': threat_actor_name,
                                'type': relationship['type'],
                                'ttp': ttp_id
                            })
                        break
           
            elif relationship['target_ref'].startswith('malware'):
                for malware in malware_objects:
                    if malware['id'] == relationship['target_ref']:
                        malware_name = malware['name']
                        if threat_actor_name.startswith('APT'):
                            entity_data.append({
                                'name': threat_actor_name,
                                'type': relationship['type'],
                                'malware': malware_name
                            })
                        break
                        
    return entity_data
