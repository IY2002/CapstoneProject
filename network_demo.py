from demo2 import setup
from page_handler import idle_screen, unidle_screen, display_page
from pre_image_processing import page_setup
import flask 
from flask import request, jsonify
import threading

app = flask.Flask(__name__)

@app.route('/demo', methods=['POST'])
def demo():
    data = request.json

    numDocPrinters = data["numDocPrinters"]
    numLabelPrinters = data["numLabelPrinters"]
    numAddDocs = data["numAddDocs"]
    boxSizes = data["boxSizes"]

    if data["status"] == "open":
        page_setup(numLabelPrinters=numLabelPrinters, numDocPrinters=numDocPrinters, numAddDocs=numAddDocs, boxSizes=boxSizes)
        display_page()
        unidle_screen()

    elif data["status"] == "closed":
        idle_screen()

    return jsonify({"status": "success"})

if __name__ == "__main__":
    elgato_thread = threading.Thread(target=setup)
    elgato_thread.daemon = True
    elgato_thread.start()
    app.run(host='0.0.0.0', port=5005)

