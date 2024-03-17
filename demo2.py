from PIL import Image, ImageDraw, ImageFont
from PIL.Image import Resampling
from StreamDeck.DeviceManager import DeviceManager
from StreamDeck.ImageHelpers import PILHelper

thumbs_up = None
thumbs_down = None
white_square = None
red_square = None
green_square = None
blue_square = None
yellow_square = None
next_image = None
prev_image = None
start_button = None
full_logo = None

process_input = True

current_page = 1

current_row = 0

deck = None

button_states = [False for _ in range(15)]

pages = [[None for _ in range(15)] for _ in range(3)]

page_1_row_1 = [[None for _ in range(3)] for _ in range(3)]

def connect_to_elgato():
    '''
    Function to connect to the Elgato StreamDeck.
    '''
    global deck
    # connect to streamdeck
    streamdecks = DeviceManager().enumerate()
    if not streamdecks:
        # throw an error if streamdeck is not found
        raise LookupError("No Stream Decks were found")
    
    deck = streamdecks[0]

def prep_image(file_path):
    '''
    Function to prepare an image to be displayed on the StreamDeck.
    '''
    image = Image.open(file_path)
    resized_image = PILHelper.create_scaled_image(deck, image, margins=[0,0,0,0])
    return PILHelper.to_native_format(deck, resized_image)

def image_setup():
    '''
    Function to pre-load the images and set them up to be displayed on the StreamDeck.
    '''
    global thumbs_up
    global thumbs_down
    global white_square
    global red_square
    global green_square
    global blue_square
    global yellow_square
    global next_image
    global prev_image
    global start_button
    global full_logo

    thumbs_up = prep_image('./images/thumbs_up.png')
    thumbs_down = prep_image('./images/thumbs_down.png')
    white_square = prep_image('./images/white_square.jpg')
    red_square = prep_image('./images/Solid_red.svg.png')
    green_square = prep_image('./images/green_square.png')
    blue_square = prep_image('./images/blue_square.jpeg')
    yellow_square = prep_image('./images/yellow_square.jpg')
    next_image = prep_image('./images/next_icon.png')
    prev_image = prep_image('./images/prev_icon.png')
    start_button = prep_image('./images/start_icon.png')
    full_logo = prep_image('./images/full_logo.png')

def create_text_overlay(image_path, text_to_overlay, font_path="./Copyduck.ttf", font_size=18, font_color='#000000', font_y_offset=0):
    '''
    Overlay the specified text onto the image at the given path.
    '''
    # Load the image from the given path
    try:
        # Load the image from the given path
        image = Image.open(image_path)
    except FileNotFoundError:
        print("Error: The specified image file was not found.")
        return None
    except IOError:
        print("Error: There was an issue opening the image file. The file may be corrupted or in an unsupported format.")
        return None
    
    image = image.resize((72, 72), Resampling.LANCZOS)

    draw = ImageDraw.Draw(image)

    # Setup the font
    font = ImageFont.truetype(font_path, font_size)

    # Calculate the bounding box of the text
    text_bbox = draw.textbbox((0, 0), text_to_overlay, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    # Calculate the position for the text to be centered on the image
    text_x = (image.width - text_width) / 2
    text_y = ((image.height - text_height) / 2) - font_y_offset

    # Draw the text on the image
    draw.text((text_x, text_y), text_to_overlay, fill=font_color, font=font)

    resized_image = PILHelper.create_scaled_image(deck, image, margins=[0,0,0,0])
    return PILHelper.to_native_format(deck, resized_image)

def key_helper(key):
    global current_row

    if current_page == 1 and key == 8:
        current_row = (current_row + 1) % 3
    display_page()
    return

def key_change_callback(deck, key, state):
    '''
    Function to handle key presses on the StreamDeck.
    '''
    if state:
        if key == 4:
            next_page()
        elif key == 9:
            prev_page()
        else:
            key_helper(key)
        
def page_setup():
    '''
    Function to setup the pages for the StreamDeck.
    '''
    row_setup()
    global pages

    for j in range(15):
        if j <= 8:
            pages[0][j] = prep_image('./cut_logo/image_part_00' + str(j+1) + '.jpg')
        else:
            pages[0][j] = prep_image('./cut_logo/image_part_0' + str(j+1) + '.jpg')

        if j >= 5 and j < 8:
            pages[1][j] = page_1_row_1[0][j-5]
        elif j == 8:
            pages[1][j] = create_text_overlay('./images/box.png', "Next", font_path='OpenSans-ExtraBold.ttf' ,font_color='#60acf7')
        elif j >= 0 and j < 5:
            pages[1][j] = create_text_overlay('./images/page_icon.png', "Picklist", font_size=18,font_path='OpenSans-ExtraBold.ttf' ,font_color='#60acf7', font_y_offset=6)
        elif j >=10 and j < 14:
            pages[1][j] = create_text_overlay('./images/label_icon.png', "Shipping", font_size=16, font_path='OpenSans-ExtraBold.ttf', font_color='#60acf7')
        else:
            pages[1][j] = full_logo

        pages[2][j] = green_square
    
    pages[2][4] = next_image
    pages[2][9] = prev_image

    pages[1][4] = next_image
    pages[1][9] = prev_image

def page_update():
    global pages

    for i in range(3):
        pages[1][i+5] = page_1_row_1[current_row][i]

def display_page():
    '''
    Function to display a page on the StreamDeck.
    '''
    page_update()

    for i in range(15):
        deck.set_key_image(i, pages[current_page][i])

def next_page():
    '''
    Function to move to the next page on the StreamDeck.
    '''
    global current_page
    current_page = (current_page + 1) % 3
    display_page()

def prev_page():
    '''
    Function to move to the previous page on the StreamDeck.
    '''
    global current_page
    current_page = (current_page - 1) % 3
    display_page()

def row_setup():
    '''
    Function to setup the rows for the StreamDeck.
    '''
    global page_1_row_1

    for j in range(3):
        page_1_row_1[0][j] = create_text_overlay('./images/box.png', "4X4X" + str(((j + 1 )) * 4), font_size=15, font_path='OpenSans-ExtraBold.ttf' ,font_color='#60acf7')
        page_1_row_1[1][j] = create_text_overlay('./images/box.png', "6X8X" + str(((j + 3)) * 2), font_size=15, font_path='OpenSans-ExtraBold.ttf' ,font_color='#60acf7')
        page_1_row_1[2][j] = create_text_overlay('./images/box.png', "8X10X" + str(((j + 3)) * 4), font_size=15, font_path='OpenSans-ExtraBold.ttf' ,font_color='#60acf7')

def pause_deck():
    deck.close()

def unpause_deck():
    deck.open()

def setup():
    '''
    Function to setup the StreamDeck.
    '''
    connect_to_elgato()
    image_setup()
    page_setup()
    deck.open()
    deck.set_key_callback(key_change_callback)
    display_page()
    
    try:
        while True:
            pass
    except KeyboardInterrupt:
        deck.close()

if __name__ == "__main__":
    setup()