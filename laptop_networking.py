import flask
import json
import requests
import socket
import webbrowser

def print_ip():
    hostname=socket.gethostname()
    IPAddr=socket.gethostbyname(hostname)
    return IPAddr

app = flask.Flask(__name__)

@app.route('/print_doc', methods=['POST'])
def print_doc():
    webbrowser.open('https://qz.shipitdone.com/ARK_Additional.html') #rollo_print_doc()
    return {"status": "success"}

@app.route('/print_label', methods=['POST'])
def print_label():
    webbrowser.open('https://qz.shipitdone.com/ARK.html')  #rollo_print_label()
    return {"status": "success"}

if __name__ == '__main__':
    ip = print_ip()
    requests.post('https://shipitdone.ngrok.app/laptop_signup', json=json.dumps({"laptop_ip": ip, "userID": "123"}))
    app.run(host='0.0.0.0', port=5000)

