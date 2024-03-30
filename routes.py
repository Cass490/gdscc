from flask import Flask, request, jsonify, make_response
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from app import app
from models import User, Task
import bcrypt
import jwt
import datetime
from functools import wraps
from utils import db

mongo = PyMongo(app)

app.config['SECRET_KEY'] = 'your_secret_key'

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.find_by_username(data['username'])
        except:
            return jsonify({'message': 'Token is invalid'}), 401

        return f(current_user, *args, **kwargs)

    return decorated

@app.route('/api/login', methods=['POST'])
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    user = User.find_by_username(auth.username)

    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    if bcrypt.checkpw(auth.password.encode('utf-8'), user['password']):
        token = jwt.encode({'username': user['username'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, app.config['SECRET_KEY'])

        return jsonify({'token': token.decode('UTF-8')})

    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

@app.route('/api/tasks', methods=['POST'])
@token_required
def create_task(current_user):
    data = request.get_json()

    title = data.get('title')
    description = data.get('description')
    assigned_to = data.get('assigned_to')

    if not title or not description:
        return jsonify({'message': 'Missing required fields'}), 400

    task = Task(title, description, assigned_to)
    task.save()

    return jsonify({'message': 'Task created successfully'})

@app.route('/api/tasks/<string:task_id>', methods=['PUT'])
@token_required
def update_task(current_user, task_id):
    data = request.get_json()

    title = data.get('title')
    description = data.get('description')
    assigned_to = data.get('assigned_to')
    status = data.get('status')

    task = Task.find_by_id(task_id)

    if not task:
        return jsonify({'message': 'Task not found'}), 404

    task['title'] = title
    task['description'] = description
    task['assigned_to'] = assigned_to
    task['status'] = status

    mongo.db.tasks.update_one({'_id': ObjectId(task_id)}, {'$set': task})

    return jsonify({'message': 'Task updated successfully'})

@app.route('/api/tasks/<string:task_id>', methods=['DELETE'])
@token_required
def delete_task(current_user, task_id):
    task = Task.find_by_id(task_id)

    if not task:
        return jsonify({'message': 'Task not found'}), 404

    mongo.db.tasks.delete_one({'_id': ObjectId(task_id)})

    return jsonify({'message': 'Task deleted successfully'})
