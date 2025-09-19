import csv
import json

def get_unique_event_display_names(file_path):
    """
    Reads a CSV file and extracts all unique values from the 'Object Name' column.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        list: A list of unique event display names.
    """
    event_display_names = set()
    with open(file_path, mode='r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            if 'Object Name' in row and row['Object Name']:
                event_display_names.add(row['Object Name'])
    return sorted(list(event_display_names))

def get_count_of_events_by_display_name(file_path):
    """
    Reads a CSV file and counts the number of events for each display name.

    Args:
        file_path (str): The path to the CSV file.
    """
    with open(file_path, mode='r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        total_events = 0
        
        for row in reader:
            if 'Object Name' in row and row['Object Name']:
                total_events += 1
        
        return total_events

def get_count_of_event_properties(file_path):
    """
    Reads a CSV file and counts the number of event properties.
    """
    with open(file_path, mode='r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        total_properties = 0

        unique_properties = set()
        
        for row in reader:
            if 'Event Property Name' in row and row['Event Property Name']:
                unique_properties.add(row['Event Property Name'])
        
        total_properties = len(unique_properties)
    
    return total_properties

if __name__ == "__main__":
    csv_file = 'amplitude_events.csv'
    unique_names = get_unique_event_display_names(csv_file)
    event_count = get_count_of_events_by_display_name(csv_file)
    event_properties_count = get_count_of_event_properties(csv_file)

    print("Unique Event Display Names:")
    for name in unique_names:
       print(name)

    print('Properties names:')
    for property in event_properties_count:
        print(property)

    print("Total Events: ", event_count)
    print("Total Event Properties: ", event_properties_count)

    #print("Unique Event Display Names: ", unique_names)


    # Example of how you might output to JSON
    # with open('unique_event_names.json', 'w', encoding='utf-8') as outfile:
    #     json.dump(unique_names, outfile, indent=4) 