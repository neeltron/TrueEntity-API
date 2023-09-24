from flask import Flask, jsonify, request
import requests
from replit import db
import os
import w3storage
import qrcode

w3s = os.environ['w3s']
w3 = w3storage.API(token=w3s)

app = Flask('app', static_folder = 'static')

@app.route('/')
def hello_world():
  return 'Hello, World!'

@app.route('/input', methods = ['POST'])
def handle_post_request():
  data = request.get_json()

  name = data.get('name')
  ssn = data.get('ssn')
  passport = data.get('passport')
  dob = data.get('dob')
  userdata = name + ', ' + ssn + ', ' + passport + ', ' + dob
  hello_cid = w3.post_upload(('sample.txt', userdata))
  print(hello_cid)
  db[name] = hello_cid
  
  response_data = {'message': 'Data received successfully'}
  image = qrcode.make(userdata)
  image.save('qrcode.png')
  return jsonify(response_data), 200

@app.route('/data', methods = ['GET'])
def data():
  name = request.args.get('name')
  url = "https://" + db[name] + ".ipfs.w3s.link"
  response = requests.get(url)
  print(response)
  return jsonify(data=response.text), 200

app.run(host='0.0.0.0', port=8080)