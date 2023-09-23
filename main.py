from flask import Flask, jsonify, request

app = Flask('app')


@app.route('/')
def hello_world():
  return 'Hello, World!'


@app.route('/input', methods=['POST'])
def handle_post_request():
  data = request.get_json()

  name = data.get('name')
  ssn = data.get('ssn')
  passport = data.get('passport')
  dob = data.get('dob')

  print("hey", name, ssn, passport, dob)

  response_data = {'message': 'Data received successfully'}
  return jsonify(response_data), 200


app.run(host='0.0.0.0', port=8080)