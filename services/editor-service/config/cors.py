from flask_cors import CORS

def configure_cors(app):
    CORS(app, 
         resources={r"/api/*": {
             "origins": ["https://norsewind.studio", "https://admin.norsewind.studio"],
             "supports_credentials": True,
             "allow_headers": ["Content-Type", "Authorization"],
             "expose_headers": ["Content-Length", "X-Rate-Limit"],
             "max_age": 600,
             "vary_header": True,
             "send_wildcard": False,
             "allow_private_network": False
         }})