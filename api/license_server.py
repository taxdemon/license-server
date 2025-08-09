from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# License keys (you can edit these as needed)
LICENSE_KEYS = {
    "RACE-7B3F-9K2P-4M6Q": {"max_devices": 3, "valid_days": 365},
    "RACE-1A2B-3C4D-5E6F": {"max_devices": 5, "valid_days": 180}
}

@app.route('/activate', methods=['POST'])
def activate():
    data = request.json
    
    # 1. Check if 'key' and 'hardware_id' are provided
    if not data.get('key') or not data.get('hardware_id'):
        return jsonify({"error": "Missing required fields: key or hardware_id"}), 400
    
    # 2. Check license key
    if data['key'] not in LICENSE_KEYS:
        return jsonify({"error": "Invalid license key"}), 400
    
    # 3. Check hardware ID (optional, can be used for tracking device)
    hardware_id = data['hardware_id']
    
    # 4. Calculate expiration date based on the license key
    expires = (datetime.now() + timedelta(days=LICENSE_KEYS[data['key']]['valid_days'])).strftime("%Y-%m-%d")
    
    # 5. Return success response with expiration date and hardware ID
    return jsonify({
        "status": "active",
        "expires": expires,
        "hardware_id": hardware_id
    })

# Vercel doesn't need to run the app with app.run() directly.
# Flask will automatically handle requests via the serverless function provided by Vercel.

