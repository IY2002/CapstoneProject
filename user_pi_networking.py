import requests
import flask
import socket
from flask import request
app = flask.Flask(__name__)
laptop_ip = ""
laptop_id = ""
@app.route('/laptop_ip', methods = ['POST'])
def get_laptop_ip():
    data = request.get_json(force = True)
    laptop_ip = data["ip"]
    laptop_id = data["userID"]

def send_print_label():
    requests.post(laptop_ip + "/print_label")

def send_print_doc():
    requests.post(laptop_ip + "/print_doc")


def send_user_ip():
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    userID = "123"
    info = {'username' : userID, 'ip' : ip}
    requests.post('https://shipitdone.ngrok.app/user_signup', json = info)