import json
from typing import Dict, List, Set
from collections import Counter, defaultdict

class GTMParser:
    """
    Parser for Google Tag Manager (GTM) workspace JSON exports.
    Handles both server-side and client-side container analysis.
    """
    
    def __init__(self, file_path: str):
        """
        Initialize the parser with the path to the GTM JSON file.
        
        Args:
            file_path (str): Path to the GTM workspace JSON file
        """
        self.file_path = file_path
        self.data = None
        self.container_type = None
        self._load_data()
        self._determine_container_type()
    
    def _load_data(self):
        """
        Load the JSON data into memory for processing.
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                self.data = json.load(file)
        except Exception as e:
            raise Exception(f"Error loading GTM data: {e}")
    
    def _determine_container_type(self):
        """
        Determine if this is a server-side or client-side container.
        """
        if not self.data:
            return
        
        container_info = self.data.get('containerVersion', {}).get('container', {})
        usage_context = container_info.get('usageContext', [])
        
        if 'SERVER' in usage_context:
            self.container_type = 'server-side'
        elif 'WEB' in usage_context:
            self.container_type = 'client-side'
        else:
            self.container_type = 'unknown'
    
    def get_container_info(self) -> Dict:
        """
        Get basic container information.
        
        Returns:
            Dict: Container metadata
        """
        if not self.data:
            return {}
        
        container_version = self.data.get('containerVersion', {})
        container = container_version.get('container', {})
        
        return {
            'container_name': container.get('name', ''),
            'public_id': container.get('publicId', ''),
            'container_type': self.container_type,
            'account_id': container.get('accountId', ''),
            'container_id': container.get('containerId', ''),
            'export_time': self.data.get('exportTime', ''),
            'tagging_server_urls': container.get('taggingServerUrls', [])
        }
    
    def get_tags_summary(self) -> Dict:
        """
        Get comprehensive summary of tags in the GTM container.
        
        Returns:
            Dict: Summary containing tag counts, types, and destinations
        """
        if not self.data:
            return {}
        
        tags = self.data.get('containerVersion', {}).get('tag', [])
        total_tags = len(tags)
        
        # Tag types breakdown
        tag_types = Counter()
        destinations = Counter()
        
        for tag in tags:
            tag_type = tag.get('type', 'unknown')
            tag_types[tag_type] += 1
            
            # Extract destinations based on tag parameters
            parameters = tag.get('parameter', [])
            for param in parameters:
                if param.get('key') in ['measurementId', 'trackingId', 'containerId']:
                    destination = param.get('value', 'unknown')
                    destinations[destination] += 1
        
        # Count tags by firing triggers
        paused_tags = sum(1 for tag in tags if tag.get('paused', False))
        active_tags = total_tags - paused_tags
        
        return {
            'total_tags': total_tags,
            'active_tags': active_tags,
            'paused_tags': paused_tags,
            'tag_types': dict(tag_types),
            'destinations': dict(destinations),
            'unique_destinations': len(destinations)
        }
    
    def get_variables_summary(self) -> Dict:
        """
        Get comprehensive summary of variables in the GTM container.
        
        Returns:
            Dict: Summary containing variable counts and types
        """
        if not self.data:
            return {}
        
        variables = self.data.get('containerVersion', {}).get('variable', [])
        total_variables = len(variables)
        
        # Variable types breakdown
        variable_types = Counter()
        
        for variable in variables:
            var_type = variable.get('type', 'unknown')
            variable_types[var_type] += 1
        
        return {
            'total_variables': total_variables,
            'variable_types': dict(variable_types),
            'unique_variable_types': len(variable_types)
        }
    
    def get_triggers_summary(self) -> Dict:
        """
        Get comprehensive summary of triggers in the GTM container.
        
        Returns:
            Dict: Summary containing trigger counts and types
        """
        if not self.data:
            return {}
        
        triggers = self.data.get('containerVersion', {}).get('trigger', [])
        total_triggers = len(triggers)
        
        # Trigger types breakdown
        trigger_types = Counter()
        
        for trigger in triggers:
            trigger_type = trigger.get('type', 'unknown')
            trigger_types[trigger_type] += 1
        
        return {
            'total_triggers': total_triggers,
            'trigger_types': dict(trigger_types),
            'unique_trigger_types': len(trigger_types)
        }
    
    def get_tags_list(self) -> List[Dict]:
        """
        Get detailed list of all tags with their metadata.
        
        Returns:
            List[Dict]: List of tags with their properties
        """
        if not self.data:
            return []
        
        tags = self.data.get('containerVersion', {}).get('tag', [])
        tags_list = []
        
        for tag in tags:
            tag_info = {
                'name': tag.get('name', ''),
                'type': tag.get('type', ''),
                'tag_id': tag.get('tagId', ''),
                'paused': tag.get('paused', False),
                'firing_triggers': len(tag.get('firingTriggerId', [])),
                'blocking_triggers': len(tag.get('blockingTriggerId', [])),
                'parameters_count': len(tag.get('parameter', []))
            }
            
            # Extract destination information
            parameters = tag.get('parameter', [])
            destination = 'unknown'
            for param in parameters:
                if param.get('key') in ['measurementId', 'trackingId', 'containerId']:
                    destination = param.get('value', 'unknown')
                    break
            
            tag_info['destination'] = destination
            tags_list.append(tag_info)
        
        return tags_list
    
    def get_destination_analysis(self) -> Dict:
        """
        Analyze where data is being sent from this container.
        
        Returns:
            Dict: Analysis of data destinations and flows
        """
        if not self.data:
            return {}
        
        tags = self.data.get('containerVersion', {}).get('tag', [])
        destinations = defaultdict(list)
        
        for tag in tags:
            tag_name = tag.get('name', '')
            tag_type = tag.get('type', '')
            
            # Extract destination from parameters
            parameters = tag.get('parameter', [])
            destination = 'unknown'
            
            for param in parameters:
                key = param.get('key', '')
                if key in ['measurementId', 'trackingId', 'containerId', 'pixelId', 'advertiserId']:
                    destination = param.get('value', 'unknown')
                    break
            
            destinations[destination].append({
                'tag_name': tag_name,
                'tag_type': tag_type,
                'paused': tag.get('paused', False)
            })
        
        # Count active vs paused by destination
        destination_summary = {}
        for dest, tags_list in destinations.items():
            active_count = sum(1 for tag in tags_list if not tag['paused'])
            total_count = len(tags_list)
            
            destination_summary[dest] = {
                'total_tags': total_count,
                'active_tags': active_count,
                'paused_tags': total_count - active_count,
                'tag_types': list(set(tag['tag_type'] for tag in tags_list))
            }
        
        return {
            'destinations': dict(destinations),
            'destination_summary': destination_summary,
            'total_destinations': len(destinations)
        }
    
    def get_data_flow_analysis(self) -> Dict:
        """
        Analyze the data flow within the GTM container.
        
        Returns:
            Dict: Analysis of how data flows through tags, triggers, and variables
        """
        if not self.data:
            return {}
        
        container_version = self.data.get('containerVersion', {})
        tags = container_version.get('tag', [])
        triggers = container_version.get('trigger', [])
        variables = container_version.get('variable', [])
        
        # Create trigger ID to name mapping
        trigger_map = {trigger.get('triggerId'): trigger.get('name', '') for trigger in triggers}
        
        # Analyze tag-trigger relationships
        tag_trigger_relationships = []
        
        for tag in tags:
            tag_name = tag.get('name', '')
            firing_triggers = tag.get('firingTriggerId', [])
            blocking_triggers = tag.get('blockingTriggerId', [])
            
            tag_trigger_relationships.append({
                'tag_name': tag_name,
                'firing_triggers': [trigger_map.get(tid, f'Unknown_{tid}') for tid in firing_triggers],
                'blocking_triggers': [trigger_map.get(tid, f'Unknown_{tid}') for tid in blocking_triggers],
                'total_conditions': len(firing_triggers) + len(blocking_triggers)
            })
        
        # Most used triggers
        all_trigger_usage = []
        for tag in tags:
            all_trigger_usage.extend(tag.get('firingTriggerId', []))
            all_trigger_usage.extend(tag.get('blockingTriggerId', []))
        
        trigger_usage_count = Counter(all_trigger_usage)
        most_used_triggers = [
            {'trigger_name': trigger_map.get(tid, f'Unknown_{tid}'), 'usage_count': count}
            for tid, count in trigger_usage_count.most_common(10)
        ]
        
        return {
            'tag_trigger_relationships': tag_trigger_relationships,
            'most_used_triggers': most_used_triggers,
            'total_relationships': len(tag_trigger_relationships),
            'avg_conditions_per_tag': sum(rel['total_conditions'] for rel in tag_trigger_relationships) / len(tag_trigger_relationships) if tag_trigger_relationships else 0
        }
    
    def get_platform_overview(self) -> Dict:
        """
        Get high-level overview metrics for the dashboard.
        
        Returns:
            Dict: Platform overview with key metrics
        """
        container_info = self.get_container_info()
        tags_summary = self.get_tags_summary()
        variables_summary = self.get_variables_summary()
        triggers_summary = self.get_triggers_summary()
        destination_analysis = self.get_destination_analysis()
        
        return {
            'platform': f"GTM ({container_info.get('container_type', 'unknown')})",
            'container_name': container_info.get('container_name', ''),
            'public_id': container_info.get('public_id', ''),
            'total_tags': tags_summary.get('total_tags', 0),
            'active_tags': tags_summary.get('active_tags', 0),
            'paused_tags': tags_summary.get('paused_tags', 0),
            'total_variables': variables_summary.get('total_variables', 0),
            'total_triggers': triggers_summary.get('total_triggers', 0),
            'total_destinations': destination_analysis.get('total_destinations', 0),
            'container_type': container_info.get('container_type', 'unknown'),
            'last_updated': container_info.get('export_time', '')
        } 