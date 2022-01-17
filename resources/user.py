from flask_restful import Resource, reqparse

from models.user import UserModel


class User(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True)
    parser.add_argument('car_parameters', type=dict, required=True)

    def get(self, username: str):
        result = UserModel.get(username)


    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass
