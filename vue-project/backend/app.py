from flask import Flask, request, jsonify
from flask_cors import CORS
from database import get_db_connection

app = Flask(__name__)
CORS(app)  # Enable CORS for Vue frontend

# API Route to Get UV Index by Location or Postcode
@app.route('/get-uv-data', methods=['GET'])
def get_uv_data():
    location = request.args.get('location')

    if not location:
        return jsonify({"error": "Location is required"}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Query to fetch UV data
        cur.execute(
            """
            SELECT uv_index FROM uv_data_test 
            WHERE location = %s OR postcode = %s 
            ORDER BY timestamp DESC LIMIT 1
            """, 
            (location, location)  # Search by suburb name or postcode
        )

        result = cur.fetchone()

        cur.close()
        conn.close()

        if result:
            return jsonify({"location": location, "uv_index": result[0]})
        else:
            return jsonify({"error": "No UV data found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)  # Run Flask on port 5000
