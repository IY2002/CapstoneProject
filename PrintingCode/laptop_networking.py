import flask
import json
import requests
import socket
import webbrowser
import ngrok
import urllib.request
from flask import request

listener = ngrok.forward(5000, authtoken = '2fBaknExz6GyPXEY2Wdm2czL6UF_2b7fdD81atXVkH7k4zgpJ')
def print_ip():
    hostname=socket.gethostname()
    IPAddr=socket.gethostbyname(hostname)
    print(listener.url())
    return listener.url()

app = flask.Flask(__name__)

@app.route('/print_doc', methods=['POST'])
def print_doc():
    data = request.get_json(force=True)
    # url = data['url']
    # urllib.request.urlretrieve(url, 'D:/Capstone_Project/Sample 4x6 Label.pdf')
    printer = data['printer']
    doc_num = data['doc_num']
    if doc_num == 1:
        urllib.request.urlretrieve(url, 'D:/Capstone_Project/Additional file.pdf')
    elif doc_num == 2:
        urllib.request.urlretrieve(url, 'D:/Capstone_Project/Additional file.pdf')
    else:
        urllib.request.urlretrieve(url, 'D:/Capstone_Project/Additional file.pdf')
    if printer == 'Epson':
        webbrowser.open('https://qz.shipitdone.com/ARK_Additional.html')  # EPSON_print_doc()
    else:
        webbrowser.open('https://qz.shipitdone.com/Rollo_Additional.html') # rollo_print_doc()
    return {"status": "success"}

@app.route('/print_label', methods=['POST'])
def print_label():
    data = request.get_json(force=True)
    printer = data['printer']
    #url = data['url']
    #urllib.request.urlretrieve(url, 'D:/Capstone_Project/Sample 4x6 Label.pdf')
    if printer =='Epson':
        webbrowser.open('https://qz.shipitdone.com/ARK.html') # EPSON_print_label()
    else:
        webbrowser.open('https://qz.shipitdone.com/qz.html')  # rollo_print_label()
    return {"status": "success"}

if __name__ == '__main__':
    ip = print_ip()
    requests.post('https://shipitdone.ngrok.app/laptop_signup', json={"laptop_ip": ip, "userID": "123"})
    app.run(host='0.0.0.0', port=5000)

