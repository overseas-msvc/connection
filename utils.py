import uuid, os


def delete_files(db, conn):
    data = db.get_object_by_id(conn.connector_type, conn.connector_id, inJson=True)
    for key, value in data.items():
         if key.endswith("_file_uuid") and data[key]:
              filepath = os.path.join("file_storage", conn.connector_type, value)
              if os.path.exists(filepath):
                os.remove(filepath)

def save_files(db, data, connector_type, id=None):
    if id:
         old_data = db.get_object_by_id(connector_type, id, inJson=True)
    files = {}
    for key, value in data[connector_type].items():
            if key.endswith("_file"):
                if not value:
                    files[key] = ''
                else:
                    if id and old_data[f"{key}_uuid"]:
                        os.remove(os.path.join("file_storage", connector_type, old_data[f"{key}_uuid"]))
                    filepath, uid = get_uid(connector_type)
                    with open(filepath,'w') as f:
                        f.write(value.split(',')[1])
                    files[key] = uid
    for key, uid in files.items():
            if uid:
                data[connector_type][f"{key}_uuid"] = uid
            del data[connector_type][key]
    return data

def get_uid(connector_type):
    uid = str(uuid.uuid4())
    filepath = os.path.join("file_storage", connector_type, uid)
    while os.path.exists(filepath):
        uid = str(uuid.uuid4())
        filepath = os.path.join("file_storage", connector_type, uid)
    return filepath, uid

def get_file_from_storage(connector_type, conn, filename):
    filepath = os.path.join("file_storage", connector_type, getattr(conn, f"{filename}_file_uuid"))
    with open(filepath, "r") as f:
        file_content = f.read()
    return {
         "file_name": filename,
         "file_content": file_content
    }