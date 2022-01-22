from flask_restful import Resource, reqparse

from models.inspection import InspectionListModel, InspectionModel


class Inspection(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('inspection-id', type=int)
    parser.add_argument('inspection-name', type=str)
    parser.add_argument('inspection-cost', type=int)
    parser.add_argument('inspection-mileage', type=int)
    parser.add_argument('inspection-lifetime', type=int)
    parser.add_argument('inspection-service-id', type=int)
    parser.add_argument('inspection-car-id', type=int)

    def get(self):
        return {"fields-for-request": InspectionModel().json()}

    def post(self):
        data = Inspection.parser.parse_args()
        print(f"Received data: {data}")
        valid_values = [value is not None for value in data.values()]
        if True not in valid_values:
            return {"message": f"The parameters which have been given are empty - {data}"}, 400
        if 'inspection-car-id' in data.keys() and data['inspection-car-id']:
            inspections = InspectionModel.get_inspections_by_car_id(data['inspection-car-id'])
        else:
            inspections = InspectionModel.get_inspections_by_parameters(data)
        if inspections:
            return {"inspections": inspections}
        else:
            return {"message": f"No inspections were found for parameters {data}"}, 404

    def put(self):
        data = Inspection.parser.parse_args()
        print(f"Received data: {data}")
        valid_values = [value is not None for value in data.values()]
        if True not in valid_values:
            return {"message": f"The parameters which have been given are empty - {data}"}, 400
        if data['inspection-id']:
            result, updated_inspection = InspectionModel(*data.values()).update_in_database(data)
            if result:
                return {"message": "Inspection was updated successfully", "inspection-parameters": updated_inspection.json()}, 201
            else:
                return {"message": f"Inspection was not updated with given parameters {data}."}, 500
        else:
            result, inspection_id = InspectionModel(*data.values()).insert_to_database()
            if result:
                return {"message": "Inspection was inserted successfully.", "inspection-id": inspection_id}, 201
            else:
                return {"message": f"Inspection with given parameters already exists with the inspection ID - {inspection_id}",
                        "inspection-id": inspection_id}

    def delete(self):
        data = Inspection.parser.parse_args()
        print(f"Received data: {data}")
        valid_values = [value is not None for value in data.values()]
        if True not in valid_values:
            return {"message": f"The parameters which have been given are empty - {data}"}, 400
        deleted_inspection = InspectionModel(*data.values()).delete_inspection()
        if deleted_inspection:
            return {"message": f"The inspection with ID {data['inspection-id']} was deleted successfully.",
                    "inspection-parameters": deleted_inspection.json()}, 204
        else:
            return {"message": f'The inspection with ID {data["inspection-id"]} does not exist.'}, 400

class InspectionsList(Resource):

    def get(self):
        inspections = InspectionListModel.get_all_inspections()
        if inspections:
            return {"inspections": inspections}
        else:
            return {"message": "No inspections were found"}, 404
