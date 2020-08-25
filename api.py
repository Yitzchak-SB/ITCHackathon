from flask import Flask, request, json
from Validations import Validations
from data.SQLiteDataLayer import SqlDataLayer
from flask_cors import CORS
from decimal import *

getcontext()

data_layer = SqlDataLayer()
app = Flask(__name__)
cors = CORS(app)


@app.route("/", methods=["POST"])
def set_location():
    try:
        data = request.json
        print(data)
        lat = float(data["data"]["lat"])
        long = float(data["data"]["long"])
        Validations.validate_lat(lat)
        Validations.validate_long(long)
        data_layer.add_address(lat, long)
        return app.response_class(response=json.dumps({"message": "Data sent successfully to DataBase"}), status=200, mimetype="application/json")
    except Exception as e:
        print(e)
        return app.response_class(response=json.dumps({"message": "Missing data for the request"}), status=400,
                                  mimetype="application/json")


@app.route("/email", methods=["POST"])
def set_email():
    try:
        data = request.json
        Validations.validate_email(data["email"])
        return app.response_class(response=json.dumps({"message": "Email sent successfully to DataBase"}), status=200,
                                  mimetype="application/json")
    except Exception as e:
        print(e)
        return app.response_class(response=json.dumps({"message": "Missing data for the request"}), status=400,
                                  mimetype="application/json")

@app.route("/")
def get_result():
    try:
        result = None
        return app.response_class(response=json.dumps({"result": result}), status=200,
                                  mimetype="application/json")
    except Exception as e:
        print(e)
        return app.response_class(response=json.dumps({"message": "Missing data for the request"}), status=400,
                                  mimetype="application/json")





if __name__ == "__main__":
    app.run(debug=True)