from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# -----------------------------
#  DATABASE CONNECTION
# -----------------------------
def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="farah1965!",
        database="Hospital"  # <-- FIXED (removed space)
    )

# -----------------------------
#  GET ALL PATIENTS
# -----------------------------
@app.route("/patients/<int:patient_id>", methods=["GET"])
def get_patient_by_id(patient_id):
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)

        query = "SELECT * FROM patients WHERE patient_id = %s"
        cursor.execute(query, (patient_id,))
        patient = cursor.fetchone()

        cursor.close()
        db.close()

        if not patient:
            return jsonify({"error": "Patient not found"}), 404

        return jsonify({"success": True, "data": patient})

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"error": "Error fetching patient"}), 500


# -----------------------------
#  CREATE PATIENT   (THIS IS WHAT REACT CALLS)
# -----------------------------
@app.route("/patients", methods=["POST"])
def create_patient():
    data = request.json

    full_name = data.get("full_name")
    gender = data.get("gender")
    age = data.get("age")
    phone = data.get("phone")
    address = data.get("address")
    diseases = data.get("diseases")
    latitude = data.get("latitude")
    longitude = data.get("longitude")

    try:
        db = get_db()
        cursor = db.cursor()

        query = """
            INSERT INTO patients 
            (full_name, gender, age, phone, address, diseases, latitude, longitude)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(query, (
            full_name, gender, age,
            phone, address, diseases,
            latitude, longitude
        ))
        db.commit()

        new_id = cursor.lastrowid

        cursor.close()
        db.close()

        patient_id = new_id

        return jsonify({
            "success": True,
            "data": {"patientId": new_id}
        })

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    app.run(port=5000, debug=True)
