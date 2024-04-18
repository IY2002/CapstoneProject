from SingletonDeckState import SingletonDeckState
from pre_image_processing import image_setup, calculator_images_setup
from page_setup import setup_idle_screen
from input_processing import key_change_callback
from page_handler import idle_screen

deck_state = SingletonDeckState()

def setup():
    '''
    Function to setup the StreamDeck.
    '''
    # Call the necessary setup functions
    image_setup()  # Setup images
    calculator_images_setup()  # Setup calculator images
    setup_idle_screen()  # Setup idle screen
    
    # Open the StreamDeck device
    deck_state.deck.open()
    
    # Set the brightness of the StreamDeck to 100
    deck_state.deck.set_brightness(100)
    
    # Set the key callback function to handle key changes
    deck_state.deck.set_key_callback(key_change_callback)
    
    # Display the idle screen on the StreamDeck
    idle_screen()
    
    try:
        while True:
            pass
    except KeyboardInterrupt:
        # Close the StreamDeck device when the program is interrupted
        deck_state.deck.close()

if __name__ == "__main__":
    setup()