from flask import Flask, jsonify, request
import os
import w3storage

w3s = os.environ['w3s']
w3 = w3storage.API(token=w3s)

some_uploads = w3.user_uploads(size=25)

print(some_uploads)

hello_cid = w3.post_upload(('sample.txt', 'hey there'))

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