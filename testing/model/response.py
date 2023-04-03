from requests import Response


class ResponseEntity:

    def __init__(self, response: Response):
        self.status_code = response.status_code
        self.json_content = response.json()
        self.headers = response.headers
        self._original_response = response
