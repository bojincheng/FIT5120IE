import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
import re
from database import get_db_connection
app = Flask(__name__)
# Enable cross original resource sharing
CORS(app)
API_KEY = "e2f745f4f5345d28044a4f1e6b883c48"
API_URL = "https://api.openweathermap.org/data/2.5/uvi"
# Regex pattern to sanitize input
def is_valid_location(location):
    return bool(re.match(r'^[a-zA-Z0-9\s-]+$', location))
@app.route('/get-uv-index', methods=['GET'])
def get_uv_index():
    location = request.args.get('location')
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        # If GPS coordinates are provided, find the nearest suburb
        if lat and lon:
            cur.execute(
                """
                SELECT locality FROM australian_postcode 
                ORDER BY (lat - %s)^2 + (long - %s)^2 ASC
                LIMIT 1
                """,
                (lat, lon)
            )
            suburb_result = cur.fetchone()
            suburb = suburb_result[0] if suburb_result else "Unknown Suburb"
        # If the user entered a location manually (postcode or suburb)
        elif location:
            if not is_valid_location(location):
                return jsonify({"error": "Invalid location name"}), 400
            # postcode input
            if location.isdigit():
                cur.execute(
                    """
                    SELECT lat, long, locality FROM australian_postcode 
                    WHERE postcode = %s
                    LIMIT 1
                    """,
                    (location,)
                )
            # suburb name input
            else:
                cur.execute(
                    """
                    SELECT lat, long, locality FROM australian_postcode 
                    WHERE locality ILIKE %s
                    LIMIT 1
                    """,
                    (location,)
                )
            result = cur.fetchone()
            if not result:
                return jsonify({"error": "Location not found"}), 404

            lat, lon, suburb = round(result[0], 2), round(result[1], 2), result[2]
        cur.close()
        conn.close()
        # Fetch UV index from API
        response = requests.get(API_URL, params={
            "lat": lat,
            "lon": lon,
            "appid": API_KEY
        })
        if response.status_code != 200:
            return jsonify({"error": f"Failed to fetch UV index from API. Status: {response.status_code}"}), 500
        uv_data = response.json()
        uv_index = uv_data.get("value")
        # UV protection suggestions
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
            "suburb": suburb,
            "lat": lat,
            "lon": lon,
            "uv_index": uv_index,
            "suggestion": suggestion
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
if __name__ == '__main__':
    app.run(debug=True, port=5000)




