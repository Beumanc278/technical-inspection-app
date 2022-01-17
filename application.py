from flask import Flask, render_template, jsonify
from flask_restful import Api

app = Flask(__name__)
api = Api(app)

@app.route('/')
def home():
    return render_template('Main.html')

app.run(port=5000, debug=True)