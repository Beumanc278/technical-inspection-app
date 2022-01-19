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

    def put(self):
        data = User.parser.parse_args()
        print(f"Received data: {data}")
        valid_values = [value is not None for value in data.values()]
        if True not in valid_values:
            return {"message": f"The parameters which have been given are empty - {data}"}, 400
        if data['user-id']:
            result, updated_user = UserModel(*data.values()).update_in_database(data)
            if result:
                return {"message": f"User was updated successfully.", "user-parameters": updated_user.json()}, 201
            else:
                return {"message": f"User was not updated with given parameters {data}."}, 500
        else:
            result, user_id = UserModel(*data.values()).insert_to_database()
            if result:
                return {"message": f"User was inserted successfully.",
                        "user-id": user_id}, 201
            else:
                return {"message": f"User with given parameters already exists with the user ID - {user_id}",
                        "user-id": user_id}

    def delete(self):
        data = User.parser.parse_args()
        print(f"Received data: {data}")
        valid_values = [value is not None for value in data.values()]
        if True not in valid_values:
            return {"message": f"The parameters which have been given are empty - {data}"}, 400
        deleted_user = UserModel(*data.values()).delete_user()
        if deleted_user:
            return {"message": f"The user with ID {data['user-id']} was deleted successfully.",
                    "user-parameters": deleted_user.json()}, 204
        else:
            return {"message": f'The user with ID {data["user-id"]} does not exist.'}, 400

class UsersList(Resource):

    def get(self):
        users = UserListModel.get()
        if users:
            return {"users": users}
        else:
            return {"message": "No users were found"}, 404
