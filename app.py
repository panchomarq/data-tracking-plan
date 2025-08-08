from flask import Flask, render_template, jsonify
from config import Config
from parsers.amplitude_parser import AmplitudeParser
from parsers.insider_parser import InsiderParser
from parsers.gtm_parser import GTMParser

app = Flask(__name__)
app.config.from_object(Config)

def initialize_parsers():
    """
    Initialize all data parsers with their respective data sources.
    
    Returns:
        Dict: Dictionary containing initialized parsers
    """
    parsers = {}
    
    try:
        # Initialize Amplitude parser
        parsers['amplitude'] = AmplitudeParser(str(Config.AMPLITUDE_CSV))
        print("✓ Amplitude parser initialized successfully")
    except Exception as e:
        print(f"✗ Error initializing Amplitude parser: {e}")
        parsers['amplitude'] = None
    
    try:
        # Initialize Insider parser
        parsers['insider'] = InsiderParser(str(Config.INSIDER_JSON))
        print("✓ Insider parser initialized successfully")
    except Exception as e:
        print(f"✗ Error initializing Insider parser: {e}")
        parsers['insider'] = None
    
    try:
        # Initialize GTM Server-side parser
        parsers['gtm_server'] = GTMParser(str(Config.GTM_SERVER_JSON))
        print("✓ GTM Server-side parser initialized successfully")
    except Exception as e:
        print(f"✗ Error initializing GTM Server-side parser: {e}")
        parsers['gtm_server'] = None
    
    try:
        # Initialize GTM Client-side parser
        parsers['gtm_client'] = GTMParser(str(Config.GTM_CLIENT_JSON))
        print("✓ GTM Client-side parser initialized successfully")
    except Exception as e:
        print(f"✗ Error initializing GTM Client-side parser: {e}")
        parsers['gtm_client'] = None
    
    return parsers

# Initialize parsers at startup
parsers = initialize_parsers()

@app.route('/')
def dashboard():
    """
    Main dashboard route showing overview of all platforms.
    """
    platform_overviews = []
    
    # Get overview from each platform
    if parsers['amplitude']:
        platform_overviews.append(parsers['amplitude'].get_platform_overview())
    
    if parsers['insider']:
        platform_overviews.append(parsers['insider'].get_platform_overview())
    
    if parsers['gtm_server']:
        platform_overviews.append(parsers['gtm_server'].get_platform_overview())
    
    if parsers['gtm_client']:
        platform_overviews.append(parsers['gtm_client'].get_platform_overview())
    
    return render_template('dashboard.html', platforms=platform_overviews)

@app.route('/amplitude')
def amplitude_detail():
    """
    Detailed view of Amplitude data.
    """
    if not parsers['amplitude']:
        return render_template('error.html', message="Amplitude data not available")
    
    parser = parsers['amplitude']
    
    data = {
        'overview': parser.get_platform_overview(),
        'events_summary': parser.get_events_summary(),
        'properties_summary': parser.get_properties_summary(),
        'events_list': parser.get_events_list()[:50],  # Limit for display
        'properties_by_event': dict(list(parser.get_properties_by_event().items())[:10])  # Top 10 events
    }
    
    return render_template('amplitude.html', data=data)

@app.route('/insider')
def insider_detail():
    """
    Detailed view of Insider data.
    """
    if not parsers['insider']:
        return render_template('error.html', message="Insider data not available")
    
    parser = parsers['insider']
    
    data = {
        'overview': parser.get_platform_overview(),
        'events_summary': parser.get_events_summary(),
        'properties_summary': parser.get_properties_summary(),
        'events_list': parser.get_events_list(),  # Show all events
        'parameter_usage': parser.get_parameter_usage_analysis(),
        'parameters_by_event': parser.get_parameters_by_event(),  # Show all events with parameters
        'all_parameters': parser.get_all_parameters_detailed(),
        'unique_parameters_list': parser.get_unique_parameters_list(),  # New unique parameters list
        'parameter_type_analysis': parser.get_parameter_type_analysis()
    }
    
    return render_template('insider.html', data=data)

@app.route('/gtm')
def gtm_overview():
    """
    Overview of both GTM containers.
    """
    gtm_data = {}
    
    if parsers['gtm_server']:
        gtm_data['server'] = {
            'overview': parsers['gtm_server'].get_platform_overview(),
            'tags_summary': parsers['gtm_server'].get_tags_summary(),
            'variables_summary': parsers['gtm_server'].get_variables_summary(),
            'triggers_summary': parsers['gtm_server'].get_triggers_summary(),
            'destination_analysis': parsers['gtm_server'].get_destination_analysis()
        }
    
    if parsers['gtm_client']:
        gtm_data['client'] = {
            'overview': parsers['gtm_client'].get_platform_overview(),
            'tags_summary': parsers['gtm_client'].get_tags_summary(),
            'variables_summary': parsers['gtm_client'].get_variables_summary(),
            'triggers_summary': parsers['gtm_client'].get_triggers_summary(),
            'destination_analysis': parsers['gtm_client'].get_destination_analysis()
        }
    
    return render_template('gtm.html', data=gtm_data)

@app.route('/gtm/<container_type>')
def gtm_detail(container_type):
    """
    Detailed view of specific GTM container.
    """
    parser_key = f'gtm_{container_type}'
    
    if parser_key not in parsers or not parsers[parser_key]:
        return render_template('error.html', message=f"GTM {container_type} data not available")
    
    parser = parsers[parser_key]
    
    data = {
        'overview': parser.get_platform_overview(),
        'container_info': parser.get_container_info(),
        'tags_summary': parser.get_tags_summary(),
        'variables_summary': parser.get_variables_summary(),
        'triggers_summary': parser.get_triggers_summary(),
        'tags_list': parser.get_tags_list()[:50],  # Limit for display
        'destination_analysis': parser.get_destination_analysis(),
        'data_flow': parser.get_data_flow_analysis()
    }
    
    return render_template('gtm_detail.html', data=data, container_type=container_type)

# API Routes for dynamic data loading
@app.route('/api/amplitude/events')
def api_amplitude_events():
    """
    API endpoint to get Amplitude events data.
    """
    if not parsers['amplitude']:
        return jsonify({'error': 'Amplitude data not available'}), 404
    
    return jsonify(parsers['amplitude'].get_events_list())

@app.route('/api/insider/events')
def api_insider_events():
    """
    API endpoint to get Insider events data.
    """
    if not parsers['insider']:
        return jsonify({'error': 'Insider data not available'}), 404
    
    return jsonify(parsers['insider'].get_events_list())

@app.route('/api/gtm/<container_type>/tags')
def api_gtm_tags(container_type):
    """
    API endpoint to get GTM tags data.
    """
    parser_key = f'gtm_{container_type}'
    
    if parser_key not in parsers or not parsers[parser_key]:
        return jsonify({'error': f'GTM {container_type} data not available'}), 404
    
    return jsonify(parsers[parser_key].get_tags_list())

@app.errorhandler(404)
def not_found(error):
    """
    404 error handler.
    """
    return render_template('error.html', message="Page not found"), 404

@app.errorhandler(500)
def internal_error(error):
    """
    500 error handler.
    """
    return render_template('error.html', message="Internal server error"), 500

if __name__ == '__main__':
    print("🚀 Starting Data Tracking Plan Dashboard...")
    print("📊 Available platforms:")
    
    for platform, parser in parsers.items():
        status = "✓ Ready" if parser else "✗ Error"
        print(f"   - {platform}: {status}")
    
    print("\n🌐 Dashboard will be available at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000) 