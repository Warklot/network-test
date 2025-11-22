from flask import Flask, request, jsonify
from ping import ping  

app = Flask(__name__)

@app.route("/ping", methods=["GET"])
def ping_api():
    hosts = request.args.get("hosts", "8.8.8.8").split(",") 
    results = []
    for host in hosts:
        results.append(ping(host.strip(), 4))
    return jsonify(results)

@app.route("/pingpost", methods=["POST"])
def ping_api_post():
    data = request.get_json()
    hosts = data.get("hosts", [])
    count = data.get("count", 4)
    
    results = []
    for host in hosts:
        results.append(ping(host.strip(), count))
        
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)