#from demo2 import setup
#from page_handler import idle_screen, unidle_screen
#from page_setup import page_setup
import requests
import ngrok
import flask 
from flask import request, jsonify
# import threading
# import os
# from nodepi_router import routing
# from nodepi_router import app
# from nodepi_router import user_info
import json
#import both app and routing function from other file
#importing app from other file to avoid circular dependency
#need to get paid plan to use domain
listener = ngrok.forward(8080,authtoken = '2eVi28Pi3ZLf6747w11xhsZ3Lbe_2B4eYebM2BKrm9uvdFbT', domain = "shipitdone.ngrok.app")

laptop_ips = {}

user_ips = {}

app = flask.Flask(__name__)

@app.route('/pi_signup' ,methods = ['POST'])
def pi_signup():
    data = request.json
    userID = data["userID"]
    user_ip = data["ip"]
    user_ips[userID] = user_ip
    if userID in laptop_ips.keys:
        requests.post(user_ip + "/laptop_ip", json={"laptop_ip": laptop_ips[userID] + "/5000"})
    
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
        requests.post(user_ips[userID] + "/laptop_ip", json={"laptop_ip": laptop_ip + "/5000"})
    else:
        laptop_ips[userID] = laptop_ip
    # print(data)
    return {"status": "success"}

@app.route('/router', methods = ['POST'])
def router():
    data = request.get_json(force=True)
    userID = data["userID"]

    if userID in user_ips:
        ip = user_ips[userID]
        requests.post(ip + "/update", data)
    
    return {"status": "success"}

if __name__ == '__main__':
    # server_thread = threading.Thread(target=routing)
    # server_thread.daemon = True
    # server_thread.start()
    app.run(host='0.0.0.0', port=8080)
