import requests
import socket

def send_to_central():
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    username = employee@shipitdone.com
    info = {'username': username , 'ip' : ip}
    requests.post('https://shipitdone.ngrok.app/laptop_signup', json = info)
   
