from PIL import Image, ImageDraw, ImageFont
from StreamDeck.ImageHelpers import PILHelper
from SingletonDeckState import SingletonDeckState
import os, psutil

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

pages = [[None for _ in range(15)] for _ in range(3)]

red_pages = [[None for _ in range(15)] for _ in range(3)]

page_0_row_1 = [[None for _ in range(3)] for _ in range(3)]

red_page_0_row_1 = [[None for _ in range(3)] for _ in range(3)]

deck_state = SingletonDeckState()

def print_memory_usage():
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    # Convert bytes to megabytes
    memory_used = memory_info.rss / 1024 / 1024
    print(f"Memory used: {memory_used:.2f} MB")

def prep_image(file_path):
    '''
    Function to prepare an image to be displayed on the StreamDeck.
    '''
    image = Image.open(file_path)
    resized_image = PILHelper.create_scaled_image(deck_state.deck, image, margins=[0,0,0,0])
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

    thumbs_up = format_image(prep_image('./images/thumbs_up.png'))
    thumbs_down = format_image(prep_image('./images/thumbs_down.png'))
    white_square = format_image(prep_image('./images/white_square.jpg'))
    red_square = format_image(prep_image('./images/Solid_red.svg.png'))
    green_square = format_image(prep_image('./images/green_square.png'))
    blue_square = format_image(prep_image('./images/blue_square.jpeg'))
    yellow_square = format_image(prep_image('./images/yellow_square.jpg'))
    next_image = format_image(prep_image('./images/next_icon.png'))
    prev_image = format_image(prep_image('./images/prev_icon.png'))
    start_button = format_image(prep_image('./images/start_icon.png'))
    full_logo = format_image(prep_image('./images/full_logo.png'))

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
    return PILHelper.to_native_format(deck_state.deck, image)

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

    resized_image = PILHelper.create_scaled_image(deck_state.deck, base_image, margins=[0,0,0,0])
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

