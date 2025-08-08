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
    
    # Amplitude configuration
    AMPLITUDE_DIR = SOURCES_DIR / 'amplitude'
    AMPLITUDE_CSV = AMPLITUDE_DIR / 'Kavak - PROD_events_2025-07-17T12_55_21.764+00_00.csv'
    
    # Insider configuration  
    INSIDER_DIR = SOURCES_DIR / 'insider'
    INSIDER_JSON = INSIDER_DIR / 'insider.json'
    
    # GTM configuration
    GTM_DIR = SOURCES_DIR / 'gtm'
    GTM_SERVER_JSON = GTM_DIR / 'GTM-P32K5GT_workspace486.json'  # Server-side
    GTM_CLIENT_JSON = GTM_DIR / 'GTM-NRGXLJ_workspace1002673.json'  # Client-side 