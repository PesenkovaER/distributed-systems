from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

servers = [
    "https://127.0.0.1:5001",
    "https://127.0.0.1:5002"
]

@app.route("/api/data", methods=["POST"])
def proxy():
    for server in servers:
        try:
            resp = requests.post(
                server + "/api/data",
                json=request.json,
                cert=("client_cert.pem", "client_key.pem"),
                verify=False
            )
            return resp.json()
        except Exception as e:
            print("Server failed:", server)

    return jsonify({"error": "all servers down"}), 500


@app.route("/export", methods=["GET"])
def export():
    for server in servers:
        try:
            resp = requests.get(
                server + "/export",
                params=request.args,
                cert=("client_cert.pem", "client_key.pem"),
                verify=False
            )
            return resp.content
        except:
            continue

    return "error", 500


if __name__ == "__main__":
    app.run(port=8000)