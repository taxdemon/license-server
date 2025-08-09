import json
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Your license keys (edit these!)
LICENSE_KEYS = {
    "RACE-7B3F-9K2P-4M6Q": {"max_devices": 3, "valid_days": 365},
    "RACE-1A2B-3C4D-5E6F": {"max_devices": 5, "valid_days": 180}
}

def handler(request):
    """Handle requests for license activation"""
    data = request.json()
    
    # 1. Check if 'key' and 'hardware_id' are provided
    if not data.get('key') or not data.get('hardware_id'):
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Missing required fields: key or hardware_id"})
        }
    
    # 2. Check license key
    if data['key'] not in LICENSE_KEYS:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Invalid license key"})
        }
    
    # 3. Calculate expiration date based on the license key
    expires = (datetime.now() + timedelta(days=LICENSE_KEYS[data['key']]['valid_days'])).strftime("%Y-%m-%d")
    
    # 4. Return success response
    return {
        "statusCode": 200,
        "body": json.dumps({
            "status": "active",
            "expires": expires
        })
    }
