from testing.fixture.application import Application


class CarHelper:

    endpoint = '/cars'

    def __init__(self, app: Application):
        self.test_endpoint = f'{app.url}{self.endpoint}'

