import json

from flask import Flask, request
from db_manage.mysql_connector.database import Database

app = Flask(__name__)

@app.route("/connections", methods=["GET"])
def get_connections():
	data = request.json
	db = Database("connection")
	objects = db.get_list_of_objects(data["connectionType"], inJson=True)
	return json.dumps(objects)

@app.route("/connection", methods=["GET"])
def get_connection():
	data = request.json
	db = Database("connection")
	conn = db.get_object_by_id(data["connectionType"], data["id"], inJson=True)
	return json.dumps(conn)

@app.route("/connection", methods=["POST"])
def create_connection():
	data = request.json
	connection_type = data["connectionType"]
	del data["connectionType"]
	db = Database("connection")
	conn = db.add_object(connection_type, data)
	return json.dumps(conn)

if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True)