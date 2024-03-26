from deck_setup import connect_to_elgato
class SingletonDeckState:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SingletonDeckState, cls).__new__(cls)
            # Initialize your variables here
            cls._instance.current_page = 0
            cls._instance.current_row = 0
            cls._instance.process_input = True
            cls._instance.deck = connect_to_elgato()
            cls._instance.box_row = []
            cls._instance.red_box_row = []
        return cls._instance
