from flask import Blueprint
api = Blueprint('api', __name__)
# Ihre API-Route-Definitionen...

# Dann in __init__.py, nach Initialisierung von `app`, `db`, etc.
from .api import api as api_blueprint
app.register_blueprint(api_blueprint, url_prefix='/api')