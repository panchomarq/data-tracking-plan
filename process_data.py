import sys
from services.parser_manager import parser_manager

def main():
    """
    Process data using the centralized ParserManager.
    """
    # Get Amplitude parser
    parser = parser_manager.get_parser('amplitude')
    
    if not parser:
        print("Error: Amplitude parser not initialized.")
        sys.exit(1)
        
    # Get events list directly from parser
    events = parser.get_events_list()
    
    # Extract unique names
    unique_names = sorted(list(set(e['name'] for e in events)))
    
    # Get counts
    events_summary = parser.get_events_summary()
    properties_summary = parser.get_properties_summary()
    
    print("Unique Event Display Names:")
    for name in unique_names:
       print(name)

    print('\nProperties summary:')
    print(f"Total Properties: {properties_summary['total_properties']}")
    print(f"Unique Properties: {properties_summary['unique_properties']}")

    print(f"\nTotal Events: {events_summary['total_events']}")

if __name__ == "__main__":
    main()
