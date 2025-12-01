from flask import Flask, jsonify
import requests
from flask_cors import CORS
import os

app = Flask(__name__)

# Allow only Netlify frontend to access the API
CORS(app, origins=["https://space-debris.netlify.app"])

@app.route('/')
def home():
    return jsonify({"message": "Space Debris API is running"})

@app.route('/api/space-debris', methods=['GET'])
def get_space_debris():
    token = "IjUxNDg2NGJhLTE4YzYtNGMyNi1hYjhiLWY2NWQ2ZWI2ZmZjNSI.oPVneREPBKjxLTPiXxoNoSL1Q0U"
    url = 'https://discosweb.esoc.esa.int/api/objects'
    
    headers = {
        'Authorization': f'Bearer {token}',
        'DiscosWeb-Api-Version': '2',
    }
    
    params = {
        'filter': "eq(objectClass,Payload)&gt(reentry.epoch,epoch:'2020-01-01')",
        'sort': '-reentry.epoch',
    }

    response = requests.get(url, headers=headers, params=params)

    if response.ok:
        return jsonify(response.json())
    else:
        return jsonify({"error": "Failed to fetch data"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
