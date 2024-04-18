import requests
import socket
import json
def send_to_central():
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    username = employee@shipitdone.com
    info = json.dumps({'username': username , 'ip' : ip})
    requests.post('https://shipitdone.ngrok.app/laptop_signup', json = info)
   
