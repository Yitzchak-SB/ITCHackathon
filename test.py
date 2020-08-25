from flask import Flask, request, json
from Validations import Validations
from data.SQLiteDataLayer import SqlDataLayer
from flask_cors import CORS
from decimal import *

getcontext()

data_layer = SqlDataLayer()
app = Flask(__name__)
cors = CORS(app)


@app.route("/")
def get_result():
   return 'Hello World'


if __name__ == "__main__":
    app.run(debug=True)