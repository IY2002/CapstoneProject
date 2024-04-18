from SingletonDeckState import SingletonDeckState
from page_handler import next_page, prev_page, page_box_update, page_shipping_update, display_box_row, display_shipping_row, display_doc_row, page_doc_update, show_calc_page, hide_calc_page
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
    # Check if the current page is the calculator page
    if deck_state.current_page == -1:
        # Flash the button on the calculator page
        for _ in range(3):
            time.sleep(0.1)
            deck_state.deck.set_key_image(key, deck_state.calc_pages[key])
            time.sleep(0.1)
            deck_state.deck.set_key_image(key, deck_state.calc_red_pages[key])

        deck_state.deck.set_key_image(key, deck_state.calc_pages[key])
    else:
        # Flash the button on other pages
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
    # Handle numeric keys 1-9
    if key >= 0 and key <= 2:
        deck_state.calc_input += str(key + 1)
    elif key >= 5 and key <= 7:
        deck_state.calc_input += str(key - 1)
    elif key >= 10 and key <= 12:
        deck_state.calc_input += str(key - 3)
    # Handle decimal point key
    elif key == 8:
        # Check if decimal point already exists in the input
        if deck_state.calc_input.find(".") != -1:
            flash_button(key)
            deck_state.process_input = True
            return
        deck_state.calc_input += "."
    # Handle backspace key
    elif key == 9:
        deck_state.calc_input = deck_state.calc_input[:-1]
    # Handle zero key
    elif key == 13:
        deck_state.calc_input += "0"
    # Handle equals key
    elif key == 14: 
        deck_state.current_page = 0
        print("Calculation: ", deck_state.calc_input)
        
        # Send the box post request with the calculated weight
        response = send_box_post_request(float(deck_state.calc_input))
        print("Response: ", response["response"]["url"])

        # Set the label URL
        deck_state.label_url = response["response"]["url"]

        hide_calc_page()
        
        deck_state.process_input = True
        return
    else:
        return

    # Update the calculator display on the StreamDeck
    update_calc_display()

    # Set the key image on the StreamDeck to indicate the pressed key
    deck_state.deck.set_key_image(key, deck_state.calc_pages[key])
    deck_state.process_input = True

def function_caller(key):
    # If the current page is greater than 0, handle document key presses
    if deck_state.current_page > 0:
        # Get the corresponding document text based on the key press
        doc_text = deck_state.doc_text_pages[deck_state.current_page - 1][key//5][deck_state.doc_current_rows[deck_state.current_page - 1][key//5]][key%5]    
       
        # Send a POST request to print the document
        requests.post(deck_state.laptop_ip.strip() + "/print_doc", json={"printer": doc_text[1], "doc_num": key//5})
        time.sleep(5)
        
        # Print the document text
        print(doc_text[0], doc_text[1])

    # If the key press is in the range 0-2, handle box key presses
    elif key >= 0 and key < 3:
        # Print the chosen box
        print("Box", deck_state.box_row_text[deck_state.current_box_row][key] )
        global box_chosen
        box_chosen = deck_state.box_row_text[deck_state.current_box_row][key ]
        show_calc_page()
        deck_state.process_input = True
        return

    # If the key press is in the range 5-7, handle shipping key presses
    elif key >= 5 and key < 8:
        # Check if label is ready or laptop IP is empty, if not, flash the button
        if deck_state.label_ready == False or deck_state.laptop_ip == "":
            flash_button(key)
        else:
            # Send a POST request to print the label
            print(deck_state.laptop_ip.strip() + "/print_label")
            requests.post(deck_state.laptop_ip.strip() + "/print_label", json={"url": deck_state.label_url, "printer": deck_state.shipping_row_text[deck_state.current_shipping_row][key - 5]})
            time.sleep(4)

        # Print the chosen shipping option
        print("Shipping", deck_state.shipping_row_text[deck_state.current_shipping_row][key - 5])

    # Set the key image on the StreamDeck and set process_input back to True
    deck_state.deck.set_key_image(key, deck_state.pages[deck_state.current_page][key])
    deck_state.process_input = True

def next_box_row():
    # Increment the current box row and update the page and display
    deck_state.current_box_row = (deck_state.current_box_row + 1) % (len(deck_state.box_row))
    page_box_update()
    display_box_row()

def next_shipping_row():
    # Increment the current shipping row and update the page and display
    deck_state.current_shipping_row = (deck_state.current_shipping_row + 1) % (len(deck_state.shipping_row))
    page_shipping_update()
    display_shipping_row()

def next_doc_row(key):
    # Increment the current document row based on the key press and update the page and display
    if key == 3:
        deck_state.doc_current_rows[deck_state.current_page - 1][0] = (deck_state.doc_current_rows[deck_state.current_page - 1][0] + 1) % deck_state.doc_num_rows[deck_state.current_page - 1][0]
    elif key == 8:
        deck_state.doc_current_rows[deck_state.current_page - 1][1] = (deck_state.doc_current_rows[deck_state.current_page - 1][1] + 1) % deck_state.doc_num_rows[deck_state.current_page - 1][1]
    elif key == 13:
        deck_state.doc_current_rows[deck_state.current_page - 1][2] = (deck_state.doc_current_rows[deck_state.current_page - 1][2] + 1) % deck_state.doc_num_rows[deck_state.current_page - 1][2]
    
    page_doc_update(key)
    display_doc_row(key)

def key_helper(key):
    # Print the key press and current page
    print(f'Key {key} pressed, current page: {deck_state.current_page}')

    # If the key press is None and the current page is not -1, return
    if deck_state.pages[deck_state.current_page][key] == None and deck_state.current_page != -1:
        return
    
    # If the current page is -1 and the key press is 4 or 3, return
    elif deck_state.current_page == -1 and (key == 4 or key == 3):
        return

    # If the current page is -1, set the key image to red and start a thread to handle the key press
    elif deck_state.current_page == -1:
        deck_state.deck.set_key_image(key, deck_state.calc_red_pages[key])
        deck_state.process_input = False

        threading.Thread(target=calc_key_handler, args=(key,)).start()
        return
    
    # If the current page is 0 and the key press is 3, go to the next box row
    elif deck_state.current_page == 0 and key == 3:
        next_box_row()

    # If the current page is 0 and the key press is 8, go to the next shipping row
    elif deck_state.current_page == 0 and key == 8:
        next_shipping_row()

    # If the key press is 3, 8, or 13 and the current page is greater than 0, go to the next document row
    elif (key == 3 or key == 8 or key == 13) and deck_state.current_page > 0:
        next_doc_row(key)

    else:        
        # Set the key image to red and start a thread to handle the key press
        deck_state.deck.set_key_image(key, deck_state.red_pages[deck_state.current_page][key])
        deck_state.process_input = False
        
        threading.Thread(target=function_caller, args=(key,)).start()
    return
