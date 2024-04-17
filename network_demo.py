import requests
from demo2 import setup
from page_handler import idle_screen, unidle_screen
from page_setup import page_setup
import flask 
from flask import request, jsonify
import threading
import socket
from SingletonDeckState import SingletonDeckState

app = flask.Flask(__name__)

deck_state = SingletonDeckState()

@app.route('/laptop_ip', methods = ['POST'])
def get_laptop_ip():
    data = request.get_json(force = True)
    deck_state.laptop_ip = data["ip"]
    # deck_state.laptop_id = data["userID"]
    print("Recieved IP: ", deck_state.laptop_ip)
    return {"status" : "success"}

def send_print_label():
    requests.post(deck_state.laptop_ip + "/print_label")

def send_print_doc():
    requests.post(deck_state.laptop_ip + "/print_doc")


def send_user_ip():
    # hostname = socket.gethostname()
    # ip = socket.gethostbyname(hostname)
    userID = "123"
    info = {'userID' : userID, 'ip' : "10.32.27.21"}
    # print("ip: ", ip)
    requests.post('http://shipitdone.ngrok.app/user_signup', json = info)

@app.route('/update', methods=['POST'])
def demo():
    data = request.get_json(force=True)

    print(data)

    # Post URL: https://wms.shipitdone.com/version-3tar/api/1.1/wf/capstone_ship_print/

    if data["status"] == "open":
        docPrinters = ["Rollo"]
        labelPrinters = [ "Rollo"]
        addDocs = data["addDocs"]
        boxSizes = data["boxSizes"]

        boxSizesList = []

        for i in range(len(boxSizes)):
            boxSizesList.append(boxSizes[i]["name"])

        print("Number of Boxes: ", len(boxSizesList))

        page_setup(boxSizes=boxSizesList, docPrinters=docPrinters, labelPrinters=labelPrinters, addDocs=["Receipts"], data=data)

        unidle_screen()

    elif data["status"] == "closed":
        idle_screen()   

    return jsonify({"status": "success"})

if __name__ == "__main__":
    elgato_thread = threading.Thread(target=setup)
    elgato_thread.daemon = True
    elgato_thread.start()
    send_user_ip()
    app.run(host='0.0.0.0', port=5005)