from flask import jsonify
from app import app, mongo  # Assuming your Flask app instance and PyMongo instance are named 'app' and 'mongo'

@app.route('/test-mongodb')
def test_mongodb():
    try:
        # Perform a simple database operation (e.g., query a collection)
        # For example, you can count the number of documents in a collection
        count = mongo.db.task_manager.count_documents({})
        return jsonify({'message': 'MongoDB connection successful', 'count': count})
    except Exception as e:
        return jsonify({'message': 'Error connecting to MongoDB', 'error': str(e)}), 500
    
    from flask import jsonify

from bson import ObjectId  # Import ObjectId from bson module

@app.route('/display-data')
def display_data():
    try:
        # Query MongoDB to retrieve data
        data = mongo.db.tasks.find()  # Replace 'your_collection_name' with the actual collection name

        # Convert MongoDB cursor to a list of dictionaries
        data_list = []
        for doc in data:
            # Convert ObjectId fields to string representation
            doc['_id'] = str(doc['_id'])
            data_list.append(doc)

        # Return JSON response with data
        return jsonify({'message': 'Data retrieved successfully', 'data': data_list})
    except Exception as e:
        return jsonify({'message': 'Error retrieving data from MongoDB', 'error': str(e)}), 500

@app.route('/test-mongodb')
def test_mongodb():
    try:
        # Perform a simple database operation (e.g., count the number of documents in a collection)
        count = mongo.db.users.count_documents({})
        return jsonify({'message': 'MongoDB connection successful', 'count': count})
    except Exception as e:
        return jsonify({'message': 'Error connecting to MongoDB', 'error': str(e)}), 500

