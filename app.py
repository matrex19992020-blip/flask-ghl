from flask import Flask, jsonify
import requests
from flask_cors import CORS
import os

app = Flask(__name__)
# Allow all origins for development
CORS(app)

# Mock data matching your UI design
MOCK_DATA = {
    "data": [
        {
            "id": "2024-001A",
            "name": "STARLINK 2240",
            "objectClass": "Payload",
            "mass": 260,
            "mission": "Commercial Communications",
            "reentry": {
                "epoch": "2024-11-15T14:30:00Z"
            },
            "cosparId": "2024-001A",
            "satno": 58001,
            "launch": {
                "epoch": "2024-01-10T08:15:00Z"
            }
        },
        {
            "id": "2023-187B",
            "name": "STARLINK 6123",
            "objectClass": "Payload",
            "mass": 305,
            "mission": "Commercial Communications",
            "reentry": {
                "epoch": "2024-10-28T09:15:00Z"
            },
            "cosparId": "2023-187B",
            "satno": 57823,
            "launch": {
                "epoch": "2023-08-22T11:30:00Z"
            }
        },
        {
            "id": "2023-156C",
            "name": "STARLINK 4564",
            "objectClass": "Payload",
            "mass": 295,
            "mission": "Commercial Communications",
            "reentry": {
                "epoch": "2024-09-20T16:45:00Z"
            },
            "cosparId": "2023-156C",
            "satno": 57456,
            "launch": {
                "epoch": "2023-05-15T19:00:00Z"
            }
        },
        {
            "id": "2024-078D",
            "name": "STARLINK 7891",
            "objectClass": "Payload",
            "mass": 268,
            "mission": "Commercial Communications",
            "reentry": {
                "epoch": "2024-08-14T12:20:00Z"
            },
            "cosparId": "2024-078D",
            "satno": 59234,
            "launch": {
                "epoch": "2024-03-05T06:45:00Z"
            }
        },
        {
            "id": "2023-089A",
            "name": "STARLINK 5432",
            "objectClass": "Payload",
            "mass": 310,
            "mission": "Commercial Communications",
            "reentry": {
                "epoch": "2024-07-08T18:30:00Z"
            },
            "cosparId": "2023-089A",
            "satno": 56789,
            "launch": {
                "epoch": "2023-04-12T14:20:00Z"
            }
        },
        {
            "id": "2022-089A",
            "name": "COSMOS 2558",
            "objectClass": "Payload",
            "mass": 1450,
            "mission": "Military Communications",
            "reentry": {
                "epoch": "2024-06-05T11:20:00Z"
            },
            "cosparId": "2022-089A",
            "satno": 52891,
            "launch": {
                "epoch": "2022-08-30T10:00:00Z"
            }
        },
        {
            "id": "2023-045E",
            "name": "STARLINK 3987",
            "objectClass": "Payload",
            "mass": 285,
            "mission": "Commercial Communications",
            "reentry": {
                "epoch": "2024-05-18T08:45:00Z"
            },
            "cosparId": "2023-045E",
            "satno": 55321,
            "launch": {
                "epoch": "2023-02-08T16:30:00Z"
            }
        },
        {
            "id": "2021-045D",
            "name": "ONEWEB-0412",
            "objectClass": "Payload",
            "mass": 148,
            "mission": "Commercial Communications",
            "reentry": {
                "epoch": "2024-04-12T07:30:00Z"
            },
            "cosparId": "2021-045D",
            "satno": 48234,
            "launch": {
                "epoch": "2021-06-15T05:20:00Z"
            }
        },
        {
            "id": "2023-112C",
            "name": "STARLINK 6745",
            "objectClass": "Payload",
            "mass": 298,
            "mission": "Commercial Communications",
            "reentry": {
                "epoch": "2024-03-25T13:10:00Z"
            },
            "cosparId": "2023-112C",
            "satno": 57112,
            "launch": {
                "epoch": "2023-07-19T09:40:00Z"
            }
        },
        {
            "id": "2022-156B",
            "name": "STARLINK 4201",
            "objectClass": "Payload",
            "mass": 275,
            "mission": "Commercial Communications",
            "reentry": {
                "epoch": "2024-02-14T15:55:00Z"
            },
            "cosparId": "2022-156B",
            "satno": 53456,
            "launch": {
                "epoch": "2022-11-03T12:15:00Z"
            }
        }
    ],
    "metadata": {
        "total": 10,
        "page": 1,
        "pageSize": 100
    }
}

@app.route('/')
def home():
    return jsonify({"message": "Space Debris API is running (MOCK MODE)"})

@app.route('/api/space-debris', methods=['GET'])
def get_space_debris():
    # Set USE_MOCK to True for testing, False for production
    USE_MOCK = os.environ.get('USE_MOCK', 'true').lower() == 'true'
    
    if USE_MOCK:
        # Return mock data
        return jsonify(MOCK_DATA)
    else:
        # Use real API
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
            return jsonify({"error": "Failed to fetch data", "status": response.status_code}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
