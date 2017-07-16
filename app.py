#!flask/bin/python
from flask import Flask
from flask import request, jsonify, abort, session, render_template
from flask.sessions import SessionInterface
from beaker.middleware import SessionMiddleware
import uuid
import os
import json
import myfitnesspal;

app = Flask(__name__)

clients = {}

@app.before_request
def session_management():
  session.permanent = True

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/api/login', methods=['POST'])
def login():
  print(session)
  if not request.json or not 'username' in request.json or not 'password' in request.json:
    return jsonify({"error": "Invalid request format"}), 404
  else:
    if session.get('logged_in'):
      return jsonify({"success": False, "data": {"message": "already logged in"}}), 200
    else:
      try:
        client = myfitnesspal.Client(request.json['username'], request.json['password'])
        clients[request.json['username']] = client
        session['logged_in'] = True
        session['username'] = request.json['username']
        print(session)
        print(session.get('logged_in'))
        print(session.get('username'))
        return jsonify({"success": True, "data": {"username": request.json['username']}}), 200
      except ValueError:
        return jsonify({"success": False, "data": {"message": "invalid credentials"}}), 404

@app.route('/api/logout', methods=['POST'])
def logout():
  if not session.get('logged_in'):
    return jsonify({"success": False})
  else:
    session.clear()
    del clients[session.get('username')]
    return index()

@app.route('/api/day/totals', methods=['GET'])
def totals():
  if 'username' in session:
    username = session['username']
    client = clients[username]
    print(request)
    year = request.headers['year']
    month = request.headers['month']
    day = request.headers['day']

    data = client.get_date(year, month, day)
    print(type(data))
    print(data.meals)
    print(data.totals)
    print(data.water)
    print(data.notes)
    print(data)
    return jsonify(data.totals), 200

  else:
    return jsonify({"success": False, "data": {"message": "Not logged in"}}), 404

@app.route('/api/day/meals', methods=['GET'])
def meals():
  if 'username' in session:
    client = clients[session['username']]

    year = request.headers['year']
    month = request.headers['month']
    day = request.headers['day']
    date = client.get_date(year, month, day)
    
    jsonObj = {}
    for meal in date.meals:
      mealObj = {}
      for entry in meal:
        entryDict = entry.get_as_dict()
        mealObj[entryDict['name']] = entryDict['nutrition_information']
      jsonObj[meal.name] = mealObj
    return jsonify(jsonObj)

@app.route('/api/day/entries', methods=['GET'])
def entries():
  if 'username' in session:
    client = clients[session['username']]

    year = request.headers['year']
    month = request.headers['month']
    day = request.headers['day']
    date = client.get_date(year, month, day)
    
    jsonObj = {}
    for meal in date.meals:
      for entry in meal:
        entryDict = entry.get_as_dict()
        jsonObj[entryDict['name']] = entryDict['nutrition_information'];

    return jsonify(jsonObj)


if __name__ == '__main__':
  app.secret_key = os.urandom(12)
  app.run(debug=True)
