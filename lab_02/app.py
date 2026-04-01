from flask import Flask, jsonify, request

app = Flask(__name__)

cars = [
    {"id": 1, "make": "Toyota", "model": "Camry", "year": 2020},
    {"id": 2, "make": "BMW", "model": "X5", "year": 2019}
]

next_id = 3


@app.route('/api/cars', methods=['GET'])
def get_cars():
    return jsonify({"cars": cars})


@app.route('/api/cars/<int:car_id>', methods=['GET'])
def get_car(car_id):

    car = next((c for c in cars if c["id"] == car_id), None)

    if car:
        return jsonify(car)

    return jsonify({"error": "Car not found"}), 404


@app.route('/api/cars', methods=['POST'])
def add_car():

    global next_id

    if not request.json:
        return jsonify({"error": "Invalid data"}), 400

    new_car = {
        "id": next_id,
        "make": request.json["make"],
        "model": request.json["model"],
        "year": request.json["year"]
    }

    cars.append(new_car)
    next_id += 1

    return jsonify(new_car), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)