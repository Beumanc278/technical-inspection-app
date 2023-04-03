import logging

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
                    level=logging.INFO)


class TestRunner:

    def __init__(self):
        self.logger: logging.Logger = logging.getLogger()
