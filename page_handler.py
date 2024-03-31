from SingletonDeckState import SingletonDeckState   
from pre_image_processing import black_square

deck_state = SingletonDeckState()

def idle_screen():
    '''
    Function to display the idle screen on the StreamDeck.
    '''
    deck_state.process_input = False
    display_page(True)
    
def unidle_screen():
    '''
    Function to unidle the display of the StreamDeck.
    '''
    deck_state.current_page = 0
    deck_state.current_box_row = 0
    deck_state.current_picklist_row = 0
    deck_state.current_shipping_row = 0
    deck_state.process_input = True
    # display_page()

def page_box_update():
    for i in range(3):
        deck_state.pages[0][i+5] = deck_state.box_row[deck_state.current_box_row][i]
        deck_state.red_pages[0][i+5] = deck_state.red_box_row[deck_state.current_box_row][i]

def page_picklist_update():
    for i in range(3):
        deck_state.pages[0][i] = deck_state.picklist_row[deck_state.current_picklist_row][i]
        deck_state.red_pages[0][i] = deck_state.red_picklist_row[deck_state.current_picklist_row][i]

def page_shipping_update():
    for i in range(3):
        deck_state.pages[0][i+10] = deck_state.shipping_row[deck_state.current_shipping_row][i]
        deck_state.red_pages[0][i+10] = deck_state.red_shipping_row[deck_state.current_shipping_row][i]

def display_page(idle=False):
    '''
    Function to display a page on the StreamDeck.
    '''
    if idle:
        for i in range(15):
            deck_state.deck.set_key_image(i, deck_state.idle_pages[i])
        return

    for i in range(15):
        if deck_state.pages[deck_state.current_page][i] == None:
            deck_state.deck.set_key_image(i, black_square)
        else:
            deck_state.deck.set_key_image(i, deck_state.pages[deck_state.current_page][i])

def reset_rows():
    '''
    Function to reset the current row of the StreamDeck.
    '''
    deck_state.current_box_row = 0
    deck_state.current_picklist_row = 0
    deck_state.current_shipping_row = 0

def next_page():
    '''
    Function to move to the next page on the StreamDeck.
    '''
    deck_state.current_page = (deck_state.current_page + 1) % len(deck_state.pages)
    reset_rows()
    display_page()

def prev_page():
    '''
    Function to move to the previous page on the StreamDeck.
    '''
    deck_state.current_page = (deck_state.current_page - 1) % len(deck_state.pages)
    reset_rows()
    display_page()

def display_box_row():
    for i in range(4):
        deck_state.deck.set_key_image(i+5, deck_state.pages[deck_state.current_page][i+5])

def display_picklist_row():
    for i in range(3):
        deck_state.deck.set_key_image(i, deck_state.pages[deck_state.current_page][i])

def display_shipping_row():
    for i in range(3):
        deck_state.deck.set_key_image(i+10, deck_state.pages[deck_state.current_page][i+10])