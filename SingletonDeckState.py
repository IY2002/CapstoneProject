from deck_setup import connect_to_elgato
class SingletonDeckState:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SingletonDeckState, cls).__new__(cls)
            cls._instance.current_page = 0
            cls._instance.current_box_row = 0
            cls._instance.current_picklist_row = 0
            cls._instance.current_shipping_row = 0
            cls._instance.process_input = True
            cls._instance.deck = connect_to_elgato()
            cls._instance.box_row = []
            cls._instance.red_box_row = []
            cls._instance.pages = []
            cls._instance.red_pages = []
            cls._instance.idle_pages = [None for i in range(15)]
            cls._instance.picklist_row = []
            cls._instance.red_picklist_row = []
            cls._instance.shipping_row = []
            cls._instance.red_shipping_row = []
            cls._instance.doc_pages = []
            cls._instance.doc_red_pages = []
            cls._instance.doc_text_pages = []
            cls._instance.doc_num_rows = []
            cls._instance.doc_current_rows = []
            cls._instance.docs_ready = False
            
        return cls._instance
