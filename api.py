from flask import Flask, request
from data.DataLayer import DataLayer
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)


@app.route("/")
def hello_world():
    return "Hello World"
