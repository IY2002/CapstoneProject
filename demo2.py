from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from PIL.Image import Resampling
from StreamDeck.DeviceManager import DeviceManager
from StreamDeck.ImageHelpers import PILHelper
import time

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

current_page = 0

current_row = 0

deck = None

button_states = [False for _ in range(15)]

pages = [[None for _ in range(15)] for _ in range(3)]

red_pages = [[None for _ in range(15)] for _ in range(3)]

page_0_row_1 = [[None for _ in range(3)] for _ in range(3)]

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
    return resized_image

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

def apply_red_hue(image, intensity=0.5):
    """
    Applies a red hue to the given PIL Image object.

    :param image: A PIL Image object to apply the red hue to.
    :param intensity: The intensity of the red hue, ranging from 0.0 to 1.0.
    :return: A new PIL Image object with the red hue applied.
    """

    # Create a red overlay
    red_overlay = Image.new("RGB", image.size, (255, 0, 0))

    # Blend the original image with the red overlay
    tinted_image = Image.blend(image, red_overlay, intensity)

    # Return the tinted image
    return tinted_image

def format_image(image):
    '''
    Function to format an image to be displayed on the StreamDeck.
    '''
    return PILHelper.to_native_format(deck, image)

def create_text_overlay(image_path, text_to_overlay, font_path="./Copyduck.ttf", font_size=18, font_color='white', font_y_offset=0, subtext=None, subtext_font_size=12, subtext_font_color='white', apply_red_hue=False):
    '''
    Overlay the specified text onto the image at the given path. If apply_red_hue is True, adds a red hue to the entire image including the text.
    '''
    try:
        base_image = Image.open(image_path)
    except FileNotFoundError:
        print("Error: The specified image file was not found.")
        return None
    except IOError:
        print("Error: There was an issue opening the image file. The file may be corrupted or in an unsupported format.")
        return None

    base_image = base_image.resize((72, 72), Image.Resampling.LANCZOS)
    overlay_image = Image.new("RGBA", base_image.size, (255,255,255,0))  # Create a transparent overlay
    draw = ImageDraw.Draw(overlay_image)

    # Setup the font for the main text
    font = ImageFont.truetype(font_path, font_size)

    # Calculate the position and draw the main text
    text_x, text_y = calculate_text_position(draw, overlay_image, text_to_overlay, font, font_y_offset)
    draw.text((text_x, text_y), text_to_overlay, fill=font_color, font=font)

    # Setup the font and draw the subtext if provided
    if subtext:
        sub_font = ImageFont.truetype(font_path, subtext_font_size)
        subtext_x, subtext_y = calculate_text_position(draw, overlay_image, subtext, sub_font, 0)
        draw.text((subtext_x, subtext_y + 15), subtext, fill=subtext_font_color, font=sub_font)

    if apply_red_hue:
        red_image = Image.new("RGB", base_image.size, (255, 0, 0))
        base_image = Image.blend(base_image.convert("RGB"), red_image, 0.4) 
        base_image = Image.alpha_composite(base_image.convert("RGBA"), overlay_image)
    else:
        base_image.paste(overlay_image, (0, 0), overlay_image)  # Paste the text overlay onto the base image

    resized_image = PILHelper.create_scaled_image(deck, base_image, margins=[0,0,0,0])
    return resized_image

def calculate_text_position(draw, image, text, font, y_offset=0):
    '''
    Calculate the position for the text to be centered on the image.
    '''
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    text_x = (image.width - text_width) / 2
    text_y = ((image.height - text_height) / 2) - y_offset
    return text_x, text_y
    
def key_helper(key):
    print("Key HELPER {} was pressed".format(key))
    global current_row
    if current_page == 0 and key == 8:
        current_row = (current_row + 1) % 3
        display_page()
    else:
        deck.set_key_image(key, format_image(apply_red_hue(pages[current_page][key])))
        pause_deck()
        time.sleep(3)
        unpause_deck()
        display_page()
        deck.set_key_image(key, format_image(pages[current_page][key]))
    return

def idle_screen():
    '''
    Function to display the idle screen on the StreamDeck.
    '''
    global current_page
    current_page = 2
    display_page()

