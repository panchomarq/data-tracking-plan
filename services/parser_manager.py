from typing import Dict, Optional, Any
from parsers.amplitude_parser import AmplitudeParser
from parsers.insider_parser import InsiderParser
from parsers.gtm_parser import GTMParser
from config import Config

class ParserManager:
    """
    Singleton service to manage data parsers initialization and access.
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ParserManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        self.parsers: Dict[str, Any] = {
            'amplitude': None,
            'insider': None,
            'gtm_server': None,
            'gtm_client': None
        }
        self._initialized = True
        self._load_parsers()
    
    def _load_parsers(self):
        """Initialize all parsers with error handling."""
        self._init_parser('amplitude', AmplitudeParser, Config.AMPLITUDE_CSV)
        self._init_parser('insider', InsiderParser, Config.INSIDER_JSON)
        self._init_parser('gtm_server', GTMParser, Config.GTM_SERVER_JSON)
        self._init_parser('gtm_client', GTMParser, Config.GTM_CLIENT_JSON)
        
    def _init_parser(self, key: str, parser_class: Any, file_path: Any):
        """Helper to initialize a single parser safely."""
        try:
            self.parsers[key] = parser_class(str(file_path))
            print(f"✓ {key.replace('_', ' ').title()} parser initialized successfully")
        except Exception as e:
            print(f"✗ Error initializing {key} parser: {e}")
            self.parsers[key] = None

    def get_parser(self, key: str) -> Optional[Any]:
        """Get a specific parser by key."""
        return self.parsers.get(key)

    def get_all_parsers(self) -> Dict[str, Any]:
        """Get all parsers."""
        return self.parsers

# Global instance
parser_manager = ParserManager()

