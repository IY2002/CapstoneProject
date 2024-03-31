from SingletonDeckState import SingletonDeckState
from pre_image_processing import image_setup, page_setup, setup_idle_screen
from input_processing import key_change_callback
from page_handler import idle_screen

deck_state = SingletonDeckState()

def setup():
    '''
    Function to setup the StreamDeck.
    '''
    image_setup()
    setup_idle_screen()
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