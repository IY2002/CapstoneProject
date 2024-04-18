from StreamDeck.DeviceManager import DeviceManager

def connect_to_elgato():
    '''
    Function to connect to the Elgato StreamDeck.
    '''
    # connect to streamdeck
    streamdecks = DeviceManager().enumerate()
    if not streamdecks:
        # throw an error if streamdeck is not found
        raise LookupError("No Stream Decks were found")
    
    return streamdecks[0]