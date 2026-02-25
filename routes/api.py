from flask import Blueprint, jsonify
from services.parser_manager import parser_manager
import sys
import os

# Add tools to path for audit imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'tools'))

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

@api_bp.route('/audit/run', methods=['POST'])
def run_audit():
    """
    API endpoint to run the UI/UX audit and return results.
    """
    try:
        from ui_auditor import UIAuditor
        
        auditor = UIAuditor()
        auditor.scan_files()
        
        return jsonify({
            'success': True,
            'report': auditor.report,
            'summary': {
                'design_tokens': len(auditor.report.get('design_tokens', [])),
                'inline_styles': len(auditor.report.get('inline_styles', [])),
                'accessibility': len(auditor.report.get('accessibility', [])),
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@api_bp.route('/audit/report')
def get_audit_report():
    """
    API endpoint to get the last audit report (from file).
    """
    import json
    from pathlib import Path
    
    report_path = Path(__file__).parent.parent / 'audit_report.json'
    
    if not report_path.exists():
        return jsonify({'error': 'No audit report found. Run an audit first.'}), 404
    
    with open(report_path, 'r') as f:
        report = json.load(f)
    
    return jsonify({
        'success': True,
        'report': report,
        'summary': {
            'design_tokens': len(report.get('design_tokens', [])),
            'inline_styles': len(report.get('inline_styles', [])),
            'accessibility': len(report.get('accessibility', [])),
        }
    })

@api_bp.route('/audit/fix/token', methods=['POST'])
def fix_design_token():
    """
    API endpoint to fix a single design token issue.
    Expects JSON: { file, line, token, replacement }
    """
    from flask import request
    from pathlib import Path
    import re
    
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'error': 'No data provided'}), 400
    
    file_path = Path(__file__).parent.parent / data.get('file', '')
    line_no = data.get('line', 0)
    token = data.get('token', '')
    replacement = data.get('replacement', '')
    
    if not all([file_path.exists(), line_no, token, replacement]):
        return jsonify({'success': False, 'error': 'Missing or invalid parameters'}), 400
    
    try:
        lines = file_path.read_text(encoding='utf-8').splitlines()
        if 0 <= line_no - 1 < len(lines):
            original_line = lines[line_no - 1]
            # Case-insensitive replacement for hex colors
            new_line = re.sub(re.escape(token), replacement, original_line, flags=re.IGNORECASE)
            lines[line_no - 1] = new_line
            file_path.write_text('\n'.join(lines), encoding='utf-8')
            return jsonify({
                'success': True, 
                'message': f'Fixed {token} -> {replacement}',
                'original': original_line,
                'fixed': new_line
            })
        else:
            return jsonify({'success': False, 'error': 'Line number out of range'}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@api_bp.route('/audit/fix/inline-style', methods=['POST'])
def fix_inline_style():
    """
    API endpoint to fix a single inline style issue.
    Extracts the style, creates a CSS class, and replaces inline style with class.
    Expects JSON: { file, line, class_name }
    """
    from flask import request
    from pathlib import Path
    import re
    
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'error': 'No data provided'}), 400
    
    file_path = Path(__file__).parent.parent / data.get('file', '')
    line_no = data.get('line', 0)
    class_name = data.get('class_name', '')
    
    if not all([file_path.exists(), line_no, class_name]):
        return jsonify({'success': False, 'error': 'Missing or invalid parameters'}), 400
    
    try:
        lines = file_path.read_text(encoding='utf-8').splitlines()
        if 0 <= line_no - 1 < len(lines):
            original_line = lines[line_no - 1]
            
            # Extract inline style
            style_match = re.search(r'style="([^"]*)"', original_line)
            if not style_match:
                return jsonify({'success': False, 'error': 'No inline style found on this line'}), 400
            
            style_content = style_match.group(1)
            
            # Remove the style attribute and add class
            new_line = re.sub(r'\s*style="[^"]*"', '', original_line)
            # Add class to existing class attribute or create new one
            if 'class="' in new_line:
                new_line = re.sub(r'class="([^"]*)"', f'class="\\1 {class_name}"', new_line)
            else:
                # Add class attribute after the tag name
                new_line = re.sub(r'(<\w+)', f'\\1 class="{class_name}"', new_line, count=1)
            
            lines[line_no - 1] = new_line
            file_path.write_text('\n'.join(lines), encoding='utf-8')
            
            # Append CSS to dashboard.css
            css_path = Path(__file__).parent.parent / 'static' / 'css' / 'dashboard.css'
            css_rule = f"\n/* Auto-generated from inline style */\n.{class_name} {{ {style_content} }}\n"
            
            with open(css_path, 'a', encoding='utf-8') as f:
                f.write(css_rule)
            
            return jsonify({
                'success': True,
                'message': f'Moved inline style to .{class_name}',
                'original': original_line,
                'fixed': new_line,
                'css_added': css_rule.strip()
            })
        else:
            return jsonify({'success': False, 'error': 'Line number out of range'}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@api_bp.route('/audit/fix/all-tokens', methods=['POST'])
def fix_all_design_tokens():
    """
    API endpoint to fix ALL design token issues at once.
    """
    from pathlib import Path
    import re
    
    # Load CSS_VARS from constants
    try:
        from constants import CSS_VARS, PROJECT_ROOT
    except ImportError:
        return jsonify({'success': False, 'error': 'Could not load constants'}), 500
    
    report_path = Path(__file__).parent.parent / 'audit_report.json'
    if not report_path.exists():
        return jsonify({'success': False, 'error': 'No audit report found'}), 404
    
    import json
    with open(report_path, 'r') as f:
        report = json.load(f)
    
    fixed_count = 0
    errors = []
    
    for issue in report.get('design_tokens', []):
        file_path = PROJECT_ROOT / issue['file']
        line_no = issue['line']
        token = issue.get('token', '')
        
        if not token:
            continue
        
        hex_upper = token.upper()
        if hex_upper not in CSS_VARS:
            continue
        
        replacement = f"var({CSS_VARS[hex_upper]})"
        
        try:
            lines = file_path.read_text(encoding='utf-8').splitlines()
            if 0 <= line_no - 1 < len(lines):
                lines[line_no - 1] = re.sub(
                    re.escape(token), replacement, lines[line_no - 1], flags=re.IGNORECASE
                )
                file_path.write_text('\n'.join(lines), encoding='utf-8')
                fixed_count += 1
        except Exception as e:
            errors.append(f"{issue['file']}:{line_no} - {str(e)}")
    
    return jsonify({
        'success': True,
        'fixed_count': fixed_count,
        'errors': errors
    })

