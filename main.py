from flask import Flask, jsonify, request
import requests
from replit import db
import os
import w3storage
import json
import qrcode
from cryptography.fernet import Fernet

w3s = os.environ['w3s']
w3 = w3storage.API(token=w3s)

secret_key = Fernet.generate_key()
print(secret_key)
cipher_suite = Fernet(secret_key)

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
  data_json = json.dumps(userdata)
  encrypted_data = cipher_suite.encrypt(data_json.encode())
  print(encrypted_data)
  hello_cid = w3.post_upload(('sample.txt', encrypted_data))
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
  decrypted_data = cipher_suite.decrypt(response.text)
  data = json.loads(decrypted_data.decode())
  print(response, data)
  return jsonify(data=data), 200

app.run(host='0.0.0.0', port=8080)