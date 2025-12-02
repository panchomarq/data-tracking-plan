from flask import Blueprint, render_template
from services.parser_manager import parser_manager

web_bp = Blueprint('web', __name__)

@web_bp.route('/')
def dashboard():
    """
    Main dashboard route showing overview of all platforms.
    """
    platform_overviews = []
    parsers = parser_manager.get_all_parsers()
    
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

@web_bp.route('/amplitude')
def amplitude_detail():
    """
    Detailed view of Amplitude data.
    """
    parser = parser_manager.get_parser('amplitude')
    if not parser:
        return render_template('error.html', message="Amplitude data not available")
    
    data = {
        'overview': parser.get_platform_overview(),
        'events_summary': parser.get_events_summary(),
        'properties_summary': parser.get_properties_summary(),
        'events_list': parser.get_events_list(),  # Show all events
        'properties_by_event': parser.get_properties_by_event(),  # Show all properties
        'unique_properties_list': parser.get_unique_properties_list()  # Show all unique properties
    }
    
    return render_template('amplitude.html', data=data)

@web_bp.route('/insider')
def insider_detail():
    """
    Detailed view of Insider data.
    """
    parser = parser_manager.get_parser('insider')
    if not parser:
        return render_template('error.html', message="Insider data not available")
    
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

@web_bp.route('/gtm')
def gtm_overview():
    """
    Overview of both GTM containers.
    """
    gtm_data = {}
    parsers = parser_manager.get_all_parsers()
    
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

@web_bp.route('/gtm/<container_type>')
def gtm_detail(container_type):
    """
    Detailed view of specific GTM container.
    """
    parser_key = f'gtm_{container_type}'
    parser = parser_manager.get_parser(parser_key)
    
    if not parser:
        return render_template('error.html', message=f"GTM {container_type} data not available")
    
    data = {
        'overview': parser.get_platform_overview(),
        'container_info': parser.get_container_info(),
        'tags_summary': parser.get_tags_summary(),
        'variables_summary': parser.get_variables_summary(),
        'triggers_summary': parser.get_triggers_summary(),
        'tags_list': parser.get_tags_list(),  # Show all tags
        'destination_analysis': parser.get_destination_analysis(),
        'data_flow': parser.get_data_flow_analysis()
    }
    
    return render_template('gtm_detail.html', data=data, container_type=container_type)

@web_bp.app_errorhandler(404)
def not_found(error):
    """
    404 error handler.
    """
    return render_template('error.html', message="Page not found"), 404

@web_bp.app_errorhandler(500)
def internal_error(error):
    """
    500 error handler.
    """
    return render_template('error.html', message="Internal server error"), 500

