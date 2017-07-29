#!flask/bin/python
from flask import Flask
from flask import request, jsonify, abort, session, render_template, send_from_directory
from flask_cors import CORS, cross_origin
import uuid
import os
import json
from datetime import date
from dateutil.rrule import rrule, DAILY
import myfitnesspal
from customexceptions import InvalidUsage
from utils import *
from collections import Counter
# from tornado.wsgi import WSGIContainer
# from tornado.httpserver import HTTPServer
# from tornado.ioloop import IOLoop


class CustomFlask(Flask):
  jinja_options = Flask.jinja_options.copy()
  jinja_options.update(dict(
  block_start_string='$$',
  block_end_string='$$',
  variable_start_string='$',
  variable_end_string='$',
  comment_start_string='$#',
  comment_end_string='#$',
))

# Allow flask to serve static files
template_dir = os.path.abspath('./client/')
assets_dir = os.path.abspath('./client/dist')
app = CustomFlask(__name__, template_folder=template_dir)

# Enable CORS
CORS(app)

@app.route('/') 
def index():
  return render_template('index.html')
# Send static files
@app.route('/dist/<path:path>')
def serve_assets(path):
  return send_from_directory(assets_dir, path)

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

  if start > end:
    raise InvalidUsage('Must enter valid date range.', status_code=400)
  else:
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

@app.route('/api/login', methods=['POST'])
def login():
  if not request.json or not 'username' in request.json or not 'password' in request.json:
    return jsonify({"error": "Invalid request format"}), 404
  else:
    if session.get('logged_in'):
      return jsonify(success=True), 200
    else:
      try:
        # Strip the unicode
        username = str(request.json['username'])
        client = myfitnesspal.Client(username, request.json['password'])
        clients[username] = client
        session['logged_in'] = True
        session['username'] = username
        print(session)
        return jsonify(success=True), 200
      except ValueError:
        raise InvalidUsage('Invalid Credentials', status_code=401)

@app.route('/api/logout', methods=['POST'])
def logout():
  if 'username' not in session:
    raise InvalidUsage('Not Logged In', status_code=401)
  else:
    del clients[session['username']]
    session.clear()
    return jsonify(Success=True), 200

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

    if start > end:
      raise InvalidUsage('Must enter valid date range', status_code=400)
    else:
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

# Averages
@app.route('/api/average/totals', methods=['GET'])
def average_totals():
  print(session)
  if 'username' in session:
    date_range = get_date_range(request)

    totals = Counter(date_range[0].totals)
    days = len(date_range)

    if not totals:
      days -= 1

    for day in date_range[1:]:
      date = day.date.strftime('%m/%d/%Y')
      if day.totals:
        totals += Counter(day.totals)
      else:
        days -= 1
    for key in totals:
      totals[key] /= days
    return jsonify({'totals': totals, 'trackedDays': days})
  else:
    raise InvalidUsage('Access Denied', status_code=403)


# @app.route('/test', methods=['GET'])
# def test():
#   print('User is downloading file')
#   uploads = os.path.join(os.getcwd(), 'static')
#   return send_from_directory(directory=uploads, filename='app.apk', as_attachment=True, attachment_filename='app.apk')


if __name__ == '__main__':
  # app.secret_key = os.urandom(12)
  # http_server = HTTPServer(WSGIContainer(app))
  # http_server.listen(5000)
  # IOLoop.instance().start()
  app.secret_key = os.urandom(12)
  app.run(port=5000, threaded=True)
