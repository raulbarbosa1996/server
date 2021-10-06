from flask import request
from flask_restful import Resource
from Model_MySQL import db, User, UserSchema

users_schema = UserSchema(many=True)
user_schema = UserSchema()


# Example
class UserResource(Resource):
    def get(self):
        users = User.query.all()
        data = users_schema.dump(users)
        return {'status': 'success', 'data': data}, 200
