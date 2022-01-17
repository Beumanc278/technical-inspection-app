from flask import Flask, render_template, jsonify
from flask_restful import Api

app = Flask(__name__)
api = Api(app)

api.add_resource()