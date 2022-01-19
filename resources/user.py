from flask_restful import Resource, reqparse

from models.user import UserModel, UserListModel


class User(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('user-id', type=int)
    parser.add_argument('username', type=str)
    parser.add_argument('car-id', type=int)

    def get(self):
        return {"fields-for-request": UserModel().json()}

    def post(self):
        data = User.parser.parse_args()
        print(f"Received data: {data}")
        valid_values = [value is not None for value in data.values()]
        if True not in valid_values:
            return {"message": f"The parameters which have been given are empty - {data}"}, 400

        users = UserModel.get_by_parameters(data)
        if users:
            return {"users": users}
        else:
            return {"message": f"No users were found for parameters {data}"}, 404

class UsersList(Resource):

    def get(self):
        users = UserListModel.get()
        if users:
            return {"users": users}
        else:
            return {"message": "No users were found"}, 404
