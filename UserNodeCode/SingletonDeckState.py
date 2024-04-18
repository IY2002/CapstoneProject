from deck_setup import connect_to_elgato

class SingletonDeckState:
    _instance = None  # Private class variable to hold the singleton instance

    def __new__(cls):
        if cls._instance is None:  # Check if the singleton instance has been created
            cls._instance = super(SingletonDeckState, cls).__new__(cls)  # Create the singleton instance
            cls._initialize(cls._instance)  # Initialize the instance
        return cls._instance  # Return the singleton instance

    @classmethod
    def _initialize(cls, instance):
        # Initialize instance variables
        instance.current_page = 0
        instance.current_box_row = 0
        instance.current_picklist_row = 0
        instance.current_shipping_row = 0
        instance.process_input = True
        instance.deck = connect_to_elgato()
        instance.box_row = []
        instance.red_box_row = []
        instance.pages = []
        instance.red_pages = []
        instance.idle_pages = [None for i in range(15)]
        instance.picklist_row = []
        instance.red_picklist_row = []
        instance.shipping_row = []
        instance.red_shipping_row = []
        instance.doc_pages = []
        instance.doc_red_pages = []
        instance.doc_text_pages = []
        instance.doc_num_rows = []
        instance.doc_current_rows = []
        instance.docs_ready = False
        instance.box_row_text = []
        instance.picklist_row_text = []
        instance.shipping_row_text = []
        instance.next_image = None
        instance.prev_image = None
        instance.full_logo = None
        instance.page_next = None
        instance.calc_pages = [None for _ in range(15)]
        instance.calc_red_pages = [None for _ in range(15)]
        instance.calc_input = ""
        instance.data = None
        instance.label_ready = False
        instance.laptop_ip = ""
        instance.laptop_id = ""
        instance.label_url = ""
