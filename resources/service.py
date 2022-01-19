from flask_restful import Resource, reqparse
from models.service import ServiceModel, ServiceListModel


class Service(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('service-id', type=int)
    parser.add_argument('service-name', type=str)
    parser.add_argument('service-description', type=str)

    def get(self):
        return {"fields-for-request": ServiceModel().json()}

    def post(self):
        data = Service.parser.parse_args()
        print(f"Received data: {data}")
        valid_values = [value is not None for value in data.values()]
        if True not in valid_values:
            return {"message": f"The parameters which have been given are empty - {data}"}, 400
        services = ServiceModel.get_by_parameters(data)
        if services:
            return {"services": services}
        else:
            return {"message": f"No services were found for parameters - {data}"}, 404

    def put(self):
        data = Service.parser.parse_args()
        print(f"Received data: {data}")
        valid_values = [value is not None for value in data.values()]
        if True not in valid_values:
            return {"message": f"The parameters which have been given are empty - {data}"}, 400
        if data['service-id']:
            result, updated_service = ServiceModel(*data.values()).update_in_database(data)
            if result:
                return {"message": "Service was updated successfully", "service-parameters": updated_service.json()}, 201
            else:
                return {"message": f"Service was not updated with given parameters {data}."}, 500
        else:
            result, service_id = ServiceModel(*data.values()).insert_to_database()
            if result:
                return {"message": "Service was inserted successfully.", "service-id": service_id}, 201
            else:
                return {"message": f"Service with given parameters already exists with the service ID - {service_id}",
                        "service-id": service_id}

    def delete(self):
        data = Service.parser.parse_args()
        print(f"Received data: {data}")
        valid_values = [value is not None for value in data.values()]
        if True not in valid_values:
            return {"message": f"The parameters which have been given are empty - {data}"}, 400
        deleted_service = ServiceModel(*data.values()).delete_service()
        if deleted_service:
            return {"message": f"The service with ID {data['service-id']} was deleted successfully.",
                    "service-parameters": deleted_service.json()}, 204
        else:
            return {"message": f'The service with ID {data["service-id"]} does not exist.'}, 400


class ServicesList(Resource):

    def get(self):
        services = ServiceListModel.get_all_services()
        if services:
            return {"services": services}
        else:
            return {"message": "No services were found"}, 404
