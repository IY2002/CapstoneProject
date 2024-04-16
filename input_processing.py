from SingletonDeckState import SingletonDeckState
from page_handler import next_page, prev_page, page_box_update, page_picklist_update, page_shipping_update, display_box_row, display_picklist_row, display_shipping_row, display_doc_row, page_doc_update, show_calc_page, hide_calc_page
import time, threading
from pre_image_processing import format_image, create_text_overlay
import requests
deck_state = SingletonDeckState()

box_url = "https://wms.shipitdone.com/version-3tar/api/1.1/wf/capstone_ship_print/"

box_chosen = ""

printready = False

labelready = False
def key_change_callback(deck, key, state):
    '''
    Function to handle key presses on the StreamDeck.
    '''
    if state and deck_state.process_input:
        if key == 4 and deck_state.current_page != -1:
            next_page()
        elif key == 9 and deck_state.current_page != -1:
            prev_page()
        elif key == 14 and deck_state.current_page != -1:
            return
        else:
            key_helper(key)

def send_box_post_request(weight):
    """
    Send a POST request to the specified URL
    """
    # Define the payload for the POST request
    box_id = ""
    for box in deck_state.data['boxSizes']:
        if box['name'] == box_chosen:
            box_id = box['uniqueID']
            break
    payload = {
        'OrderUniqueId': deck_state.data['OrderUniqueID'],
        'BoxUniqueID': box_id,
        'Weight': weight
    }
    
    # Send the POST request
    response = requests.post(box_url, json=payload)
    # #need to save file, it gives us the URL.
    # #Rename the file to a consistent name
    # #save the location of the file, set flag stating label is ready
    # filepath = "/dummy/label.pdf"
    # file = wget(box_url, out = filepath)
    # labelready = True


    # #print the label

    # #after printing, reset the print button flag
    # printready = False
    # #delete the file
    # os.remove('/dummy/label.pdf')
    # #reset the label ready flag
    # labelready = False

    deck_state.label_ready = True

    return response.json()

def update_calc_display():
    '''
    Function to update the calculator display on the StreamDeck.
    '''
    cur_number_image = format_image(create_text_overlay('./images/black_square.png', deck_state.calc_input + " lbs", font_path='OpenSans-ExtraBold.ttf', font_color='#60acf7', font_y_offset=6, font_size=24))
    deck_state.deck.set_key_image(4, cur_number_image)

def flash_button(key):
    '''
    Function to flash a button on the calculator page.
    '''
    if deck_state.current_page == -1:
        for _ in range(3):
            time.sleep(0.1)
            deck_state.deck.set_key_image(key, deck_state.calc_pages[key])
            time.sleep(0.1)
            deck_state.deck.set_key_image(key, deck_state.calc_red_pages[key])

        deck_state.deck.set_key_image(key, deck_state.calc_pages[key])
    else:
        for _ in range(3):
            time.sleep(0.1)
            deck_state.deck.set_key_image(key, deck_state.pages[deck_state.current_page][key])
            time.sleep(0.1)
            deck_state.deck.set_key_image(key, deck_state.red_pages[deck_state.current_page][key])

        deck_state.deck.set_key_image(key, deck_state.pages[deck_state.current_page][key])


def calc_key_handler(key):
    '''
    Function to handle key presses on the calculator page.
    '''
    if key >= 0 and key <= 2:
        deck_state.calc_input += str(key + 1)
    elif key >= 5 and key <= 7:
        deck_state.calc_input += str(key - 1)
    elif key >= 10 and key <= 12:
        deck_state.calc_input += str(key - 3)
    elif key == 8:
        if deck_state.calc_input.find(".") != -1:
            flash_button(key)
            deck_state.process_input = True
            return
        deck_state.calc_input += "."
    elif key == 9:
        deck_state.calc_input = deck_state.calc_input[:-1]
    elif key == 13:
        deck_state.calc_input += "0"
    elif key == 14: 
        deck_state.current_page = 0
        print("Calculation: ", deck_state.calc_input)
        
        response = send_box_post_request(float(deck_state.calc_input))
        print("Response: ", response["response"]["url"])

        hide_calc_page()
        
        deck_state.process_input = True
        return
    else:
        return

    update_calc_display()

    deck_state.deck.set_key_image(key, deck_state.calc_pages[key])
    deck_state.process_input = True

