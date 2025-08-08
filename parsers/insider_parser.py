import json
from typing import Dict, List, Set
from collections import Counter, defaultdict

class InsiderParser:
    """
    Parser for Insider JSON data containing event definitions and parameters.
    """
    
    def __init__(self, file_path: str):
        """
        Initialize the parser with the path to the Insider JSON file.
        
        Args:
            file_path (str): Path to the Insider JSON file
        """
        self.file_path = file_path
        self.data = None
        self._load_data()
    
    def _load_data(self):
        """
        Load the JSON data into memory for processing.
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                self.data = json.load(file)
        except Exception as e:
            raise Exception(f"Error loading Insider data: {e}")
    
    def get_events_summary(self) -> Dict:
        """
        Get comprehensive summary of events in Insider.
        
        Returns:
            Dict: Summary containing event counts, categories, and parameter breakdown
        """
        if not self.data:
            return {}
        
        total_events = len(self.data)
        
        # Events with categories
        categorized_events = sum(1 for event in self.data if event.get('category'))
        
        # Events with PII parameters
        pii_events = 0
        for event in self.data:
            if any(param.get('is_pii', False) for param in event.get('params', [])):
                pii_events += 1
        
        # Events with segmentation parameters
        segmentation_events = 0
        for event in self.data:
            if any(param.get('show_on_segment', False) for param in event.get('params', [])):
                segmentation_events += 1
        
        # Categories breakdown
        categories = Counter()
        for event in self.data:
            category = event.get('category', 'Uncategorized')
            if category:
                categories[category] += 1
            else:
                categories['Uncategorized'] += 1
        
        return {
            'total_events': total_events,
            'categorized_events': categorized_events,
            'pii_events': pii_events,
            'segmentation_events': segmentation_events,
            'categories': dict(categories)
        }
    
    def get_properties_summary(self) -> Dict:
        """
        Get comprehensive summary of event parameters in Insider.
        
        Returns:
            Dict: Summary containing parameter counts, types, and characteristics
        """
        if not self.data:
            return {}
        
        all_params = []
        for event in self.data:
            all_params.extend(event.get('params', []))
        
        total_properties = len(all_params)
        
        # Unique parameter names
        unique_params = set(param.get('key', '') for param in all_params)
        unique_properties = len(unique_params)
        
        # Parameter types breakdown
        param_types = Counter(param.get('type', 'unknown') for param in all_params)
        
        # PII parameters
        pii_params = sum(1 for param in all_params if param.get('is_pii', False))
        
        # Segmentation parameters
        segmentation_params = sum(1 for param in all_params if param.get('show_on_segment', False))
        
        # Parameters with display names
        named_params = sum(1 for param in all_params if param.get('display_name'))
        
        return {
            'total_properties': total_properties,
            'unique_properties': unique_properties,
            'param_types': dict(param_types),
            'pii_params': pii_params,
            'segmentation_params': segmentation_params,
            'named_params': named_params,
            'unnamed_params': total_properties - named_params
        }
    
    def get_events_list(self) -> List[Dict]:
        """
        Get detailed list of all events with their metadata.
        
        Returns:
            List[Dict]: List of events with their properties
        """
        if not self.data:
            return []
        
        events_list = []
        for event in self.data:
            event_info = {
                'key': event.get('key', ''),
                'display_name': event.get('display_name', ''),
                'category': event.get('category', ''),
                'is_pii': event.get('is_pii', False),
                'params_count': len(event.get('params', [])),
                'pii_params_count': sum(1 for p in event.get('params', []) if p.get('is_pii', False)),
                'segmentation_params_count': sum(1 for p in event.get('params', []) if p.get('show_on_segment', False))
            }
            events_list.append(event_info)
        
        return events_list
    
    def get_parameters_by_event(self) -> Dict[str, List[Dict]]:
        """
        Get parameters grouped by their associated events.
        
        Returns:
            Dict[str, List[Dict]]: Events as keys, lists of parameters as values
        """
        if not self.data:
            return {}
        
        events_params = {}
        
        for event in self.data:
            event_key = event.get('key', '')
            params_list = []
            
            for param in event.get('params', []):
                param_info = {
                    'key': param.get('key', ''),
                    'display_name': param.get('display_name', ''),
                    'type': param.get('type', ''),
                    'is_pii': param.get('is_pii', False),
                    'show_on_segment': param.get('show_on_segment', False)
                }
                params_list.append(param_info)
            
            events_params[event_key] = params_list
        
        return events_params
    
    def get_all_parameters_detailed(self) -> List[Dict]:
        """
        Get comprehensive list of all parameters with detailed information.
        
        Returns:
            List[Dict]: List of all parameters with their complete details
        """
        if not self.data:
            return []
        
        all_parameters = []
        
        for event in self.data:
            event_key = event.get('key', '')
            event_display_name = event.get('display_name', '')
            
            for param in event.get('params', []):
                param_detail = {
                    'key': param.get('key', ''),
                    'display_name': param.get('display_name', ''),
                    'type': param.get('type', ''),
                    'is_pii': param.get('is_pii', False),
                    'show_on_segment': param.get('show_on_segment', False),
                    'event_key': event_key,
                    'event_display_name': event_display_name,
                    'event_category': event.get('category', '')
                }
                all_parameters.append(param_detail)
        
        return all_parameters

    def get_unique_parameters_list(self) -> List[Dict]:
        """
        Get a list of unique parameters with aggregated information.
        
        Returns:
            List[Dict]: List of unique parameters with usage details
        """
        if not self.data:
            return []
        
        # Collect all parameter instances
        param_instances = defaultdict(list)
        
        for event in self.data:
            event_key = event.get('key', '')
            event_display_name = event.get('display_name', '')
            
            for param in event.get('params', []):
                param_key = param.get('key', '')
                param_instances[param_key].append({
                    'display_name': param.get('display_name', ''),
                    'type': param.get('type', ''),
                    'is_pii': param.get('is_pii', False),
                    'show_on_segment': param.get('show_on_segment', False),
                    'event_key': event_key,
                    'event_display_name': event_display_name,
                    'event_category': event.get('category', '')
                })
        
        # Create unique parameter list
        unique_parameters = []
        
        for param_key, instances in param_instances.items():
            # Get the most common values for aggregation
            display_names = [inst['display_name'] for inst in instances if inst['display_name']]
            types = [inst['type'] for inst in instances]
            pii_statuses = [inst['is_pii'] for inst in instances]
            segment_statuses = [inst['show_on_segment'] for inst in instances]
            
            # Determine representative values
            most_common_display_name = max(set(display_names), key=display_names.count) if display_names else ''
            most_common_type = max(set(types), key=types.count) if types else 'unknown'
            has_pii = any(pii_statuses)
            has_segment = any(segment_statuses)
            
            # Check if values are consistent across events
            is_type_consistent = len(set(types)) <= 1
            is_pii_consistent = len(set(pii_statuses)) <= 1
            is_segment_consistent = len(set(segment_statuses)) <= 1
            
            unique_param = {
                'key': param_key,
                'display_name': most_common_display_name,
                'type': most_common_type,
                'is_pii': has_pii,
                'show_on_segment': has_segment,
                'usage_count': len(instances),
                'events_list': [inst['event_key'] for inst in instances],
                'is_type_consistent': is_type_consistent,
                'is_pii_consistent': is_pii_consistent,
                'is_segment_consistent': is_segment_consistent,
                'all_instances': instances
            }
            
            unique_parameters.append(unique_param)
        
        # Sort by usage count (most used first)
        unique_parameters.sort(key=lambda x: x['usage_count'], reverse=True)
        
        return unique_parameters
    
    def get_parameter_usage_analysis(self) -> Dict:
        """
        Analyze parameter usage across events.
        
        Returns:
            Dict: Analysis of parameter reuse and patterns
        """
        if not self.data:
            return {}
        
        # Count parameter usage across events
        param_usage = defaultdict(list)
        param_details = defaultdict(list)
        
        for event in self.data:
            event_key = event.get('key', '')
            for param in event.get('params', []):
                param_key = param.get('key', '')
                param_usage[param_key].append(event_key)
                param_details[param_key].append({
                    'event_key': event_key,
                    'event_display_name': event.get('display_name', ''),
                    'display_name': param.get('display_name', ''),
                    'type': param.get('type', ''),
                    'is_pii': param.get('is_pii', False),
                    'show_on_segment': param.get('show_on_segment', False)
                })
        
        # Find reused parameters
        reused_params = {k: v for k, v in param_usage.items() if len(v) > 1}
        unique_params = {k: v for k, v in param_usage.items() if len(v) == 1}
        
        # Most common parameters
        most_common = sorted(param_usage.items(), key=lambda x: len(x[1]), reverse=True)[:20]
        
        return {
            'total_unique_params': len(param_usage),
            'reused_params_count': len(reused_params),
            'unique_params_count': len(unique_params),
            'most_common_params': [{'param': k, 'events_count': len(v)} for k, v in most_common],
            'reused_params': {k: len(v) for k, v in reused_params.items()},
            'param_details': dict(param_details)
        }
    
    def get_parameter_type_analysis(self) -> Dict:
        """
        Analyze parameter types and their distribution.
        
        Returns:
            Dict: Analysis of parameter types across events
        """
        if not self.data:
            return {}
        
        type_analysis = defaultdict(lambda: {
            'count': 0,
            'pii_count': 0,
            'segmentation_count': 0,
            'events': set()
        })
        
        for event in self.data:
            event_key = event.get('key', '')
            for param in event.get('params', []):
                param_type = param.get('type', 'unknown')
                type_analysis[param_type]['count'] += 1
                type_analysis[param_type]['events'].add(event_key)
                
                if param.get('is_pii', False):
                    type_analysis[param_type]['pii_count'] += 1
                    
                if param.get('show_on_segment', False):
                    type_analysis[param_type]['segmentation_count'] += 1
        
        # Convert sets to counts for JSON serialization
        result = {}
        for param_type, data in type_analysis.items():
            result[param_type] = {
                'count': data['count'],
                'pii_count': data['pii_count'],
                'segmentation_count': data['segmentation_count'],
                'events_count': len(data['events'])
            }
        
        return result
    
    def get_platform_overview(self) -> Dict:
        """
        Get high-level overview metrics for the dashboard.
        
        Returns:
            Dict: Platform overview with key metrics
        """
        events_summary = self.get_events_summary()
        properties_summary = self.get_properties_summary()
        
        return {
            'platform': 'Insider',
            'total_events': events_summary['total_events'],
            'total_properties': properties_summary['total_properties'],
            'unique_properties': properties_summary['unique_properties'],
            'pii_events': events_summary['pii_events'],
            'segmentation_events': events_summary['segmentation_events'],
            'categories_count': len(events_summary['categories']),
            'last_updated': 'Data export timestamp not available'
        } 