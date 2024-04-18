from SingletonDeckState import SingletonDeckState   
from pre_image_processing import black_square

# Create an instance of SingletonDeckState
deck_state = SingletonDeckState()

# Define a function to display the idle screen on the StreamDeck
def idle_screen():
    '''
    Function to display the idle screen on the StreamDeck.
    '''
    deck_state.process_input = False
    deck_state.docs_ready = False
    display_page(True)
    
# Define a function to unidle the display of the StreamDeck
def unidle_screen():
    '''
    Function to unidle the display of the StreamDeck.
    '''
    deck_state.current_page = 0
    deck_state.current_box_row = 0
    deck_state.current_shipping_row = 0
    deck_state.process_input = True

# Define a function to display the calculator page on the StreamDeck
def show_calc_page():
    '''
    Function to display the calculator page on the StreamDeck.
    '''
    deck_state.current_page = -1
    deck_state.calc_input = ""
    display_page()

# Define a function to hide the calculator page on the StreamDeck
def hide_calc_page():
    '''
    Function to hide the calculator page on the StreamDeck.
    '''
    deck_state.current_page = 0
    display_page()

# Define a function to update the box row on the StreamDeck
def page_box_update():
    '''
    Function to update the box row on the StreamDeck.
    '''
    for i in range(3):
        deck_state.pages[0][i] = deck_state.box_row[deck_state.current_box_row][i]
        deck_state.red_pages[0][i] = deck_state.red_box_row[deck_state.current_box_row][i]

# Define a function to update the shipping row on the StreamDeck
def page_shipping_update():
    '''
    Function to update the shipping row on the StreamDeck.
    '''
    for i in range(3):
        deck_state.pages[0][i+5] = deck_state.shipping_row[deck_state.current_shipping_row][i]
        deck_state.red_pages[0][i+5] = deck_state.red_shipping_row[deck_state.current_shipping_row][i]

# Define a function to update the document row on the StreamDeck
def page_doc_update(key):
    '''
    Function to update the document row on the StreamDeck based on the given key.
    '''
    if key == 3:
        # Update the first key in the document row
        for i in range(3):
            if len(deck_state.doc_pages[deck_state.current_page - 1]) >= 1:
                # If there is a document available for the current page and row, update the key image
                deck_state.pages[deck_state.current_page][i] = deck_state.doc_pages[deck_state.current_page - 1][0][deck_state.doc_current_rows[deck_state.current_page - 1][0]][i]
                deck_state.red_pages[deck_state.current_page][i] = deck_state.doc_red_pages[deck_state.current_page - 1][0][deck_state.doc_current_rows[deck_state.current_page - 1][0]][i]
            else:
                # If there is no document available, display a black square
                deck_state.pages[deck_state.current_page][i] = black_square
                deck_state.red_pages[deck_state.current_page][i] = black_square

    elif key == 8:
        # Update the second key in the document row
        for i in range(3):
            if len(deck_state.doc_pages[deck_state.current_page - 1]) >= 2:
                # If there is a document available for the current page and row, update the key image
                deck_state.pages[deck_state.current_page][i+5] = deck_state.doc_pages[deck_state.current_page - 1][1][deck_state.doc_current_rows[deck_state.current_page - 1][1]][i]
                deck_state.red_pages[deck_state.current_page][i+5] = deck_state.doc_red_pages[deck_state.current_page - 1][1][deck_state.doc_current_rows[deck_state.current_page - 1][1]][i]
            else:
                # If there is no document available, display a black square
                deck_state.pages[deck_state.current_page][i+5] = black_square
                deck_state.red_pages[deck_state.current_page][i+5] = black_square
    
    elif key == 13:
        # Update the third key in the document row
        for i in range(3):
            if len(deck_state.doc_pages[deck_state.current_page - 1]) >= 3:
                # If there is a document available for the current page and row, update the key image
                deck_state.pages[deck_state.current_page][i+10] = deck_state.doc_pages[deck_state.current_page - 1][2][deck_state.doc_current_rows[deck_state.current_page - 1][2]][i]
                deck_state.red_pages[deck_state.current_page][i+10] = deck_state.doc_red_pages[deck_state.current_page - 1][2][deck_state.doc_current_rows[deck_state.current_page - 1][2]][i]
            else:
                # If there is no document available, display a black square
                deck_state.pages[deck_state.current_page][i+10] = black_square
                deck_state.red_pages[deck_state.current_page][i+10] = black_square

def display_page(idle=False):
    '''
    Function to display a page on the StreamDeck.
    '''
    if deck_state.current_page == -1:
        # Display the calculator page
        for i in range(15):
            deck_state.deck.set_key_image(i, deck_state.calc_pages[i])
        return
    if idle:
        # Display the idle screen
        for i in range(15):
            deck_state.deck.set_key_image(i, deck_state.idle_pages[i])
        return

    # Display the current page
    for i in range(15):
        if deck_state.pages[deck_state.current_page][i] == None:
            # If the key image is None, display a black square
            deck_state.deck.set_key_image(i, black_square)
        else:
            # Display the key image for the current page and key
            deck_state.deck.set_key_image(i, deck_state.pages[deck_state.current_page][i])

def reset_rows():
    '''
    Function to reset the current row of the StreamDeck.
    '''
    if deck_state.current_page == 0:
        # Reset the box and shipping rows
        deck_state.current_box_row = 0
        deck_state.current_shipping_row = 0

        page_box_update()
        page_shipping_update()

    else:
        # Reset the document rows
        deck_state.doc_current_rows[deck_state.current_page - 1] = [0, 0, 0]

        page_doc_update(3)
        page_doc_update(8)
        page_doc_update(13)

# Define a function to move to the next page on the StreamDeck
def next_page():
    '''
    Function to move to the next page on the StreamDeck.
    '''
    if deck_state.docs_ready:
        deck_state.current_page = (deck_state.current_page + 1) % len(deck_state.pages)
        reset_rows()
        display_page()

# Define a function to move to the previous page on the StreamDeck
def prev_page():
    '''
    Function to move to the previous page on the StreamDeck.
    '''
    if deck_state.docs_ready:
        deck_state.current_page = (deck_state.current_page - 1) % len(deck_state.pages)
        reset_rows()
        display_page()

# Define a function to display the box row on the StreamDeck
def display_box_row():
    '''
    Function to display the box row on the StreamDeck.
    '''
    for i in range(4):
        deck_state.deck.set_key_image(i+5, deck_state.pages[deck_state.current_page][i])

# Define a function to display the shipping row on the StreamDeck
def display_shipping_row():
    '''
    Function to display the shipping row on the StreamDeck.
    '''
    for i in range(3):
        deck_state.deck.set_key_image(i+10, deck_state.pages[deck_state.current_page][i+5])

# Define a function to display the document row on the StreamDeck
def display_doc_row(key):
    '''
    Function to display the document row on the StreamDeck based on the given key.
    '''
    if key == 3:
        for i in range(3):
            deck_state.deck.set_key_image(i, deck_state.pages[deck_state.current_page][i])
    
    elif key == 8:
        for i in range(3):
            deck_state.deck.set_key_image(i+5, deck_state.pages[deck_state.current_page][i+5])
    
    elif key == 13:
        for i in range(3):
            deck_state.deck.set_key_image(i+10, deck_state.pages[deck_state.current_page][i+10])
