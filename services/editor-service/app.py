from flask import Flask
from flask_cors import CORS
from routes.editor import editor_bp
from config.cors import configure_cors

app = Flask(__name__)

# Configure CORS
configure_cors(app)

# Register blueprints
app.register_blueprint(editor_bp)

@app.route('/health')
def health():
    return {'status': 'healthy'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)