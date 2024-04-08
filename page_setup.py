from pre_image_processing import black_square, format_image, create_text_overlay, apply_red_hue, prep_image
from SingletonDeckState import SingletonDeckState
from concurrent.futures import ThreadPoolExecutor
import threading
import time

deck_state = SingletonDeckState()

def setup_idle_screen():
    '''
    Function to setup the idle screen for the StreamDeck.
    '''
    for j in range(15):
        if j <= 8:
            deck_state.idle_pages[j] = format_image(prep_image('./cut_logo/image_part_00' + str(j+1) + '.jpg'))
        else:
            deck_state.idle_pages[j] = format_image(prep_image('./cut_logo/image_part_0' + str(j+1) + '.jpg'))

def first_page_setup(labelPrinters, boxSizes):
    '''
    Function to setup the first page for the StreamDeck.
    '''

    for j in range(15):
        if j >= 0 and j < 3:
            deck_state.pages[0][j] = deck_state.picklist_row[0][j]
            deck_state.red_pages[0][j] = deck_state.red_picklist_row[0][j]
        elif j == 3:
            if len(labelPrinters) > 3:
                deck_state.pages[0][j] = deck_state.page_next

            else:
                deck_state.pages[0][j] = None
                deck_state.red_pages[0][j] = None
        
        elif j >= 5 and j < 8:
            deck_state.pages[0][j] = deck_state.box_row[0][j-5]
            deck_state.red_pages[0][j] = deck_state.red_box_row[0][j-5]

        elif j == 8:
            if len(boxSizes) > 3:
                deck_state.pages[0][j] = format_image(create_text_overlay('./images/box.png', "Next", font_path='OpenSans-ExtraBold.ttf' ,font_color='#60acf7'))
            else:
                deck_state.pages[0][j] = None
                deck_state.red_pages[0][j] = None

        elif j >=10 and j < 13:
            deck_state.pages[0][j] = deck_state.shipping_row[0][j-10]
            deck_state.red_pages[0][j] = deck_state.red_shipping_row[0][j-10]

        elif j == 13:
            if len(labelPrinters) > 3:
                deck_state.pages[0][j] = format_image(create_text_overlay('./images/label_icon.png', "Next", font_path='OpenSans-ExtraBold.ttf' ,font_color='#60acf7', font_y_offset=6))
            else:
                deck_state.pages[0][j] = None
                deck_state.red_pages[0][j] = None

    for j in range(15):
        deck_state.deck.set_key_image(j, black_square if deck_state.pages[0][j]==None else deck_state.pages[0][j])
    return

def utility_buttons_setup(num_pages):
    '''
    Function to setup the utility buttons for the StreamDeck.
    '''
    if num_pages == 1:
        deck_state.pages[0][14] = deck_state.full_logo
        return
    for i in range(num_pages):
        deck_state.pages[i][4] = deck_state.next_image
        deck_state.pages[i][9] = deck_state.prev_image
        deck_state.pages[i][14] = deck_state.full_logo

