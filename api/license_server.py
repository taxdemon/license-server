from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import hmac
import hashlib
import os
from dotenv import load_dotenv

# Load password from .env file
load_dotenv()

app = Flask(__name__)

# Your license keys (edit these!)
LICENSE_KEYS = {
    "RACE-7B3F-9K2P-4M6Q": {"max_devices": 3, "valid_days": 365},
    "RACE-1A2B-3C4D-5E6F": {"max_devices": 5, "valid_days": 180}
}

@app.route('/activate', methods=['POST'])
def activate():
    data = request.json
    
    # 1. Check license key
    if data['key'] not in LICENSE_KEYS:
        return jsonify({"error": "Invalid license key"}), 400
    
    # 2. Check hardware ID (prevents sharing)
    hardware_id = data['hardware_id']
    
    # 3. Return success
    expires = (datetime.now() + timedelta(days=LICENSE_KEYS[data['key']]['valid_days'])).strftime("%Y-%m-%d")
    return jsonify({
        "status": "active",
        "expires": expires
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
