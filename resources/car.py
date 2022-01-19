from flask_restful import Resource, reqparse
from models.car import CarListModel, CarModel


class Car(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('car-id', type=int)
    parser.add_argument('car-brend', type=str)
    parser.add_argument('car-model', type=str)
    parser.add_argument('car-year', type=int)
    parser.add_argument('car-engine-type', type=str)
    parser.add_argument('car-engine-capacity', type=float)
    parser.add_argument('car-transmission', type=str)
    parser.add_argument('car-drive-unit', type=str)

    def get(self):
        return {"fields-for-request": CarModel().json()}

    def post(self):
        data = Car.parser.parse_args()
        print(f"Received data: {data}")
        valid_values = [value is not None for value in data.values()]
        if True not in valid_values:
            return {"message": f"The parameters which have been given are empty - {data}"}, 400
        if data['car-id']:
            cars = CarModel.get_by_car_id(data['car-id'])
        else:
            cars = CarModel.get_by_parameters(data)
        if cars:
            return {"cars": cars}
        else:
            given_parameters = [f'{key}: {value}' for key, value in data.items() if value is not None]
            return {"message": f"Cars not found for parameters: {given_parameters}"}, 404

    def put(self):
        data = Car.parser.parse_args()
        print(f"Received data: {data}")
        valid_values = [value is not None for value in data.values()]
        if True not in valid_values:
            return {"message": f"The parameters which have been given are empty - {data}"}, 400
        if data['car-id']:
            try:
                CarModel(*data.values()).update_in_database(data)
                return {"message": "Car was updated successfully"}, 201
            except Exception as ex:
                print(ex)
                return {"message": f"An error occured updating the car with parameters {data.values()}"}, 500
        else:
            try:
                result, car_id = CarModel(*data.values()).insert_to_database()
                if result:
                    return {"message": "Car was inserted successfully.", "car-id": car_id}, 201
                else:
                    return {"message": f"Car with given parameters already exists with the car ID - {car_id}",
                            "car-id": car_id}
            except Exception as ex:
                print(ex)
                return {"message": f'An error occured inserting the car with parameters {data.values()}'}

    def delete(self):
        data = Car.parser.parse_args()
        print(f"Received data: {data}")
        valid_values = [value is not None for value in data.values()]
        if True not in valid_values:
            return {"message": f"The parameters which have been given are empty - {data}"}, 400
        try:
            deleted_car = CarModel(*data.values()).delete_car()
        except Exception as ex:
            print(ex)
            return {"message": f"An error occurred deleting the car with ID - {data['car-id']}"}, 500
        if deleted_car:
            return {"message": f"The car with ID {data['car-id']} was deleted successfully.",
                    "car-parameters": deleted_car.json()}, 204
        else:
            return {"message": f'The car with ID {data["car-id"]} does not exist.'}, 400

class CarList(Resource):

    def get(self):
        cars = CarListModel.get_all_cars()
        if cars:
            return {"cars": cars}
        else:
            return {"message": "No cars were found"}, 404
