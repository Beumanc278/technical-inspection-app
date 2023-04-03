import requests

from testing.model.response import ResponseEntity


class RequestHelper:

    @staticmethod
    def get(target_url, headers=None):
        response = requests.get(target_url, headers)
        return ResponseEntity(response)

    @staticmethod
    def post(target_url, json):
        response = requests.post(target_url, json)
        return ResponseEntity(response)

    @staticmethod
    def put(target_url, json):
        response = requests.put(target_url, json)
        return ResponseEntity(response)

    @staticmethod
    def delete(target_url, json):
        response = requests.delete(target_url, json=json)
        return ResponseEntity(response)
