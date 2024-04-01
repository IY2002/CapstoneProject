from SingletonDeckState import SingletonDeckState
from page_handler import next_page, prev_page, page_box_update, page_picklist_update, page_shipping_update, display_box_row, display_picklist_row, display_shipping_row, display_doc_row, page_doc_update
import time, threading

deck_state = SingletonDeckState()

def key_change_callback(deck, key, state):
    '''
    Function to handle key presses on the StreamDeck.
    '''
    if state and deck_state.process_input:
        if key == 4:
            next_page()
        elif key == 9:
            prev_page()
        elif key == 14:
            return
        else:
            key_helper(key)

def time_waiting(key):
    # Simulate a long-running task with a loop
    time.sleep(1.5)
    
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
    if deck_state.pages[deck_state.current_page][key] == None:
        return
    
    elif deck_state.current_page == 0 and key == 3:
        next_picklist_row()

    elif deck_state.current_page == 0 and key == 8:
        next_box_row()

    elif deck_state.current_page == 0 and key == 13:
        next_shipping_row()

    elif key == 3 or key == 8 or key == 13:
        next_doc_row(key)

    else:
        deck_state.deck.set_key_image(key, deck_state.red_pages[deck_state.current_page][key])
        deck_state.process_input = False
        
        threading.Thread(target=time_waiting, args=(key,)).start()
    return
