import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from database import get_db_connection
app = Flask(__name__)
# Enable cross original resource sharing 
CORS(app)
# My OpenWeatherMap API key
API_KEY = "e2f745f4f5345d28044a4f1e6b883c48"
# Use 2.5 version as it is free
API_URL = "https://api.openweathermap.org/data/2.5/uvi" 
@app.route('/get-uv-index', methods=['GET'])
def get_uv_index():
    location = request.args.get('location')
    if not location:
        return jsonify({"error": "Location is required"}), 400
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        # Check if location is a number (postcode) or a string (locality),
        # Using parameterized queries and passing location as a parameter in the cur.execute() method.
        # This ensures that location is treated as a value, not executable code, thus protecting your query from SQL injection attacks.
        if location.isdigit():
            # Query by postcode
            cur.execute(
                """
                SELECT lat, long FROM australian_postcode 
                WHERE postcode = %s
                LIMIT 3
                """,
                (location,)
            )
        else:
            # Query by locality (string)
            cur.execute(
                """
                SELECT lat, long FROM australian_postcode 
                WHERE locality ILIKE %s
                LIMIT 3
                """,
                (location,)
            )
        result = cur.fetchone()
        cur.close()
        conn.close()
        if not result:
            return jsonify({"error": "Location not found in database"}), 404
        # Round to 2 decimal places, as some of the data records have multiple decimal places
        lat, lon = round(result[0], 2), round(result[1], 2)  
        # Request OpenWeatherMap API for real-time UV index
        response = requests.get(API_URL, params={
            "lat": lat,
            "lon": lon,
            "appid": API_KEY
        })
        if response.status_code != 200:
            return jsonify({"error": f"Failed to fetch UV index from API. Status: {response.status_code}, Response: {response.text}"}), 500
        uv_data = response.json()
        uv_index = uv_data.get("value")
        # Give UV protection suggestion based on UV Index
        if uv_index <= 2:
            suggestion = "Minimal protection needed, but sunscreen recommended for prolonged exposure."
        elif uv_index <= 5:
            suggestion = "Wear sunglasses, use SPF 30+, and seek shade around midday."
        elif uv_index <= 7:
            suggestion = "Wear protective clothing, SPF 50+, avoid midday sun (10 AM - 3 PM)."
        elif uv_index <= 10:
            suggestion = "Limit outdoor exposure, SPF 50+, wear a wide-brimmed hat and sunglasses."
        else:
            suggestion = "Avoid direct sun exposure, use SPF 50+, reapply sunscreen every 2 hours."
        return jsonify({
            "location": location,
            "lat": lat,
            "lon": lon,
            "uv_index": uv_index,
            "suggestion": suggestion
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
if __name__ == '__main__':
    app.run(debug=True, port=5000)