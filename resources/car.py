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

    def post(self):
        data = Car.parser.parse_args()
        valid_values = [bool(value) for value in data.values()]
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


class CarList(Resource):

    def get(self):
        cars = CarListModel.get_all_cars()
        if cars:
            return {"cars": cars}
        else:
            return {"message": "No cars were found"}, 404