def key_change_callback(deck, key, state):
    '''
    Function to handle key presses on the StreamDeck.
    '''
    global current_page
    if state:
        print("Key {} was pressed".format(key))
        if key == 4 and current_page != 2:
            next_page()
        elif key == 9 and current_page != 2:
            prev_page()
        elif key == 14 and current_page != 2:
            idle_screen()
        elif key == 14:
            current_page = 0
            display_page()
        else:
            key_helper(key)
        
def page_setup():
    '''
    Function to setup the pages for the StreamDeck.
    '''
    row_setup()
    global pages
    global red_pages

    for j in range(15):

        if j <= 8:
            pages[2][j] = prep_image('./cut_logo/image_part_00' + str(j+1) + '.jpg')
        else:
            pages[2][j] = prep_image('./cut_logo/image_part_0' + str(j+1) + '.jpg')

        if j >= 5 and j < 8:
            pages[0][j] = page_0_row_1[0][j-5]
            pages[1][j] = create_text_overlay('./images/page_icon.png', "Doc. 2", font_size=18,font_path='OpenSans-ExtraBold.ttf' ,font_color='#60acf7', font_y_offset=6, subtext="Printer " + str(j - 4), subtext_font_size=13)

        elif j == 8:
            pages[0][j] = create_text_overlay('./images/box.png', "Next", font_path='OpenSans-ExtraBold.ttf' ,font_color='#60acf7')
            pages[1][j] = create_text_overlay('./images/page_icon.png', "Doc. 2", font_size=18,font_path='OpenSans-ExtraBold.ttf' ,font_color='#60acf7', font_y_offset=6, subtext="Printer " + str(j - 4), subtext_font_size=13)
        elif j >= 0 and j < 5:
            pages[0][j] = create_text_overlay('./images/page_icon.png', "Picklist", font_size=16,font_path='OpenSans-ExtraBold.ttf' ,font_color='#60acf7', font_y_offset=6, subtext="Printer " + str(j + 1), subtext_font_size=13)
            pages[1][j] = create_text_overlay('./images/page_icon.png', "Doc. 1", font_size=18,font_path='OpenSans-ExtraBold.ttf' ,font_color='#60acf7', font_y_offset=6, subtext="Printer " + str(j +1), subtext_font_size=13)
        elif j >=10 and j < 14:
            pages[0][j] = create_text_overlay('./images/label_icon.png', "Shipping", font_size=16, font_path='OpenSans-ExtraBold.ttf', font_color='#60acf7',font_y_offset=6, subtext="Printer " + str(j - 9), subtext_font_size=13)
            pages[1][j] = create_text_overlay('./images/page_icon.png', "Doc. 3", font_size=16, font_path='OpenSans-ExtraBold.ttf', font_color='#60acf7',font_y_offset=6, subtext="Printer " + str(j - 9), subtext_font_size=13)         

    pages[0][14] = full_logo
    pages[1][14] = full_logo
    
    pages[0][4] = next_image
    pages[0][9] = prev_image

    pages[1][4] = next_image
    pages[1][9] = prev_image

def page_update():
    global pages

    for i in range(3):
        pages[0][i+5] = page_0_row_1[current_row][i]

def display_page():
    '''
    Function to display a page on the StreamDeck.
    '''
    page_update()

    for i in range(15):
        deck.set_key_image(i, format_image(pages[current_page][i]))

def next_page():
    '''
    Function to move to the next page on the StreamDeck.
    '''
    global current_page
    current_page = (current_page + 1) % 2
    display_page()

def prev_page():
    '''
    Function to move to the previous page on the StreamDeck.
    '''
    global current_page
    current_page = (current_page - 1) % 2
    display_page()

def row_setup():
    '''
    Function to setup the rows for the StreamDeck.
    '''
    global page_0_row_1

    for j in range(3):
        page_0_row_1[0][j] = create_text_overlay('./images/box.png', "4X4X" + str(((j + 1 )) * 4), font_size=16, font_path='OpenSans-ExtraBold.ttf' ,font_color='#60acf7', font_y_offset=-3)
        page_0_row_1[1][j] = create_text_overlay('./images/box.png', "6X8X" + str(((j + 3)) * 2), font_size=16, font_path='OpenSans-ExtraBold.ttf' ,font_color='#60acf7', font_y_offset=-3)
        page_0_row_1[2][j] = create_text_overlay('./images/box.png', "8X10X" + str(((j + 3)) * 4), font_size=16, font_path='OpenSans-ExtraBold.ttf' ,font_color='#60acf7', font_y_offset=-3)

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