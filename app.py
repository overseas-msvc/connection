import json

from flask import Flask, request
from db_manage.mysql_connector.database import Database
from flask_cors import CORS

from utils import save_files, delete_files

app = Flask(__name__)

CORS(app, supports_credentials=True)

@app.route("/connections", methods=["GET"])
def get_connections():
	filter = request.args.get("filter", "")
	db = Database("Connection")
	objects = db.get_filtered_list_of_objects("Connection", filter, include_columns=["name", "connector_type"], inJson=True)
	return json.dumps(objects)

@app.route("/connection", methods=["GET"])
def get_connection():
	id = request.args.get("id")
	db = Database("Connection")
	conn = db.get_object_by_id("Connection", id)
	conn = db.get_object_by_id(conn.connector_type, conn.connector_id, inJson=True)
	return json.dumps(conn)

@app.route("/connection", methods=["POST"])
def create_connection():
	data = request.json
	connector_type = data["connector_type"]
	db = Database("Connection")
	if db.get_list_of_objects("Connection", {"name": data["name"]}):
		return f"connection with name '{data['name']}' already exists"
	data = save_files(db, data, connector_type)
	connector_id = db.add_object(connector_type, data[connector_type])
	data["connector_id"] = connector_id
	del data[connector_type]
	if connector_id:
		conn = db.add_object("Connection", data)
		return json.dumps(conn), 200
	return "failed to create connection", 500

@app.route("/connection", methods=["PUT"])
def update_connection():
	data = request.json
	db = Database("Connection")
	conn = db.get_object_by_id("Connection", data["id"])
	data = save_files(db, data, conn.connector_type, db.get_object_by_id("Connection", data["id"]).connector_id)
	conn = db.update_object(conn.connector_type, conn.connector_id, data[conn.connector_type])
	return json.dumps(conn), 200

@app.route("/connection", methods=["DELETE"])
def delete_connection():
	id = request.args.get("id")
	db = Database("Connection")
	conn = db.get_object_by_id("Connection", id)
	if not conn:
		return f"couldnt find a connection with id: {id}", 400
	delete_files(db, conn)
	db.delete_object(conn.connector_type, conn.connector_id)
	db.delete_object("Connection", id)
	return "", 200


if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True)