from flask import Flask, request
from data.DataLayer import DataLayer
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)


@app.route("/", methods=["POST"])
def get_location():
    data = request.json




if __name__ == "__main__":
    app.run(debug=True)