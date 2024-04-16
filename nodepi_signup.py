#from demo2 import setup
#from page_handler import idle_screen, unidle_screen
#from page_setup import page_setup
import requests
import ngrok
import flask 
from flask import request, jsonify
import threading
import os
from nodepi_router import routing
from nodepi_router import app
from nodepi_router import user_info
#import both app and routing function from other file
#importing app from other file to avoid circular dependency
#need to get paid plan to use domain
listener = ngrok.forward(8080,authtoken = '2eq2WxQMV2gKe379SXbMb3Cw7bj_648cU7cn9Zh4Kg4K7ZdqL', domain = "<bedbug-eminent-martin.ngrok-free.app>")


@app.route('/signup' ,methods = ['POST'])
def signup():
    data = request.json
    userID = data["userID"]
    ip = data["ip"]
    user_info[userID] = ip





if __name__ == '__main__':
    server_thread = threading.Thread(target=routing)
    server_thread.daemon = True
    server_thread.start()
    app.run(host='0.0.0.0', port=8080)
