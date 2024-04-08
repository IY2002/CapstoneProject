from deck_setup import connect_to_elgato
class SingletonDeckState:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SingletonDeckState, cls).__new__(cls)
            cls._initialize(cls._instance)
        return cls._instance

    @classmethod
    def _initialize(cls, instance):
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


    # def __new__(cls):
    #     if cls._instance is None:
    #         cls._instance = super(SingletonDeckState, cls).__new__(cls)
    #         cls._instance.current_page = 0
    #         cls._instance.current_box_row = 0
    #         cls._instance.current_picklist_row = 0
    #         cls._instance.current_shipping_row = 0
    #         cls._instance.process_input = True
    #         cls._instance.deck = connect_to_elgato()
    #         cls._instance.box_row = []
    #         cls._instance.red_box_row = []
    #         cls._instance.pages = []
    #         cls._instance.red_pages = []
    #         cls._instance.idle_pages = [None for i in range(15)]
    #         cls._instance.picklist_row = []
    #         cls._instance.red_picklist_row = []
    #         cls._instance.shipping_row = []
    #         cls._instance.red_shipping_row = []
    #         cls._instance.doc_pages = []
    #         cls._instance.doc_red_pages = []
    #         cls._instance.doc_text_pages = []
    #         cls._instance.doc_num_rows = []
    #         cls._instance.doc_current_rows = []
    #         cls._instance.docs_ready = False
    #         cls._instance.box_row_text = []
    #         cls._instance.picklist_row_text = []
    #         cls._instance.shipping_row_text = []
    #         cls._instance.next_image = None
    #         cls._instance.prev_image = None
    #         cls._instance.full_logo = None
    #         cls._instance.page_next = None
            
    #     return cls._instance
