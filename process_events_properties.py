#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Property Extractor for Data Tracking Plan

This script extracts and combines property data from Amplitude and Insider using the centralized parsers,
formatting them to match the Google Sheet structure shown in the tracking plan.
"""

import pandas as pd
from typing import Dict, List, Set, Any
from services.parser_manager import parser_manager

def extract_amplitude_properties(parser) -> Set[str]:
    """
    Extract event property names from Amplitude using the initialized parser.
    
    Args:
        parser: Initialized AmplitudeParser instance
        
    Returns:
        Set of unique property names
    """
    properties = set()
    if not parser or parser.data is None:
        print("Amplitude parser not initialized or no data.")
        return properties
        
    df = parser.data
    
    try:
        # Process Event Properties
        if 'Property Type' in df.columns and 'Event Property Name' in df.columns:
            # Filter for Event Properties
            event_props = df[df['Property Type'] == 'Event Property']['Event Property Name'].dropna()
            for name in event_props:
                if is_valid_property_name(name):
                    properties.add(name)
        
        # Process Event Display Names (special format like [Guides-Surveys])
        if 'Event Display Name' in df.columns:
            display_names = df['Event Display Name'].dropna()
            for name in display_names:
                if (isinstance(name, str) and 
                    '[' in name and 
                    ']' in name and
                    is_valid_property_name(name)):
                    properties.add(name)
                    
    except Exception as e:
        print(f"Error processing Amplitude data: {e}")
    
    return properties


def is_valid_property_name(name: str) -> bool:
    """
    Check if a string is a valid property name.
    
    Args:
        name: String to validate
        
    Returns:
        True if it's a valid property name, False otherwise
    """
    if not name or not isinstance(name, str):
        return False
    
    name = name.strip()
    
    # Skip empty strings
    if not name:
        return False
    
    # Skip very long strings (likely IDs or encoded data)
    if len(name) > 200:
        return False
    
    # Skip strings that look like encoded IDs or hashes
    if len(name) > 50 and any(char in name for char in ['/', '%', '&', '=', '+', '?']):
        return False
    
    # Skip strings that are mostly numbers and special characters
    alphanumeric_count = sum(1 for char in name if char.isalnum() or char in [' ', '_', '-', '[', ']'])
    if len(name) > 10 and alphanumeric_count / len(name) < 0.7:
        return False
    
    return True


def extract_insider_properties(parser) -> Set[str]:
    """
    Extract property keys from Insider using the initialized parser.
    
    Args:
        parser: Initialized InsiderParser instance
        
    Returns:
        Set of unique property keys
    """
    properties = set()
    if not parser or parser.data is None:
        print("Insider parser not initialized or no data.")
        return properties
        
    data = parser.data
    
    try:
        # Iterate through each event in the JSON data
        for event in data:
            # Check if the event has a display_name with special format
            if ('display_name' in event and 
                '[' in event['display_name'] and 
                ']' in event['display_name'] and
                is_valid_property_name(event['display_name'])):
                properties.add(event['display_name'])
                
            # Extract event key if it has special format
            if ('key' in event and 
                '[' in event['key'] and 
                ']' in event['key'] and
                is_valid_property_name(event['key'])):
                properties.add(event['key'])
                
            # Check for params list which contains properties
            if 'params' in event and isinstance(event['params'], list):
                for param in event['params']:
                    # Extract the property key
                    if ('key' in param and 
                        param['key'].strip() and
                        is_valid_property_name(param['key'])):
                        properties.add(param['key'])
                        
                    # Extract the display_name if it has special format
                    if ('display_name' in param and 
                        param['display_name'].strip() and
                        '[' in param['display_name'] and 
                        ']' in param['display_name'] and
                        is_valid_property_name(param['display_name'])):
                        properties.add(param['display_name'])
    except Exception as e:
        print(f"Error processing Insider data: {e}")
    
    return properties


def identify_property_sources(amplitude_properties: Set[str], insider_properties: Set[str]) -> Dict[str, str]:
    """
    Identify the source of each property.
    
    Args:
        amplitude_properties: Set of properties from Amplitude
        insider_properties: Set of properties from Insider
        
    Returns:
        Dictionary mapping property names to their source
    """
    property_sources = {}
    
    # Process properties from both sources
    for prop in amplitude_properties:
        property_sources[prop] = "Amplitude"
        
    for prop in insider_properties:
        if prop in property_sources:
            property_sources[prop] = "Amplitude, Insider"
        else:
            property_sources[prop] = "Insider"
            
    return property_sources


def generate_property_rows(property_sources: Dict[str, str]) -> List[Dict[str, str]]:
    """
    Generate rows for the Google Sheet format.
    
    Args:
        property_sources: Dictionary mapping property names to their sources
        
    Returns:
        List of dictionaries representing rows for the sheet
    """
    rows = []
    for prop, source in sorted(property_sources.items()):
        # Create a row with default values
        row = {
            "Property ID": "",
            "Estatus": "No implementado",
            "Property Name": prop,
            "dataLayer name": prop,  # Default to same name
            "Property Description": "",
            "Grupo": "",
            "Property Type": "",  # Can be set based on naming convention if needed
            "Tipo de datos": "String",  # Default to String
            "Ejemplo de respuesta": "",
            "Front/Back": "",
            "Fuente": source
        }
        rows.append(row)
    
    return rows


def save_to_csv(rows: List[Dict[str, str]], output_path: str) -> None:
    """
    Save the formatted rows to a CSV file.
    
    Args:
        rows: List of row dictionaries
        output_path: Output CSV file path
    """
    if not rows:
        print("No rows to save.")
        return
    
    # Define column order based on the Google Sheet structure
    columns = [
        "Property ID", "Estatus", "Property Name", "dataLayer name", 
        "Property Description", "Grupo", "Property Type", 
        "Tipo de datos", "Ejemplo de respuesta", "Front/Back", "Fuente"
    ]
    
    # Create DataFrame and save to CSV
    df = pd.DataFrame(rows)
    df = df[columns]  # Ensure columns are in correct order
    df.to_csv(output_path, index=False, encoding='utf-8')
    print(f"Saved {len(rows)} properties to {output_path}")


def generate_html_table(rows: List[Dict[str, str]], output_path: str) -> None:
    """
    Generate HTML table format for easy copying to Google Sheets.
    
    Args:
        rows: List of row dictionaries
        output_path: Output HTML file path
    """
    # Define column order based on the Google Sheet structure
    columns = [
        "Property ID", "Estatus", "Property Name", "dataLayer name", 
        "Property Description", "Grupo", "Property Type", 
        "Tipo de datos", "Ejemplo de respuesta", "Front/Back"
    ]
    
    # Create DataFrame
    df = pd.DataFrame(rows)
    df = df[columns]  # Ensure columns are in correct order
    
    # Generate HTML table with styling for easy copying
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Property Tracking Plan</title>
        <style>
            table {
                border-collapse: collapse;
                width: 100%;
            }
            th, td {
                border: 1px solid #dddddd;
                text-align: left;
                padding: 8px;
            }
            th {
                background-color: #f2f2f2;
            }
            tr:nth-child(even) {
                background-color: #f9f9f9;
            }
            .copy-button {
                margin: 10px 0;
                padding: 8px 16px;
                background-color: #4CAF50;
                color: white;
                border: none;
                cursor: pointer;
            }
            .copy-instructions {
                margin-bottom: 20px;
            }
        </style>
    </head>
    <body>
        <h1>Property Tracking Plan</h1>
        <div class="copy-instructions">
            <p>Para copiar esta tabla a Google Sheets:</p>
            <ol>
                <li>Haz clic en el botón "Copiar tabla al portapapeles"</li>
                <li>En Google Sheets, selecciona la celda donde quieres pegar</li>
                <li>Pega con Ctrl+V (o Cmd+V en Mac)</li>
            </ol>
        </div>
        <button class="copy-button" onclick="copyTableToClipboard()">Copiar tabla al portapapeles</button>
        
        <div id="table-container">
    """
    
    # Add the HTML table
    html_content += df.to_html(index=False)
    
    # Add JavaScript for copying to clipboard
    html_content += """
        </div>

        <script>
            function copyTableToClipboard() {
                const table = document.querySelector('table');
                const range = document.createRange();
                range.selectNode(table);
                window.getSelection().removeAllRanges();
                window.getSelection().addRange(range);
                document.execCommand('copy');
                window.getSelection().removeAllRanges();
                alert('Tabla copiada al portapapeles. Ahora puedes pegarla en Google Sheets.');
            }
        </script>
    </body>
    </html>
    """
    
    # Write to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"HTML table saved to {output_path}")


def main():
    output_csv_path = 'property_tracking_plan.csv'
    
    # Extract properties from both sources using centralized parsers
    print("Extracting properties from Amplitude...")
    amplitude_parser = parser_manager.get_parser('amplitude')
    amplitude_properties = extract_amplitude_properties(amplitude_parser)
    print(f"Found {len(amplitude_properties)} unique properties in Amplitude")
    
    print("Extracting properties from Insider...")
    insider_parser = parser_manager.get_parser('insider')
    insider_properties = extract_insider_properties(insider_parser)
    print(f"Found {len(insider_properties)} unique properties in Insider")
    
    # Get property sources
    property_sources = identify_property_sources(amplitude_properties, insider_properties)
    print(f"Combined total: {len(property_sources)} unique properties")
    
    # Generate rows for the Google Sheet format
    rows = generate_property_rows(property_sources)
    
    # Save to CSV
    save_to_csv(rows, output_csv_path)
    
    print("Done! CSV file generated at:")
    print(f"- {output_csv_path}")


if __name__ == "__main__":
    main()
