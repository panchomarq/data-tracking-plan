from flask import Blueprint, jsonify
from services.parser_manager import parser_manager

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/amplitude/events')
def api_amplitude_events():
    """
    API endpoint to get Amplitude events data.
    """
    parser = parser_manager.get_parser('amplitude')
    if not parser:
        return jsonify({'error': 'Amplitude data not available'}), 404
    
    return jsonify(parser.get_events_list())

@api_bp.route('/insider/events')
def api_insider_events():
    """
    API endpoint to get Insider events data.
    """
    parser = parser_manager.get_parser('insider')
    if not parser:
        return jsonify({'error': 'Insider data not available'}), 404
    
    return jsonify(parser.get_events_list())

@api_bp.route('/gtm/<container_type>/tags')
def api_gtm_tags(container_type):
    """
    API endpoint to get GTM tags data.
    """
    parser_key = f'gtm_{container_type}'
    parser = parser_manager.get_parser(parser_key)
    
    if not parser:
        return jsonify({'error': f'GTM {container_type} data not available'}), 404
    
    return jsonify(parser.get_tags_list())

