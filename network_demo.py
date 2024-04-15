import requests
from demo2 import setup
from page_handler import idle_screen, unidle_screen
from page_setup import page_setup
import flask 
from flask import request, jsonify
import threading

app = flask.Flask(__name__)

@app.route('/demo', methods=['POST'])
def demo():
    data = request.get_json(force=True)

    print(data)

    # Post URL: https://wms.shipitdone.com/version-3tar/api/1.1/wf/capstone_ship_print/

    if data["status"] == "open":
        docPrinters = ["Epson", "Rollo"]
        labelPrinters = ["Epson", "Rollo"]
        addDocs = data["addDocs"]
        boxSizes = data["boxSizes"]

        boxSizesList = []

        for i in range(len(boxSizes)):
            boxSizesList.append(boxSizes[i]["name"])

        print("Number of Boxes: ", len(boxSizesList))

        page_setup(boxSizes=boxSizesList, docPrinters=docPrinters, labelPrinters=labelPrinters, addDocs=addDocs, data=data)

        unidle_screen()

    elif data["status"] == "closed":
        idle_screen()   

    return jsonify({"status": "success"})

if __name__ == "__main__":
    elgato_thread = threading.Thread(target=setup)
    elgato_thread.daemon = True
    elgato_thread.start()
    app.run(host='0.0.0.0', port=5005)