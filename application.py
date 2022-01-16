import os
from flask import Flask, jsonify, request, render_template

from modules.database import DatabaseHelper


class Application:
    app = Flask(__name__)

    def __init__(self):
        self.project_dir = os.getcwd()
        self.users_db = DatabaseHelper(os.path.join(self.project_dir, 'databases', 'users.db'))
        self.services_db = DatabaseHelper(os.path.join(self.project_dir, 'databases', 'services.db'))
        self.offers_db = DatabaseHelper(os.path.join(self.project_dir, 'databases', 'offers.db'))

    @app.route('/')
    def home(self):
        return render_template('index.html')


if __name__ == "__main__":
    app = Application().app
    app.run(port=5000)