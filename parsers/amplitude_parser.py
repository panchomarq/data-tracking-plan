import csv
import pandas as pd
from typing import Dict, List
from collections import defaultdict

class AmplitudeParser:
    """
    Parser for Amplitude CSV export data containing events and properties metadata.
    """
    
    def __init__(self, file_path: str):
        """
        Initialize the parser with the path to the Amplitude CSV file.
        
        Args:
            file_path (str): Path to the Amplitude CSV export file
        """
        self.file_path = file_path
        self.data = None
        self._load_data()
    
    def _load_data(self):
        """
        Load the CSV data into a pandas DataFrame for efficient processing.
        """
        try:
            self.data = pd.read_csv(self.file_path)
        except Exception as e:
            raise Exception(f"Error loading Amplitude data: {e}")
    
    def get_events_summary(self) -> Dict:
        """
        Get comprehensive summary of events in Amplitude.
        
        Returns:
            Dict: Summary containing event counts, categories, and status breakdown
        """
        # Filter rows that represent events (not property groups or properties)
        events_df = self.data[
            (self.data['Object Type'] == 'Event') & 
            (self.data['Object Name'].notna()) &
            (self.data['Object Name'] != '')
        ]
        
        total_events = len(events_df)
        
        # Event activity status breakdown
        activity_status = events_df['Event Activity'].value_counts().to_dict()
        
        # Event categories breakdown
        categories = events_df['Event Category'].value_counts().to_dict()
        
        # Schema status breakdown
        schema_status = events_df['Event Schema Status'].value_counts().to_dict()
        
        # Events by owner
        owners = events_df['Object Owner'].value_counts().head(10).to_dict()
        
        return {
            'total_events': total_events,
            'activity_status': activity_status,
            'categories': categories,
            'schema_status': schema_status,
            'top_owners': owners,
            'unique_event_names': events_df['Object Name'].nunique()
        }
    
    def get_properties_summary(self) -> Dict:
        """
        Get comprehensive summary of event properties in Amplitude.
        
        Returns:
            Dict: Summary containing property counts, types, and validation info
        """
        # Filter rows that represent properties
        properties_df = self.data[
            (self.data['Event Property Name'].notna()) & 
            (self.data['Event Property Name'] != '')
        ]
        
        total_properties = len(properties_df)
        unique_properties = properties_df['Event Property Name'].nunique()
        
        # Property value types breakdown
        value_types = properties_df['Property Value Type'].value_counts().to_dict()
        
        # Required vs optional properties
        required_breakdown = properties_df['Property Required'].value_counts().to_dict()
        
        # Schema status for properties
        property_schema_status = properties_df['Property Schema Status'].value_counts().to_dict()
        
        # Array properties
        array_properties = properties_df[properties_df['Property Is Array'] == True]
        
        return {
            'total_properties': total_properties,
            'unique_properties': unique_properties,
            'value_types': value_types,
            'required_breakdown': required_breakdown,
            'schema_status': property_schema_status,
            'array_properties_count': len(array_properties)
        }
    
    def get_events_list(self) -> List[Dict]:
        """
        Get detailed list of all events with their metadata.
        
        Returns:
            List[Dict]: List of events with their properties
        """
        events_df = self.data[
            (self.data['Object Type'] == 'Event') & 
            (self.data['Object Name'].notna()) &
            (self.data['Object Name'] != '')
        ]
        
        events_list = []
        for _, row in events_df.iterrows():
            event = {
                'name': row['Object Name'],
                'display_name': row.get('Event Display Name', ''),
                'category': row.get('Event Category', ''),
                'owner': row.get('Object Owner', ''),
                'description': row.get('Object Description', ''),
                'activity': row.get('Event Activity', ''),
                'schema_status': row.get('Event Schema Status', ''),
                'volume_180_days': row.get('Event 180 Day Volume', 0),
                'queries_180_days': row.get('Event 180 Day Queries', 0),
                'first_seen': row.get('Event First Seen', ''),
                'last_seen': row.get('Event Last Seen', '')
            }
            events_list.append(event)
        
        return events_list
    
    def get_properties_by_event(self) -> Dict[str, List[Dict]]:
        """
        Get properties grouped by their associated events.
        
        Returns:
            Dict[str, List[Dict]]: Events as keys, lists of properties as values
        """
        properties_df = self.data[
            (self.data['Event Property Name'].notna()) & 
            (self.data['Event Property Name'] != '') &
            (self.data['Object Name'].notna()) &
            (self.data['Object Name'] != '')
        ]
        
        events_properties = defaultdict(list)
        
        for _, row in properties_df.iterrows():
            event_name = row['Object Name']
            property_info = {
                'name': row['Event Property Name'],
                'description': row.get('Property Description', ''),
                'type': row.get('Property Value Type', ''),
                'required': row.get('Property Required', False),
                'is_array': row.get('Property Is Array', False),
                'schema_status': row.get('Property Schema Status', ''),
                'first_seen': row.get('Property First Seen', ''),
                'last_seen': row.get('Property Last Seen', '')
            }
            events_properties[event_name].append(property_info)
        
        return dict(events_properties)
    
    def get_platform_overview(self) -> Dict:
        """
        Get high-level overview metrics for the dashboard.
        
        Returns:
            Dict: Platform overview with key metrics
        """
        events_summary = self.get_events_summary()
        properties_summary = self.get_properties_summary()
        
        return {
            'platform': 'Amplitude',
            'total_events': events_summary['total_events'],
            'total_properties': properties_summary['total_properties'],
            'unique_properties': properties_summary['unique_properties'],
            'active_events': events_summary['activity_status'].get('ACTIVE', 0),
            'deleted_events': events_summary['activity_status'].get('DELETED', 0),
            'categories_count': len(events_summary['categories']),
            'last_updated': 'July 17, 2025'  # Based on filename timestamp
        } 