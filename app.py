from flask import Flask
from flask_pymongo import PyMongo

# Flask app initialization
app = Flask(__name__)
app.secret_key = 'abcd'

# MongoDB connection setup
MONGO_URI = 'mongodb://localhost:27017/task_manager'  
app.config['MONGO_URI'] = MONGO_URI
mongo = PyMongo(app)
@app.route('/')
def home():
    return 'Welcome to the Task Manager API!'


# Import routes
from routes import *

if __name__ == '__main__':
    app.run(debug=True)
