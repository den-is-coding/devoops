import json
from flask import Flask, request, jsonify
from flask-mongoengine import MongoEngine

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'db': 'test',
    'host': '128.199.5.33',
    'port': 27017,
    'username': 'erick',
    'password': 'nDGzT&c7E2k8a',
}
db = MongoEngine()
db.init_app(app)

class User(db.Document):
    name = db.StringField()
    email = db.StringField()
    role = db.StringField()
    unique_facial_id = db.StringField()
    def to_json(self):
        return {
            "name": self.name,
            "email": self.email,
            "role" : self.role,
            "unique_facial_id" : self.unique_facial_id
        }


@app.route('/', methods=['GET'])
def query_records():
    email = request.args.get('email')
    user = User.objects(email=email).first()
    if not user:
        return jsonify({'error': 'data not found'})
    else:
        return jsonify(user.to_json())

@app.route('/', methods=['PUT'])
def create_record():
    record = json.loads(request.data)
    user = User(name=record['name'],
                email=record['email'],
                role=record['role'],
                unique_facial_id=record['unique_facial_id']
                )
    user.save()
    return jsonify(user.to_json())

@app.route('/', methods=['POST'])
def update_record():
    record = json.loads(request.data)
    user = User.objects(email=record['email']).first()
    if not user:
        return jsonify({'error': 'data not found'})
    else:
        user.update(name=record['name'],email=record['email'], role=record['role'], unique_facial_id=record['unique_facial_id'])
    return jsonify(user.to_json())

@app.route('/', methods=['DELETE'])
def delete_record():
    record = json.loads(request.data)
    user = User.objects(email=record['email']).first()
    if not user:
        return jsonify({'error': 'data not found'})
    else:
        user.delete()
    return jsonify(user.to_json())

@app.route('/all_users', methods=['POST'])
def get_all_users():
    record = json.loads(request.data)
    user = User.objects(email=record['email']).first()
    print(user)
    if not user:
        return jsonify({'error': 'user dont exist'})
    else:
        if user['role'] == 'admin':
            return jsonify(User.objects())
        else:
            return jsonify({'error': 'no access, bad role'})


if __name__ == "__main__":
    app.run()

