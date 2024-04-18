import requests
import ngrok
import flask 
from flask import request, jsonify
import json

listener = ngrok.forward(8080,authtoken = '2eVi28Pi3ZLf6747w11xhsZ3Lbe_2B4eYebM2BKrm9uvdFbT', domain = "shipitdone.ngrok.app")

laptop_ips = {}

user_ips = {}

app = flask.Flask(__name__)

@app.route('/get_data', methods = ['GET'])
def get_data():
    return user_ips

@app.route('/user_signup' ,methods = ['POST'])
def pi_signup():
    data = request.json
    userID = str(data["userID"])
    user_ip = "10.32.27.21"
    user_ips[userID] = user_ip
    if userID in laptop_ips.keys():
        requests.post("http://" + user_ip + ":5005/laptop_ip", json={"ip": laptop_ips[userID] })
    
    print("User: ", userID, user_ip)

    return {"status": "success"}

@app.route('/laptop_signup', methods = ['POST'])
def laptop_signup():
    data = request.json
    print(data)
    userID = str(data['userID'])
    laptop_ip = str(data['laptop_ip'])
    print("userID", userID)
    print("laptop_ip", laptop_ip)

    if userID in user_ips.keys():
        requests.post("http://" + user_ips[userID] + ":5005/laptop_ip", json={"ip": laptop_ip })
    
    laptop_ips[userID] = laptop_ip
    # print(data)
    return {"status": "success"}

@app.route('/router', methods = ['POST'])
def router():
    data = request.get_json(force=True)
    userID = str(data["userID"])

    print(data)

    if userID in user_ips.keys():
        ip = user_ips[userID]
        requests.post("http://10.32.27.21:5005/update", json=data)
        print("sent data")
    
    return {"status": "success"}

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=8080)
