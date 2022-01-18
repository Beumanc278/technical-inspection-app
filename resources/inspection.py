from flask_restful import Resource, reqparse

from models.inspection import InspectionListModel, InspectionModel


class Inspection(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('inspection-cost', type=float)
    parser.add_argument('mileage', type=int)
    parser.add_argument('lifetime', type=int)
    parser.add_argument('service-id', type=int)
    parser.add_argument('car-parameters', type=str)

    def post(self):
        data = Inspection.parser.parse_args()
        valid_values = [bool(value) for value in data.values()]
        if True not in valid_values:
            return {"message": f"The parameters which have been given are empty - {data}"}, 400
        if 'car-parameters' in data.keys():
            inspections = InspectionModel.get_inspections_by_car_parameters(data['car-parameters'])
        else:
            inspections = InspectionModel.get_inspections_by_parameters(data)
        if inspections:
            return {"inspections": inspections}
        else:
            return {"message": f"No inspections were found for parameters {data}"}, 404

class InspectionsList(Resource):

    def get(self):
        inspections = InspectionListModel.get_all_inspections()
        if inspections:
            return {"inspections": inspections}
        else:
            return {"message": "No inspections were found"}, 404
