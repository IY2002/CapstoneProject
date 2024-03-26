from pre_image_processing import pages, red_pages
from SingletonDeckState import SingletonDeckState   
from pre_image_processing import prep_image, format_image, create_text_overlay, apply_red_hue
deck_state = SingletonDeckState()

def idle_screen():
    '''
    Function to display the idle screen on the StreamDeck.
    '''
    deck_state.current_page = 2
    # deck_state.process_input = False
    display_page()

def unidle_screen():
    '''
    Function to unidle the display of the StreamDeck.
    '''
    deck_state.current_page = 0
    deck_state.current_row = 0
    # deck_state.process_input = True
    display_page()

def page_update():
    global pages
    global red_pages

    for i in range(3):
        pages[0][i+5] = deck_state.box_row[deck_state.current_row][i]
        red_pages[0][i+5] = deck_state.red_box_row[deck_state.current_row][i]

def display_page():
    '''
    Function to display a page on the StreamDeck.
    '''
    if deck_state.current_page == 0:
        page_update()

    for i in range(15):
        deck_state.deck.set_key_image(i, pages[deck_state.current_page][i])

def next_page():
    '''
    Function to move to the next page on the StreamDeck.
    '''
    deck_state.current_page = (deck_state.current_page + 1) % 2
    display_page()

def prev_page():
    '''
    Function to move to the previous page on the StreamDeck.
    '''
    deck_state.current_page = (deck_state.current_page - 1) % 2
    display_page()

def display_row():
    for i in range(4):
        deck_state.deck.set_key_image(i+5, pages[deck_state.current_page][i+5])
