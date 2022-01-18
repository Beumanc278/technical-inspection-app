from flask_restful import Resource, reqparse
from models.service import ServiceModel, ServiceListModel


class Service(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('service-id', type=int)

    def post(self):
        data = Service.parser.parse_args()
        valid_values = [bool(value) for value in data.values()]
        if True not in valid_values:
            return {"message": f"The parameters which have been given are empty - {data}"}, 400
        services = ServiceModel.get_services_by_parameters(data)
        if services:
            return {"services": services}
        else:
            return {"message": f"No services were found for parameters - {data}"}, 404

class ServicesList(Resource):

    def get(self):
        services = ServiceListModel.get_all_services()
        if services:
            return {"services": services}
        else:
            return {"message": "No services were found"}, 404
