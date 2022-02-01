from unicodedata import name
from flask import request, jsonify, make_response
from emp_details.database import db_session
import emp_details.models as models
from emp_details import app


@app.route('/employee', methods=['GET', 'POST', 'DELETE'])
def employee():
    print(request.method)
    if(request.method == 'GET'):
        # access query parameters
        users = models.User.query.all()
        return jsonify([user.to_json() for user in users])

    if(request.method == 'POST'):
        # get the data from the POST body
        data = request.get_json()
        print(data)
        # create a new user object
        name = data['name']
        email = data['email']
        department = data['department']
        new_user = models.User(name, email, department)
        try:
            db_session.add(new_user)
            db_session.commit()
            db_session.refresh(new_user)
        except Exception as e:
            print(e)
            return jsonify({'error': 'Unable to add user'}), 409
        return jsonify(new_user.to_json()), 201


@app.route('/employee/<int:emp_id>', methods=['GET', 'PUT', 'DELETE'])
def employee_with_id(emp_id):
    if(request.method == 'GET'):
        user = models.User.query.get(emp_id)
        if(user is not None):
            return jsonify(user.to_json())
        else:
            return jsonify({'error': 'User not found'}), 404

    if(request.method == 'DELETE'):
        user = models.User.query.get(emp_id)

        if(user == None):
            return jsonify({'error': 'User not found'}), 404

        db_session.delete(user)
        db_session.commit()
        return jsonify({"status": "deleted successfully"}), 204

    if(request.method == 'PUT'):
        user = models.User.query.get(emp_id)

        if(user == None):
            return jsonify({'error': 'User not found'}), 404

        # get the data from the POST body
        data = request.get_json()
        user.name = data['name']
        user.email = data['email']
        user.department = data['department']
        try:
            db_session.commit()
        except Exception as e:
            print(e)
            return jsonify({'error': 'Unable to update user'}), 409
        return jsonify(user.to_json())


@app.route('/')
def home():
    session = db_session()
    res = session.query(models.User).all()
    return jsonify([user.to_json() for user in res])
