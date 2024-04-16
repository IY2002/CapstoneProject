import requests
import socket

def send_to_central():
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    username = employee@shipitdone.com
    info = {'username',ip}
    requests.post('https://shipitdone.ngrok.app', json = info)
   
