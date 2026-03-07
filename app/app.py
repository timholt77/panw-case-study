from flask import Flask
from .routes import routes_bp

app = Flask(__name__)
app.secret_key = 'dev-secret-key'
app.register_blueprint(routes_bp)