def page_setup():
    '''
    Function to setup the pages for the StreamDeck.
    '''
    row_setup()
    global pages
    global red_pages

    for j in range(15):

        if j <= 8:
            pages[2][j] = format_image(prep_image('./cut_logo/image_part_00' + str(j+1) + '.jpg'))
        else:
            pages[2][j] = format_image(prep_image('./cut_logo/image_part_0' + str(j+1) + '.jpg'))

        if j >= 5 and j < 8:
            pages[0][j] = page_0_row_1[0][j-5]
            pages[1][j] = format_image(create_text_overlay('./images/page_icon.png', "Doc. 2", font_size=18,font_path='OpenSans-ExtraBold.ttf' ,font_color='#60acf7', font_y_offset=6, subtext="Printer " + str(j - 4), subtext_font_size=13))
            red_pages[0][j] = red_page_0_row_1[0][j-5]
            red_pages[1][j] = format_image(apply_red_hue(create_text_overlay('./images/page_icon.png', "Doc. 2", font_size=18,font_path='OpenSans-ExtraBold.ttf' ,font_color='#60acf7', font_y_offset=6, subtext="Printer " + str(j - 4), subtext_font_size=13)))

        elif j == 8:
            pages[0][j] = format_image(create_text_overlay('./images/box.png', "Next", font_path='OpenSans-ExtraBold.ttf' ,font_color='#60acf7'))
            pages[1][j] = format_image(create_text_overlay('./images/page_icon.png', "Doc. 2", font_size=18,font_path='OpenSans-ExtraBold.ttf' ,font_color='#60acf7', font_y_offset=6, subtext="Printer " + str(j - 4), subtext_font_size=13))
            red_pages[0][j] = format_image(apply_red_hue(create_text_overlay('./images/box.png', "Next", font_path='OpenSans-ExtraBold.ttf' ,font_color='#60acf7')))
            red_pages[1][j] = format_image(apply_red_hue(create_text_overlay('./images/page_icon.png', "Doc. 2", font_size=18,font_path='OpenSans-ExtraBold.ttf' ,font_color='#60acf7', font_y_offset=6, subtext="Printer " + str(j - 4), subtext_font_size=13)))

        elif j >= 0 and j < 5:
            pages[0][j] = format_image(create_text_overlay('./images/page_icon.png', "Picklist", font_size=16,font_path='OpenSans-ExtraBold.ttf' ,font_color='#60acf7', font_y_offset=6, subtext="Printer " + str(j + 1), subtext_font_size=13))
            pages[1][j] = format_image(create_text_overlay('./images/page_icon.png', "Doc. 1", font_size=18,font_path='OpenSans-ExtraBold.ttf' ,font_color='#60acf7', font_y_offset=6, subtext="Printer " + str(j +1), subtext_font_size=13))
            red_pages[0][j] = format_image(apply_red_hue(create_text_overlay('./images/page_icon.png', "Picklist", font_size=16,font_path='OpenSans-ExtraBold.ttf' ,font_color='#60acf7', font_y_offset=6, subtext="Printer " + str(j + 1), subtext_font_size=13)))
            red_pages[1][j] = format_image(apply_red_hue(create_text_overlay('./images/page_icon.png', "Doc. 1", font_size=18,font_path='OpenSans-ExtraBold.ttf' ,font_color='#60acf7', font_y_offset=6, subtext="Printer " + str(j +1), subtext_font_size=13)))

        elif j >=10 and j < 14:
            pages[0][j] = format_image(create_text_overlay('./images/label_icon.png', "Shipping", font_size=16, font_path='OpenSans-ExtraBold.ttf', font_color='#60acf7',font_y_offset=6, subtext="Printer " + str(j - 9), subtext_font_size=13))
            pages[1][j] = format_image(create_text_overlay('./images/page_icon.png', "Doc. 3", font_size=16, font_path='OpenSans-ExtraBold.ttf', font_color='#60acf7',font_y_offset=6, subtext="Printer " + str(j - 9), subtext_font_size=13))   
            red_pages[0][j] = format_image(apply_red_hue(create_text_overlay('./images/label_icon.png', "Shipping", font_size=16, font_path='OpenSans-ExtraBold.ttf', font_color='#60acf7',font_y_offset=6, subtext="Printer " + str(j - 9), subtext_font_size=13)))
            red_pages[1][j] = format_image(apply_red_hue(create_text_overlay('./images/page_icon.png', "Doc. 3", font_size=16, font_path='OpenSans-ExtraBold.ttf', font_color='#60acf7',font_y_offset=6, subtext="Printer " + str(j - 9), subtext_font_size=13)))      

    pages[0][14] = full_logo
    pages[1][14] = full_logo
    
    pages[0][4] = next_image
    pages[0][9] = prev_image

    pages[1][4] = next_image
    pages[1][9] = prev_image

def row_setup():
    '''
    Function to setup the rows for the StreamDeck.
    '''
    global page_0_row_1
    global red_page_0_row_1

    for j in range(3):
        page_0_row_1[0][j] = format_image(create_text_overlay('./images/box.png', "4X4X" + str(((j + 1 )) * 4), font_size=16, font_path='OpenSans-ExtraBold.ttf' ,font_color='#60acf7', font_y_offset=-3))
        page_0_row_1[1][j] = format_image(create_text_overlay('./images/box.png', "6X8X" + str(((j + 3)) * 2), font_size=16, font_path='OpenSans-ExtraBold.ttf' ,font_color='#60acf7', font_y_offset=-3))
        page_0_row_1[2][j] = format_image(create_text_overlay('./images/box.png', "8X10X" + str(((j + 3)) * 4), font_size=16, font_path='OpenSans-ExtraBold.ttf' ,font_color='#60acf7', font_y_offset=-3))
        red_page_0_row_1[0][j] = format_image(apply_red_hue(create_text_overlay('./images/box.png', "4X4X" + str(((j + 1 )) * 4), font_size=16, font_path='OpenSans-ExtraBold.ttf' ,font_color='#60acf7', font_y_offset=-3)))
        red_page_0_row_1[1][j] = format_image(apply_red_hue(create_text_overlay('./images/box.png', "6X8X" + str(((j + 3)) * 2), font_size=16, font_path='OpenSans-ExtraBold.ttf' ,font_color='#60acf7', font_y_offset=-3)))
        red_page_0_row_1[2][j] = format_image(apply_red_hue(create_text_overlay('./images/box.png', "8X10X" + str(((j + 3)) * 4), font_size=16, font_path='OpenSans-ExtraBold.ttf' ,font_color='#60acf7', font_y_offset=-3)))

    print_memory_usage()