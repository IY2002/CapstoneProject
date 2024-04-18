#from demo2 import setup
#from page_handler import idle_screen, unidle_screen
#from page_setup import page_setup
import requests
import ngrok
import flask 
from flask import request, jsonify
import threading
import os
user_info = {}
app = flask.Flask(__name__)
def routing():
    @app.route('/router', methods = ['POST'])
    def router():
        data = request.get_json(force=True)
        userID = data["userID"]

        if userID in user_info:
            ip = user_info[userID]
            requests.post(ip, data)