import requests
from flask import Flask, request, json
from Validations import Validations
from data.MySqlDataLayer import MySqlDataLayer
from flask_cors import CORS

from hackaton_ds import find_roof_json

data_layer = MySqlDataLayer()
app = Flask(__name__)
cors = CORS(app)


@app.route("/", methods=["POST"])
def set_location():
    result = None
    try:
        data = request.json
        response = requests.get("https://us1.locationiq.com/v1/search.php?key=4dd6358a6c3c9e&q={}&format=json".format(data["address"])).json()
        latitude = float(response[0]["lat"])
        longitude = float(response[0]["lon"])
        Validations.validate_lat(latitude)
        Validations.validate_long(longitude)
        #square = data_layer.get_data_from_input(latitude, longitude)
        square = find_roof_json(latitude, longitude)
        result = {"latitude": latitude, "longitude": longitude, "square": float(square)}
        return app.response_class(response=json.dumps(result), status=200, mimetype="application/json")
    except Exception as e:
        print(e)
        return app.response_class(response=json.dumps("This is not a rooftop"), status=400,
                                  mimetype="application/json")


@app.route("/email", methods=["POST"])
def set_email():
    try:
        data = request.json
        email = data["email"]
        latitude = data["latitude"]
        longitude = data["longitude"]
        Validations.validate_email(email)
        data_layer.add_email(email, latitude, longitude)
        return app.response_class(response=json.dumps({"message": "Email sent successfully to DataBase"}), status=200,
                                  mimetype="application/json")
    except Exception as e:
        print(e)
        return app.response_class(response=json.dumps({"message": "Missing data for the request"}), status=400,
                                  mimetype="application/json")


@app.route("/")
def get_result():
    content = request.json
    latitude = content["latitude"]
    longitude = content["longitude"]
    try:
        result = data_layer.get_square(latitude, longitude)
        return app.response_class(response=json.dumps({"result": result}), status=200,
                                  mimetype="application/json")
    except Exception as e:
        print(e)
        return app.response_class(response=json.dumps({"message": "Missing data for the request"}), status=400,
                                  mimetype="application/json")


@app.route("/test")
def test():
    try:
        return app.response_class(response=json.dumps({"result": "app is running"}), status=200,
                                  mimetype="application/json")
    except Exception as e:
        print(e)
        return app.response_class(response=json.dumps({"message": "Missing data for the request"}), status=400,
                                  mimetype="application/json")


@app.route('/file')
def json_to_database():
    results = data_layer.json_to_db()
    response = app.response_class(
        response={json.dumps(results)},
        status=200,
        mimetype='application/json'
    )
    return response



if __name__ == "__main__":
    app.run(debug=True)
