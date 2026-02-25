from dotenv import load_dotenv

load_dotenv()

from flask import Flask
from config import Config
from routes.web import web_bp
from routes.api import api_bp
from services.parser_manager import parser_manager

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Register Blueprints
    app.register_blueprint(web_bp)
    app.register_blueprint(api_bp)

    return app

app = create_app()

if __name__ == '__main__':
    print("🚀 Starting Data Tracking Plan Dashboard...")
    print("📊 Available platforms:")
    
    parsers = parser_manager.get_all_parsers()
    for platform, parser in parsers.items():
        status = "✓ Ready" if parser else "✗ Error"
        print(f"   - {platform}: {status}")
    
    print("\n🌐 Dashboard will be available at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
