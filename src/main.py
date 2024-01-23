from flask import Flask, request, redirect, jsonify
from pymongo import MongoClient
import os
import requests
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv() 

def serialize_doc(doc):
    doc["_id"] = str(doc["_id"]) 
    return doc

class MongoConnector:
    def __init__(self, app, uri):
        self.app = app
        try:
            client = MongoClient(uri, serverSelectionTimeoutMS=5000)
            client.server_info() # Force a call to check the connection
            self.db = client.datastream
            self.register_routes()
        except:
            print("MongoDB connection failed. Limited functionality.")

    def register_routes(self):
        self.register_actions_crud_routes()
        self.register_datastream_crud_routes()

    def register_datastream_crud_routes(self):
        collection = self.db.datastreams

        @self.app.route('/datastreams', methods=['POST'])
        def create_datastream():
            data = request.json
            if not data.get('userid') or not data.get('uuid'):
                return jsonify({'error': 'Missing userid or uuid'}), 400

            document_id = collection.insert_one(data).inserted_id
            return jsonify({'message': 'Datastream created', 'id': str(document_id)}), 201  # Convert ObjectId to string

        @self.app.route('/datastreams/<userid>', methods=['GET'])
        def read_datastreams(userid):
            documents = collection.find({'userid': userid})
            return jsonify([serialize_doc(doc) for doc in documents]), 200

        @self.app.route('/datastream/<uuid>', methods=['GET'])
        def read_datastream(uuid):
            document = collection.find_one({'uuid': uuid})
            if document:
                return jsonify(serialize_doc(document)), 200
            else:
                return jsonify({'error': 'Datastream not found'}), 404

        @self.app.route('/datastream/<uuid>', methods=['PUT'])
        def update_datastream(uuid):
            data = request.json
            result = collection.update_one({'uuid': uuid}, {'$set': data})
            if result.matched_count:
                return jsonify({'message': 'Datastream updated'}), 200
            else:
                return jsonify({'error': 'Datastream not found'}), 404

        @self.app.route('/datastream/<uuid>', methods=['DELETE'])
        def delete_datastream(uuid):
            result = collection.delete_one({'uuid': uuid})
            if result.deleted_count:
                return jsonify({'message': 'Datastream deleted'}), 200
            else:
                return jsonify({'error': 'Datastream not found'}), 404
   
    def register_actions_crud_routes(self):
        collection = self.db.actions

        @self.app.route('/actions', methods=['POST'])
        def create_action():
            data = request.json
            if not data.get('userid') or not data.get('uuid'):
                return jsonify({'error': 'Missing userid or uuid'}), 400

            document_id = collection.insert_one(data).inserted_id
            return jsonify({'message': 'Action created', 'id': str(document_id)}), 201  # Convert ObjectId to string

        @self.app.route('/actions/<userid>', methods=['GET'])
        def read_actions(userid):
            documents = collection.find({'userid': userid})
            return jsonify([serialize_doc(doc) for doc in documents]), 200

        @self.app.route('/action/<uuid>', methods=['GET'])
        def read_action(uuid):
            document = collection.find_one({'uuid': uuid})
            if document:
                return jsonify(serialize_doc(document)), 200
            else:
                return jsonify({'error': 'Action not found'}), 404

        @self.app.route('/action/<uuid>', methods=['PUT'])
        def update_action(uuid):
            data = request.json
            result = collection.update_one({'uuid': uuid}, {'$set': data})
            if result.matched_count:
                return jsonify({'message': 'Action updated'}), 200
            else:
                return jsonify({'error': 'Action not found'}), 404

        @self.app.route('/action/<uuid>', methods=['DELETE'])
        def delete_action(uuid):
            result = collection.delete_one({'uuid': uuid})
            if result.deleted_count:
                return jsonify({'message': 'Action deleted'}), 200
            else:
                return jsonify({'error': 'Action not found'}), 404
        
app = Flask(__name__)
mongo_connector = MongoConnector(app, os.getenv('MONGODB_URI'))
CORS(app, resources={r"/*": {"origins": ["http://localhost:3001"]}})

@app.route('/auth')
def auth():
    print('received something')
    code = request.args.get('code')
    data = {
        'grant_type': 'authorization_code',
        'client_id': os.getenv('CLIENT_ID'),
        'client_secret': os.getenv('CLIENT_SECRET'),
        'redirect_uri': f'{os.getenv('HOST_URI')}/auth',
        'code': code
    }
    
    response = requests.post(os.getenv('ENDPOINT_TOKEN'), data=data)
    
    if response.status_code == 200:
        session_token = response.json().get('access_token')
        userinfo_endpoint = os.getenv('ENDPOINT_USER_INFO')
        token = session_token
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        response = requests.get(userinfo_endpoint, headers=headers)
        if response.status_code == 200:
            user_info = response.json()
            return redirect(f'{os.getenv('FRONTEND_URI')}/auth?sub={user_info['sub']}')
        else:
            print("Failed to retrieve user info. Status Code:", response.status_code)
            print("Response:", response.text)
                
    else:
        return redirect(f'{os.getenv('FRONTEND_URI')}/error')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv('HOST_PORT'))

