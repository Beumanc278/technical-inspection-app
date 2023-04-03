import subprocess
import pytest

from testing.fixture.application import Application
from testing.fixture.request import RequestHelper
from testing.fixture.runner import TestRunner

PROJECT_PATH = r"C:\\Users\\beumanc\\PycharmProjects\\technical-inspection-app\\"

def setUp(logger):
    # create a new database with mock data for testing
    logger.info("Create a new database for testing")
    subprocess.run(f'python {PROJECT_PATH}\database\database.py')


@pytest.fixture(scope='session')
def runner():
    runner = TestRunner()
    setUp(runner.logger)
    yield TestRunner()
    tearDown(runner.logger)

@pytest.fixture(scope='session')
def app():
    #
    yield Application()

@pytest.fixture(scope='session')
def request_helper():
    yield RequestHelper()


def tearDown(logger):
    logger.info("Restore the initial state of database")
    subprocess.run(f'python {PROJECT_PATH}\database\database.py')
