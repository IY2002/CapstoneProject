from SingletonDeckState import SingletonDeckState
from pre_image_processing import image_setup, page_setup
from input_processing import display_page, key_change_callback
from page_handler import idle_screen, unidle_screen

deck_state = SingletonDeckState()

def setup():
    '''
    Function to setup the StreamDeck.
    '''
    image_setup()
    page_setup(numLabelPrinters=4, numDocPrinters=4, numAddDocs=3)
    deck_state.deck.open()
    deck_state.deck.set_brightness(100)
    deck_state.deck.set_key_callback(key_change_callback)
    idle_screen()
    
    try:
        while True:
            pass
    except KeyboardInterrupt:
        deck_state.deck.close()

if __name__ == "__main__":
    setup()