from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from app import app

mongo = PyMongo(app)

class User:
    def __init__(self, username, password, role='regular'):
        self.username = username
        self.password = password
        self.role = role

    @staticmethod
    def find_by_username(username):
        return mongo.db.users.find_one({'username': username})

    def save(self):
        mongo.db.users.insert_one({'username': self.username, 'password': self.password, 'role': self.role})

class Task:
    def __init__(self, title, description, assigned_to=None, status='pending'):
        self.title = title
        self.description = description
        self.assigned_to = assigned_to
        self.status = status

    @staticmethod
    def find_by_id(task_id):
        return mongo.db.tasks.find_one({'_id': ObjectId(task_id)})

    def save(self):
        mongo.db.tasks.insert_one({'title': self.title, 'description': self.description, 'assigned_to': self.assigned_to, 'status': self.status})
