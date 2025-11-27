from flask import Flask, request, jsonify
from ping import HostPinger
import logging
from flask import request

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
ALLOWED_KEYS = {"hosts", "count"}
@app.before_request
def log_request_info():
    logging.info(f"{request.method} {request.path} from {request.remote_addr}")
    logging.info(f"Body: {request.get_json()}")

@app.route("/pingpost", methods=["POST"])
def ping_api_post():
    data = request.get_json()
    extra_keys = set(data.keys()) - ALLOWED_KEYS
    if extra_keys:
        return jsonify({"error": f"Invalid keys in request body: {', '.join(extra_keys)}"}), 400
    hosts = data.get("hosts", [])
    count = data.get("count")
    
    if not hosts or count is None:
        return jsonify({"error": "Misssing 'host' or 'count' in request body"}), 400

    try:
        count = int(count)
        if count <= 0:
            raise ValueError
    except ValueError:
        return jsonify({"error": "'count' must be a positive integer"}), 400

    results = []
    for host in hosts:
        pinger = HostPinger(host.strip(), count)
        pinger.ping()
        results.append(pinger.get_info())
        
    return jsonify(results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)

