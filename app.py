from flask import Flask, request

app = Flask(__name__)

@app.route("/connection", methods=["GET"])
def get_connection():
	data = request.json
	return f"reply from endpoint get_connection, data = {data}"

@app.route("/connection", methods=["POST"])
def create_connection():
	data = request.json
	return f"reply from endpoint create_connection, data = {data}"

if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True)