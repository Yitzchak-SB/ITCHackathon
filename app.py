from flask import Flask, request, json
from Validations import Validations
from data.MySqlDataLayer import MySqlDataLayer
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
data_layer = MySqlDataLayer()


@app.route("/", methods=["POST"])
def set_location():
    try:
        data = request.json
        latitude = data["latitude"]
        longitude = data["longitude"]
        Validations.validate_lat(float(latitude))
        Validations.validate_long(float(longitude))
        data_layer.add_address(latitude, longitude)
        return app.response_class(response=json.dumps({"message": "Data sent successfully to DataBase"}), status=200, mimetype="application/json")
    except Exception as e:
        print(e)
        return app.response_class(response=json.dumps({"message": "Missing data for the request"}), status=400,
                                  mimetype="application/json")


@app.route("/result", methods=["POST"])
def set_result():
    try:
        data = request.json
        return app.response_class(response=json.dumps({"result": data}),
                                  status=200, mimetype="application/json")
    except Exception as e:
        print(e)
        return app.response_class(response=json.dumps({"message": "Missing data for the request"}), status=400,
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
        result = data_layer.get_result(latitude, longitude)
        return app.response_class(response=json.dumps({"result": result}), status=200,
                                  mimetype="application/json")
    except Exception as e:
        print(e)
        return app.response_class(response=json.dumps({"message": "Missing data for the request"}), status=400,
                                  mimetype="application/json")


if __name__ == "__main__":
    app.run(debug=True)
