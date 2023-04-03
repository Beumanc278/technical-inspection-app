from testing.fixture.application import Application
from testing.fixture.car import CarHelper
from testing.fixture.request import RequestHelper


def test_get_cars(runner, app: Application, request_helper: RequestHelper):
    car = CarHelper(app)
    response = request_helper.get(car.test_endpoint)
    expected_status_code = 200
    actual_status_code = response.status_code
    assert actual_status_code == expected_status_code, f'The actual status code "{actual_status_code}" does not correspond to the expected "{expected_status_code}"'


def test_get_inspections(runner, app: Application, request_helper: RequestHelper):
    pass


def test_get_services(runner, app: Application, request_helper: RequestHelper):
    pass


def test_get_users(runner, app: Application, request_helper: RequestHelper):
    pass
