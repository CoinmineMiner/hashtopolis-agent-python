import os
import json
from flask import Flask, jsonify, request
import threading

api = Flask(__name__)


@api.route("/stats", methods=["GET", "PUT"])
def get_stats():
    if request.method == "GET":
        try:
            return jsonify(api.config["stats"])
        except Exception as e:
            return (
                json.dumps({"success": False, "reason": e}),
                400,
                {"ContentType": "application/json"},
            )

    elif request.method == "PUT":
        try:
            json_obj = request.get_json()
            if json_obj:
                api.config["stats"] = json_obj
            return (
                json.dumps({"success": True}),
                200,
                {"ContentType": "application/json"},
            )
        except Exception as e:
            return (
                json.dumps({"success": False, "reason": e}),
                400,
                {"ContentType": "application/json"},
            )


api.config["stats"] = {
    "accepted": 0,
    "cracks": 0,
    "progress_in_percent": 0,
    "skips": 0,
    "speed": 0,
    "zaps": 0,
}

host = os.environ.get("HASHTOPOLIS_API_HOST") or "0.0.0.0"
port = int(os.environ.get("HASHTOPOLIS_API_PORT") or "8000")
print("Starting Api Server on {}:{}".format(host, port))

threading.Thread(
    target=lambda: api.run(debug=False, host=host, port=port, use_reloader=False)
).start()
