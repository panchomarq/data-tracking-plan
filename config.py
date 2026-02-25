import os
from pathlib import Path

class Config:
    """
    Configuration settings for the Data Tracking Plan Flask application.
    """
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = True
    
    # Data sources paths
    BASE_DIR = Path(__file__).parent
    SOURCES_DIR = BASE_DIR / 'sources'
    
    # Amplitude configuration — API (live) vs CSV (fallback)
    AMPLITUDE_API_KEY = os.environ.get('AMPLITUDE_API_KEY', '')
    AMPLITUDE_SECRET_KEY = os.environ.get('AMPLITUDE_SECRET_KEY', '')
    AMPLITUDE_REGION = os.environ.get('AMPLITUDE_REGION', 'us')
    AMPLITUDE_SOURCE_MODE = os.environ.get('AMPLITUDE_SOURCE_MODE', 'api')
    AMPLITUDE_CACHE_TTL = int(os.environ.get('AMPLITUDE_CACHE_TTL', '900'))

    _AMP_URLS = {
        'us': 'https://amplitude.com/api/2',
        'eu': 'https://analytics.eu.amplitude.com/api/2',
    }
    AMPLITUDE_BASE_URL = _AMP_URLS.get(AMPLITUDE_REGION, _AMP_URLS['us'])

    # Amplitude CSV fallback paths
    AMPLITUDE_DIR = SOURCES_DIR / 'amplitude'
    AMPLITUDE_CSV = AMPLITUDE_DIR / 'amplitude_events.csv'
    
    # Insider configuration  
    INSIDER_DIR = SOURCES_DIR / 'insider'
    INSIDER_JSON = INSIDER_DIR / 'insider.json'
    
    # GTM configuration
    GTM_DIR = SOURCES_DIR / 'gtm'
    GTM_SERVER_JSON = GTM_DIR / 'GTM-P32K5GT_workspace486.json'  # Server-side
    GTM_CLIENT_JSON = GTM_DIR / 'GTM-NRGXLJ_workspace1002783.json'  # Client-side
