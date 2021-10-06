from flask import Blueprint
from flask_restful import Api

from resources.UserResource import UserResource
from resources.RecognitionResource import RecognitionResource

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Routes
api.add_resource(RecognitionResource, '/identification')
api.add_resource(UserResource, '/users')
