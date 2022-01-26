from database import db_session
from flask import Flask, render_template, url_for, request, redirect, jsonify
import models

app = Flask(__name__)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route('/employee', methods=['GET', 'POST', 'DELETE'])
def employee():
    print(request.method)
    if(request.method == 'GET'):
        users = models.User.query.all()
        return jsonify([user.to_json() for user in users])

    if(request.method == 'POST'):
        name = request.form['name']
        email = request.form['email']
        department = request.form['department']
        new_user = models.User(name, email, department)
        db_session.add(new_user)
        db_session.commit()
        db_session.refresh(new_user)

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
            return jsonify({'error': 'User not found'})

        user.name = request.form['name']
        user.email = request.form['email']
        user.department = request.form['department']
        db_session.commit()
        return jsonify(user.to_json())


@app.route('/')
def home():
    session = db_session()
    res = session.query(models.User).all()
    return jsonify([user.to_json() for user in res])


if __name__ == '__main__':
    app.run(debug=True)