def function_caller(key):
    if deck_state.current_page > 0:
        doc_text = deck_state.doc_text_pages[deck_state.current_page - 1][key//5][deck_state.doc_current_rows[deck_state.current_page - 1][key//5]][key%5]
        
        if deck_state.laptop_ip != "":
                requests.post(deck_state.laptop_ip + ":5005/print_doc")
        else:
            flash_button(key)
        
        print(doc_text[0], doc_text[1])

    # elif key < 3:
    #     print("Picklist", deck_state.picklist_row_text[deck_state.current_picklist_row][key])

    elif key >= 0 and key < 3:
        print("Box", deck_state.box_row_text[deck_state.current_box_row][key] )
        global box_chosen
        box_chosen = deck_state.box_row_text[deck_state.current_box_row][key ]
        show_calc_page()
        deck_state.process_input = True
        return

    elif key >= 5 and key < 8:
        if deck_state.label_ready == False:
            flash_button(key)
        else:
            if deck_state.laptop_ip != "":
                requests.post(deck_state.laptop_ip + ":5005/print_label")
            else:
                flash_button(key)

        print("Shipping", deck_state.shipping_row_text[deck_state.current_shipping_row][key - 5])


    # Simulate a long-running task with a loop
    # time.sleep(1.5)
    
    # Once the task is done, set process_input back to True
    deck_state.deck.set_key_image(key, deck_state.pages[deck_state.current_page][key])
    deck_state.process_input = True

def next_box_row():
    deck_state.current_box_row = (deck_state.current_box_row + 1) % (len(deck_state.box_row))
    page_box_update()
    display_box_row()

def next_picklist_row():
    deck_state.current_picklist_row = (deck_state.current_picklist_row + 1) % (len(deck_state.picklist_row))
    page_picklist_update()
    display_picklist_row()

def next_shipping_row():
    deck_state.current_shipping_row = (deck_state.current_shipping_row + 1) % (len(deck_state.shipping_row))
    page_shipping_update()
    display_shipping_row()

def next_doc_row(key):
    if key == 3:
        deck_state.doc_current_rows[deck_state.current_page - 1][0] = (deck_state.doc_current_rows[deck_state.current_page - 1][0] + 1) % deck_state.doc_num_rows[deck_state.current_page - 1][0]
    elif key == 8:
        deck_state.doc_current_rows[deck_state.current_page - 1][1] = (deck_state.doc_current_rows[deck_state.current_page - 1][1] + 1) % deck_state.doc_num_rows[deck_state.current_page - 1][1]
    elif key == 13:
        deck_state.doc_current_rows[deck_state.current_page - 1][2] = (deck_state.doc_current_rows[deck_state.current_page - 1][2] + 1) % deck_state.doc_num_rows[deck_state.current_page - 1][2]
    
    page_doc_update(key)
    display_doc_row(key)

def key_helper(key):
    print(f'Key {key} pressed, current page: {deck_state.current_page}')
    if deck_state.pages[deck_state.current_page][key] == None and deck_state.current_page != -1:
        return
    
    elif deck_state.current_page == -1 and (key == 4 or key == 3):
        return

    elif deck_state.current_page == -1:
        deck_state.deck.set_key_image(key, deck_state.calc_red_pages[key])
        deck_state.process_input = False

        threading.Thread(target=calc_key_handler, args=(key,)).start()
        return
    
    elif deck_state.current_page == 0 and key == 3:
        next_picklist_row()

    elif deck_state.current_page == 0 and key == 8:
        next_box_row()

    elif deck_state.current_page == 0 and key == 13:
        next_shipping_row()

    elif (key == 3 or key == 8 or key == 13) and deck_state.current_page > 0:
        next_doc_row(key)

    else:        
        deck_state.deck.set_key_image(key, deck_state.red_pages[deck_state.current_page][key])
        deck_state.process_input = False
        
        threading.Thread(target=function_caller, args=(key,)).start()
    return
