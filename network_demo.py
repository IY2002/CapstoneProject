from demo2 import setup
from page_handler import idle_screen, unidle_screen, display_page
from pre_image_processing import page_setup
import flask 
from flask import request, jsonify
import threading
import time

app = flask.Flask(__name__)

@app.route('/demo', methods=['POST'])
def demo():
    real_start = time.time()
    start_time = time.time()
    data = request.json

    if data["status"] == "open":
        docPrinters = data["docPrinters"]
        labelPrinters = data["labelPrinters"]
        addDocs = data["addDocs"]
        boxSizes = data["boxSizes"]

        page_setup(boxSizes=boxSizes, docPrinters=docPrinters, labelPrinters=labelPrinters, addDocs=addDocs)
        print("time to setup: ", time.time() - start_time)

        start_time = time.time()
        unidle_screen()
        print("time to unidle: ", time.time() - start_time)


    elif data["status"] == "closed":
        idle_screen()   

    print("Time taken: ", time.time() - real_start)

    return jsonify({"status": "success"})

if __name__ == "__main__":
    elgato_thread = threading.Thread(target=setup)
    elgato_thread.daemon = True
    elgato_thread.start()
    app.run(host='0.0.0.0', port=5005)

