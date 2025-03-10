import json

from flask import Flask, request
from db_manage.mysql_connector.database import Database

app = Flask(__name__)

@app.route("/connections", methods=["GET"])
def get_connections():
	data = request.json
	db = Database("Connection")
	condition = data["filter"] if "filter" in data else {}
	objects = db.get_list_of_objects("Connection", condition, inJson=True)
	return json.dumps(objects)

@app.route("/connection", methods=["GET"])
def get_connection():
	data = request.json
	db = Database("Connection")
	conn = db.get_object_by_id("Connection", data["id"])
	conn = db.get_object_by_id(conn.connector_type, conn.connector_id, inJson=True)
	return json.dumps(conn)

@app.route("/connection", methods=["POST"])
def create_connection():
	data = request.json

	connector_type = data["connector_type"]
	
	db = Database("Connection")
	connector_id = db.add_object(connector_type, data[connector_type])
	del data[connector_type]
	data["connector_id"] = connector_id
	if connector_id:
		conn = db.add_object("Connection", data)
	return json.dumps(conn), 200

@app.route("/connection", methods=["PUT"])
def update_connection():
	data = request.json
	db = Database("Connection")
	conn = db.get_object_by_id("Connection", data["id"])
	conn = db.update_object(conn.connector_type, conn.connector_id, data[conn.connector_type])
	return json.dumps(conn), 200

@app.route("/connection", methods=["DELETE"])
def delete_connection():
	data = request.json
	db = Database("Connection")
	conn = db.get_object_by_id("Connection", data["id"])
	if not conn:
		return f"couldnt find a connection with id: {data["id"]}", 400
	db.delete_object(conn.connector_type, conn.connector_id)
	db.delete_object("Connection", data["id"])
	return "", 200


if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True)