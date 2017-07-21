#!flask/bin/python
from flask import Flask
from flask import request, jsonify, abort, session, render_template
from flask.sessions import SessionInterface
from beaker.middleware import SessionMiddleware
import uuid
import os
import json
from datetime import date
from dateutil.rrule import rrule, DAILY
import myfitnesspal
from customexceptions import InvalidUsage
from utils import *
from collections import Counter

app = Flask(__name__)

clients = {}

# Utility function to get the user:
def get_client():
  return clients[session['username']]


def get_date(request):
  client = get_client()
  year = request.headers['year']
  month = request.headers['month']
  day = request.headers['day']
  return client.get_date(year, month, day)

def get_date_range(request):
  dates = []

  client = get_client()

  start_year = int(request.headers['start-year'])
  start_month = int(request.headers['start-month'])
  start_day = int(request.headers['start-day'])

  end_year = int(request.headers['end-year'])
  end_month = int(request.headers['end-month'])
  end_day = int(request.headers['end-day'])

  start = date(start_year, start_month, start_day)
  end = date(end_year, end_month, end_day)

  for dt in rrule(DAILY, dtstart=start, until=end):
    year = int(dt.strftime("%Y"))
    month = int(dt.strftime("%m"))
    day = int(dt.strftime("%d"))
    dates.append(client.get_date(year, month, day))
    
  return dates  

### Routes

@app.errorhandler(InvalidUsage)
def handle_error(error):
  response = jsonify(error.to_dict())
  response.status_code = error.status_code
  return response

@app.before_request
def session_management():
  session.permanent = True

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/api/login', methods=['POST'])
def login():
  if not request.json or not 'username' in request.json or not 'password' in request.json:
    return jsonify({"error": "Invalid request format"}), 404
  else:
    if session.get('logged_in'):
      return jsonify({"success": False, "data": {"message": "already logged in"}}), 200
    else:
      try:
        client = myfitnesspal.Client(request.json['username'], request.json['password'])
        print(dir(client))
        clients[request.json['username']] = client
        session['logged_in'] = True
        session['username'] = request.json['username']
        return jsonify(Success=True), 200
      except ValueError:
        raise InvalidUsage('Invalid Credentials', status_code=401)

@app.route('/api/logout', methods=['POST'])
def logout():
  if not session.get('logged_in'):
    raise InvalidUsage('Not Logged In', status_code=401)
  else:
    session.clear()
    del clients[session.get('username')]
    return index()

### /api/day/
@app.route('/api/day/weight', methods=['GET'])
def get_weight():
  if 'username' in session:
    client = get_client()
    year = int(request.headers['year'])
    month = int(request.headers['month'])
    day = int(request.headers['day'])
    
    currentDate = date(year, month, day)
    try:
      weight = client.get_measurements(currentDate, currentDate)
      print(weight)
      return jsonify(weight)
    except ValueError:
      return jsonify({}), 204

  else:
    raise InvalidUsage('Access Denied', status_code=403)

@app.route('/api/day/totals', methods=['GET'])
def totals():
  if 'username' in session:
    date = get_date(request)
    return jsonify(date.totals), 200
  else:
    raise InvalidUsage('Access Denied', status_code=403)

@app.route('/api/day/meals', methods=['GET'])
def meals():
  if 'username' in session:
    date = get_date(request)
    return jsonify(get_meals(date))
  else:
    raise InvalidUsage('Access Denied', status_code=403)

@app.route('/api/day/entries', methods=['GET'])
def entries():
  if 'username' in session:
    date = get_date(request)
    
    entries = {}
    for meal in date.meals:
      for entry in meal:
        entryDict = entry.get_as_dict()
        entries[entryDict['name']] = entryDict['nutrition_information'];
    return jsonify(entries)
  else:
    raise InvalidUsage('Access Denied', status_code=403)

@app.route('/api/day/water', methods=['GET'])
def water():
  if 'username' in session:
    date = get_date(request)
    return jsonify(date.water)
  else:
    raise InvalidUsage('Access Denied', status_code=403)

@app.route('/api/range/totals', methods=['GET'])
def range_totals():
  if 'username' in session:
    date_range = get_date_range(request)

    totals = {}
    for day in date_range:
      date = day.date.strftime('%m/%d/%Y')
      totals[date] = day.totals
    return jsonify(totals)
  else:
    raise InvalidUsage('Access Denied', status_code=403)

@app.route('/api/range/meals', methods=['GET'])
def range_meals():
  if 'username' in session:
    date_range = get_date_range(request)

    meals = {}
    for day in date_range:
      date = day.date.strftime('%m/%d/%Y')
      meals[date] = get_meals(day)
    return jsonify(meals)
  else:
    raise InvalidUsage('Access Denied', status_code=403)

@app.route('/api/range/weight', methods=['GET'])
def get_weight_history():
  if 'username' in session:
    client = get_client()

    start_year = int(request.headers['start-year'])
    start_month = int(request.headers['start-month'])
    start_day = int(request.headers['start-day'])

    end_year = int(request.headers['end-year'])
    end_month = int(request.headers['end-month'])
    end_day = int(request.headers['end-day'])

    start = date(start_year, start_month, start_day)
    end = date(end_year, end_month, end_day)

    weight = client.get_measurements('Weight', end, start)
    res = {k.strftime('%Y/%m/%d') : v for k, v in weight.iteritems()}

    return jsonify(res)
  else:
    raise InvalidUsage('Access Denied', status_code=403)

@app.route('/api/range/entries', methods=['GET'])
def get_entries_history():
  if 'username' in session:
    date_range = get_date_range(request)

    entries = {}
    for date in date_range:
      for meal in date.meals:
        for entry in meal:
          if entry.short_name not in entries:
            obj = {
              'count': 1,
              'nutrition': entry.nutrition_information
            }
            entries[entry.short_name] = obj
          else:
            entries[entry.short_name]['count'] += 1
            old_entry = Counter(entries[entry.short_name]['nutrition'])
            new_entry = Counter(entry.nutrition_information)
            concat_entry = old_entry + new_entry
            entries[entry.short_name]['nutrition'] = concat_entry
              
    return jsonify(entries)
  else:
    raise InvalidUsage('Access Denied', status_code=403)

if __name__ == '__main__':
  app.secret_key = os.urandom(12)
  app.run(debug=True)
