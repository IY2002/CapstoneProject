from pre_image_processing import black_square, format_image, create_text_overlay, apply_red_hue, prep_image
from SingletonDeckState import SingletonDeckState
from concurrent.futures import ThreadPoolExecutor
import threading
import time

# Create an instance of SingletonDeckState
deck_state = SingletonDeckState()

# Function to setup the idle screen for the StreamDeck
def setup_idle_screen():
    '''
    Function to setup the idle screen for the StreamDeck.
    '''
    for j in range(15):
        if j <= 8:
            # Load and format the idle screen image for keys 0-8
            deck_state.idle_pages[j] = format_image(prep_image('./cut_logo/image_part_00' + str(j+1) + '.jpg'))
        else:
            # Load and format the idle screen image for keys 9-14
            deck_state.idle_pages[j] = format_image(prep_image('./cut_logo/image_part_0' + str(j+1) + '.jpg'))

# Function to setup the first page for the StreamDeck
def first_page_setup(labelPrinters, boxSizes):
    '''
    Function to setup the first page for the StreamDeck.
    '''

    for j in range(15):

        if j >= 0 and j < 3:
            # Assign the box row images to keys 0-2
            deck_state.pages[0][j] = deck_state.box_row[0][j]
            deck_state.red_pages[0][j] = deck_state.red_box_row[0][j]

        elif j == 3:
            if len(boxSizes) > 3:
                # Create a "Next" button image for key 3 if there are more box sizes
                deck_state.pages[0][j] = format_image(create_text_overlay('./images/box.png', "Next", font_path='OpenSans-ExtraBold.ttf' ,font_color='#60acf7'))
            else:
                # Set key 3 to None if there are no more box sizes
                deck_state.pages[0][j] = None
                deck_state.red_pages[0][j] = None

        elif j >=5 and j < 8:
            # Assign the shipping row images to keys 5-7
            deck_state.pages[0][j] = deck_state.shipping_row[0][j-5]
            deck_state.red_pages[0][j] = deck_state.red_shipping_row[0][j-5]

        elif j == 8:
            if len(labelPrinters) > 3:
                # Create a "Next" button image for key 8 if there are more label printers
                deck_state.pages[0][j] = format_image(create_text_overlay('./images/label_icon.png', "Next", font_path='OpenSans-ExtraBold.ttf' ,font_color='#60acf7', font_y_offset=6))
            else:
                # Set key 8 to None if there are no more label printers
                deck_state.pages[0][j] = None
                deck_state.red_pages[0][j] = None

    for j in range(15):
        # Set the key images on the StreamDeck to the corresponding images in deck_state.pages
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
    # Start timer to measure execution time
    start_time = time.time()

    # Initialize empty lists to store images and text for each document page
    docs_flat = []
    red_docs_flat = []
    docs_text_flat = []

    # Iterate over each document and printer combination
    for i in range(len(addDocs)):
        this_doc = []
        this_red_doc = []
        this_text = []

        # Generate images and text for each printer
        for j in range(len(docPrinters)):
            this_doc.append(format_image(create_text_overlay('./images/page_icon.png', addDocs[i], font_size=16, font_path='OpenSans-ExtraBold.ttf', font_color='#60acf7', font_y_offset=6, subtext=docPrinters[j], subtext_font_size=13)))
            this_red_doc.append(format_image(apply_red_hue(create_text_overlay('./images/page_icon.png', addDocs[i], font_size=16, font_path='OpenSans-ExtraBold.ttf', font_color='#60acf7', font_y_offset=6, subtext=docPrinters[j], subtext_font_size=13))))
            this_text.append([addDocs[i], docPrinters[j]])

        # Append generated images and text to respective lists
        docs_flat.append(this_doc)
        red_docs_flat.append(this_red_doc)
        docs_text_flat.append(this_text)

    # Group the images and text into pages
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

        # Split the images and text into rows of 3
        for j in range(len(working_data)//3 + 1 if len(working_data) % 3 != 0 else len(working_data)//3):
            new_row = []
            new_red_row = []
            new_text_row = []

            # Add images and text to each row
            for k in range(3):
                if j*3 + k >= len(working_data):
                    new_row.append(None)
                    new_red_row.append(None)
                    new_text_row.append(None)
                else:
                    new_row.append(working_data[j*3 + k])
                    new_red_row.append(working_data_red[j*3 + k])
                    new_text_row.append(working_data_text[j*3 + k])

            # Append rows to the current document page
            cur_doc_page.append(new_row)
            cur_red_doc_page.append(new_red_row)
            cur_text_page.append(new_text_row)

        # Append document pages to respective lists
        docs_grouped.append(cur_doc_page)
        docs_red_grouped.append(cur_red_doc_page)
        docs_text_grouped.append(cur_text_page)

    # Update the deck state with the generated document pages
    deck_state.doc_pages = []
    deck_state.doc_red_pages = []
    deck_state.doc_text_pages = []

    for i in range(0, len(docs_grouped), 3):
        deck_state.doc_pages.append(docs_grouped[i:i+3])
        deck_state.doc_red_pages.append(docs_red_grouped[i:i+3])
        deck_state.doc_text_pages.append(docs_text_grouped[i:i+3])

    # Update the StreamDeck with the images from the document pages
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

    # Initialize the current row for each document
    deck_state.doc_current_rows = [[0,0,0] for _ in range(len(deck_state.doc_pages))]

    # Print completion message and execution time
    print("Doc pages setup complete.")
    print("Time taken: ", time.time() - start_time)

    # Enable next and prev page functionality
    deck_state.docs_ready = True

def page_setup(boxSizes=["4x4X4", "6X6X8", "8X8X12", "16X18X24"], docPrinters=["Printer 1", "Printer 2", "Printer 3", "Printer 4"], labelPrinters=["Printer 1", "Printer 2", "Printer 3", "Printer 4"], addDocs=["Doc. 1", "Doc. 2", "Doc. 3"], data=None):
    '''
    Function to setup the pages for the StreamDeck.
    '''

    if data is not None:
        deck_state.data = data
        
    # Use ThreadPoolExecutor to run setup functions in parallel
    with ThreadPoolExecutor(max_workers=3) as executor:
        future_box = executor.submit(box_row_setup, boxSizes)  # Submit box_row_setup function to executor
        future_shipping = executor.submit(shipping_row_setup, labelPrinters)  # Submit shipping_row_setup function to executor

        future_box.result()  # Wait for box_row_setup to complete
        future_shipping.result()  # Wait for shipping_row_setup to complete

    num_pages = 1
    num_pages += len(addDocs) // 3 if len(addDocs) % 3 == 0 else len(addDocs) // 3 + 1

    deck_state.pages = [[None for _ in range(15)] for _ in range(num_pages)]  # Initialize pages list with None values
    deck_state.red_pages = [[None for _ in range(15)] for _ in range(num_pages)]  # Initialize red_pages list with None values

    utility_buttons_setup(num_pages)  # Call utility_buttons_setup function

    first_page_setup(labelPrinters, boxSizes)  # Call first_page_setup function

    threading.Thread(target=setup_doc_pages, args=(docPrinters, addDocs)).start()  # Start a new thread to run setup_doc_pages function

    return

def box_row_setup(boxSizes):
    '''
    Function to setup the rows for the StreamDeck.
    '''
    num_rows = len(boxSizes) // 3 if len(boxSizes) % 3 == 0 else len(boxSizes) // 3 + 1  # Calculate the number of rows

    deck_state.box_row = [[None for _ in range(3)] for _ in range(num_rows)]  # Initialize box_row list with None values
    deck_state.red_box_row = [[None for _ in range(3)] for _ in range(num_rows)]  # Initialize red_box_row list with None values
    deck_state.box_row_text = [[None for _ in range(3)] for _ in range(num_rows)]  # Initialize box_row_text list with None values

    for i in range(num_rows):
        for j in range(3):
            if (i * 3) + j < len(boxSizes):
                text = boxSizes[(i*3) + j]  # Get the text for the current box
                deck_state.box_row[i][j] = format_image(create_text_overlay('./images/box.png', text_to_overlay=text, font_size=16, font_path='./OpenSans-ExtraBold.ttf' ,font_color='#60acf7', font_y_offset=-3))  # Create and format the image for the box
                deck_state.red_box_row[i][j] = format_image(apply_red_hue(create_text_overlay('./images/box.png', text_to_overlay=text, font_size=16, font_path='./OpenSans-ExtraBold.ttf' ,font_color='#60acf7', font_y_offset=-3)))  # Create and format the red image for the box
                deck_state._instance.box_row_text[i][j] = text  # Store the text for the box

            else:
                deck_state.box_row[i][j] = None  # Set the box image to None
                deck_state.red_box_row[i][j] = None  # Set the red box image to None
                deck_state.box_row_text[i][j] = None  # Set the box text to None

    deck_state.current_box_row = 0  # Set the current box row to 0

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

                # Generate shipping label images with text overlay
                deck_state.shipping_row[i][j] = format_image(create_text_overlay('./images/label_icon.png', text_to_overlay="Shipping", font_size=16, font_path='OpenSans-ExtraBold.ttf' ,font_color='#60acf7', font_y_offset=6, subtext=text, subtext_font_size=13))
                deck_state.red_shipping_row[i][j] = format_image(apply_red_hue(create_text_overlay('./images/label_icon.png', text_to_overlay="Shipping", font_size=16, font_path='OpenSans-ExtraBold.ttf' ,font_color='#60acf7', font_y_offset=6, subtext=text, subtext_font_size=13)))
                deck_state.shipping_row_text[i][j] = text
            else:
                # Set remaining shipping label images to None
                deck_state.shipping_row[i][j] = None
                deck_state.red_shipping_row[i][j] = None
                deck_state.shipping_row_text[i][j] = None

    deck_state.current_shipping_row = 0
