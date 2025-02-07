from flask import Flask
from config import Config
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Flask
app = Flask(__name__)
app.config.from_object(Config)

# Initialize Firebase
cred = credentials.Certificate(app.config["FIREBASE_CREDENTIALS"])
firebase_admin.initialize_app(cred)
db = firestore.client()


# Import and register blueprints
from server.src.routes import routes_blueprint
from server.src.auth import auth_blueprint

app.register_blueprint(routes_blueprint)
app.register_blueprint(auth_blueprint)