def setup_doc_pages(docPrinters, addDocs):
    start_time = time.time()
    docs_flat = []
    red_docs_flat = []
    docs_text_flat = []
    for i in range(len(addDocs)):
        this_doc = []
        this_red_doc = []
        this_text = []
        for j in range(len(docPrinters)):
            this_doc.append(format_image(create_text_overlay('./images/page_icon.png', addDocs[i], font_size=16, font_path='OpenSans-ExtraBold.ttf', font_color='#60acf7', font_y_offset=6, subtext=docPrinters[j], subtext_font_size=13)))
            this_red_doc.append(format_image(apply_red_hue(create_text_overlay('./images/page_icon.png', addDocs[i], font_size=16, font_path='OpenSans-ExtraBold.ttf', font_color='#60acf7', font_y_offset=6, subtext=docPrinters[j], subtext_font_size=13))))
            this_text.append([addDocs[i], docPrinters[j]])

        docs_flat.append(this_doc)
        red_docs_flat.append(this_red_doc)
        docs_text_flat.append(this_text)

    docs_grouped = []
    docs_red_grouped = []
    docs_text_grouped = []

    for i in range(len(docs_flat)):
        cur_doc_page = []
        cur_red_doc_page = []
        cur_text_page = []
        working_data = docs_flat[i]
        working_data_red = red_docs_flat[i]
        working_data_text = docs_text_flat[i]

        for j in range(len(working_data)//3 + 1 if len(working_data) % 3 != 0 else len(working_data)//3):
            new_row = []
            new_red_row = []
            new_text_row = []
            for k in range(3):
                if j*3 + k >= len(working_data):
                    new_row.append(None)
                    new_red_row.append(None)
                    new_text_row.append(None)
                else:
                    new_row.append(working_data[j*3 + k])
                    new_red_row.append(working_data_red[j*3 + k])
                    new_text_row.append(working_data_text[j*3 + k])
            cur_doc_page.append(new_row)
            cur_red_doc_page.append(new_red_row)
            cur_text_page.append(new_text_row)

        docs_grouped.append(cur_doc_page)
        docs_red_grouped.append(cur_red_doc_page)
        docs_text_grouped.append(cur_text_page)

    deck_state.doc_pages = []
    deck_state.doc_red_pages = []
    deck_state.doc_text_pages = []

    for i in range(0, len(docs_grouped), 3):
        deck_state.doc_pages.append(docs_grouped[i:i+3])
        deck_state.doc_red_pages.append(docs_red_grouped[i:i+3])
        deck_state.doc_text_pages.append(docs_text_grouped[i:i+3])

    for i in range(1, len(deck_state.doc_pages)+1):
        for j in range(3):
            for k in range(3):
                if len(deck_state.doc_pages[i-1]) <= j:
                    deck_state.pages[i][j*5 + k] = None
                    deck_state.red_pages[i][j*5 + k] = None
                else:
                    deck_state.pages[i][j*5 + k] = deck_state.doc_pages[i-1][j][0][k]
                    deck_state.red_pages[i][j*5 + k] = deck_state.doc_red_pages[i-1][j][0][k]

    # Add next button to rows that have more than one page
    for i in range(len(deck_state.doc_pages)):
        for j in range(3):
            if len(deck_state.doc_pages[i]) > j and len(deck_state.doc_pages[i][j]) > 1:
                deck_state.pages[i+1][j*5 + 3] = deck_state.page_next

    # Setup the number of rows for each document
    deck_state.doc_num_rows = [[0,0,0] for _ in range(len(deck_state.doc_pages))]
    for i in range(len(deck_state.doc_pages)):
        for j in range(3):
            if len(deck_state.doc_pages[i]) > j:
                deck_state.doc_num_rows[i][j] = len(deck_state.doc_pages[i][j])
    
    deck_state.doc_current_rows = [[0,0,0] for _ in range(len(deck_state.doc_pages))]

    print("Doc pages setup complete.")
    print("Time taken: ", time.time() - start_time)

    # Enables next and prev page functionality
    deck_state.docs_ready = True

def page_setup(boxSizes=["4x4X4", "6X6X8", "8X8X12", "16X18X24"], docPrinters=["Printer 1", "Printer 2", "Printer 3", "Printer 4"], labelPrinters=["Printer 1", "Printer 2", "Printer 3", "Printer 4"], addDocs=["Doc. 1", "Doc. 2", "Doc. 3"]):
    '''
    Function to setup the pages for the StreamDeck.
    '''
    # Use ThreadPoolExecutor to run setup functions in parallel
    with ThreadPoolExecutor(max_workers=3) as executor:
        future_box = executor.submit(box_row_setup, boxSizes)
        future_shipping = executor.submit(shipping_row_setup, labelPrinters)
        future_picklist = executor.submit(picklist_row_setup, labelPrinters)

        future_box.result()
        future_shipping.result()
        future_picklist.result()

    num_pages = 1
    num_pages += len(addDocs) // 3 if len(addDocs) % 3 == 0 else len(addDocs) // 3 + 1

    deck_state.pages = [[None for _ in range(15)] for _ in range(num_pages)]
    deck_state.red_pages = [[None for _ in range(15)] for _ in range(num_pages)]

    utility_buttons_setup(num_pages)

    first_page_setup(labelPrinters, boxSizes)

    threading.Thread(target=setup_doc_pages, args=(docPrinters, addDocs)).start()

    return

def box_row_setup(boxSizes):
    '''
    Function to setup the rows for the StreamDeck.
    '''
    num_rows = len(boxSizes) // 3 if len(boxSizes) % 3 == 0 else len(boxSizes) // 3 + 1

    deck_state.box_row = [[None for _ in range(3)] for _ in range(num_rows)]
    deck_state.red_box_row = [[None for _ in range(3)] for _ in range(num_rows)]
    deck_state.box_row_text = [[None for _ in range(3)] for _ in range(num_rows)]

    for i in range(num_rows):
        for j in range(3):
            if (i * 3) + j < len(boxSizes):
                text = boxSizes[(i*3) + j]
                deck_state.box_row[i][j] = format_image(create_text_overlay('./images/box.png', text_to_overlay=text, font_size=16, font_path='./OpenSans-ExtraBold.ttf' ,font_color='#60acf7', font_y_offset=-3))
                deck_state.red_box_row[i][j] = format_image(apply_red_hue(create_text_overlay('./images/box.png', text_to_overlay=text, font_size=16, font_path='./OpenSans-ExtraBold.ttf' ,font_color='#60acf7', font_y_offset=-3)))
                deck_state._instance.box_row_text[i][j] = text

            else:
                deck_state.box_row[i][j] = None
                deck_state.red_box_row[i][j] = None
                deck_state.box_row_text[i][j] = None

    deck_state.current_box_row = 0

def shipping_row_setup(labelPrinters):
    '''
    Function to setup the shipping label rows for the StreamDeck.
    '''
    num_rows = len(labelPrinters) // 3 if len(labelPrinters) % 3 == 0 else len(labelPrinters) // 3 + 1

    deck_state.shipping_row = [[None for _ in range(3)] for _ in range(num_rows)]
    deck_state.red_shipping_row = [[None for _ in range(3)] for _ in range(num_rows)]
    deck_state.shipping_row_text = [[None for _ in range(3)] for _ in range(num_rows)]

    for i in range(num_rows):
        for j in range(3):
            if (i * 3) + j < len(labelPrinters):
                text = labelPrinters[(i*3) + j]

                deck_state.shipping_row[i][j] = format_image(create_text_overlay('./images/label_icon.png', text_to_overlay="Shipping", font_size=16, font_path='OpenSans-ExtraBold.ttf' ,font_color='#60acf7', font_y_offset=6, subtext=text, subtext_font_size=13))
                deck_state.red_shipping_row[i][j] = format_image(apply_red_hue(create_text_overlay('./images/label_icon.png', text_to_overlay="Shipping", font_size=16, font_path='OpenSans-ExtraBold.ttf' ,font_color='#60acf7', font_y_offset=6, subtext=text, subtext_font_size=13)))
                deck_state.shipping_row_text[i][j] = text
            else:
                deck_state.shipping_row[i][j] = None
                deck_state.red_shipping_row[i][j] = None
                deck_state.shipping_row_text[i][j] = None

    deck_state.current_shipping_row = 0

def picklist_row_setup(labelPrinters):
    '''
    Function to setup the picklist rows for the StreamDeck.
    '''
    num_rows = len(labelPrinters) // 3 if len(labelPrinters) % 3 == 0 else len(labelPrinters) // 3 + 1

    deck_state.picklist_row = [[None for _ in range(3)] for _ in range(num_rows)]
    deck_state.red_picklist_row = [[None for _ in range(3)] for _ in range(num_rows)]
    deck_state.picklist_row_text = [[None for _ in range(3)] for _ in range(num_rows)]

    for i in range(num_rows):
        for j in range(3):
            if (i * 3) + j < len(labelPrinters):
                text = labelPrinters[(i*3) + j]

                deck_state.picklist_row[i][j] = format_image(create_text_overlay('./images/page_icon.png', text_to_overlay="Picklist", font_size=16, font_path='OpenSans-ExtraBold.ttf' ,font_color='#60acf7', font_y_offset=6, subtext=text, subtext_font_size=13))
                deck_state.red_picklist_row[i][j] = format_image(apply_red_hue(create_text_overlay('./images/page_icon.png', text_to_overlay="Picklist", font_size=16, font_path='OpenSans-ExtraBold.ttf' ,font_color='#60acf7', font_y_offset=6, subtext=text, subtext_font_size=13)))
                deck_state.picklist_row_text[i][j] = text
            else:
                deck_state.picklist_row[i][j] = None
                deck_state.red_picklist_row[i][j] = None
                deck_state.picklist_row_text[i][j] = None

    deck_state.current_picklist_row = 0
                