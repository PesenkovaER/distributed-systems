from flask import Flask, request, jsonify
from cryptography.fernet import Fernet
import ssl
import sys
import csv
import xml.etree.ElementTree as ET
import io

app = Flask(__name__)

# загрузка ключа
with open("encryption_key.txt", "rb") as f:
    key = f.read()

fernet = Fernet(key)

# временное хранилище для сообщений текущей сессии
user_messages = []

@app.route("/api/data", methods=["POST"])
def handle():
    encrypted = request.json["data"]

    try:
        decrypted = fernet.decrypt(encrypted.encode()).decode()
        print("Decrypted:", decrypted)
        
        # сохраняем сообщение в память
        user_messages.append({
            "id": len(user_messages) + 1,
            "message": decrypted
        })
        
        return jsonify({"status": "ok", "message": decrypted})
    except Exception as e:
        return jsonify({"error": "decryption failed"}), 400

@app.route("/export", methods=["GET"])
def export():
    fmt = request.args.get("format", "json")

    if fmt == "json":
        return jsonify(user_messages)

    elif fmt == "csv":
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=["id", "message"])
        writer.writeheader()
        writer.writerows(user_messages)
        return output.getvalue(), 200, {'Content-Type': 'text/plain'}

    elif fmt == "xml":
        root = ET.Element("messages")
        for item in user_messages:
            msg_elem = ET.SubElement(root, "message")
            for k, v in item.items():
                sub = ET.SubElement(msg_elem, k)
                sub.text = str(v)
        return ET.tostring(root, encoding='unicode'), 200, {'Content-Type': 'text/plain'}

    return jsonify({"error": "unknown format"}), 400

if __name__ == "__main__":
    port = int(sys.argv[1])

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain("server_cert.pem", "server_key.pem")
    context.load_verify_locations("ca_cert.pem")
    context.verify_mode = ssl.CERT_REQUIRED

    app.run(host="0.0.0.0", port=port, ssl_context=context)