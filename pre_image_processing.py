from PIL import Image, ImageDraw, ImageFont
from StreamDeck.ImageHelpers import PILHelper
from SingletonDeckState import SingletonDeckState

thumbs_up = None
thumbs_down = None
white_square = None
red_square = None
green_square = None
blue_square = None
black_square = None
yellow_square = None
# next_image = None
# prev_image = None
start_button = None
# full_logo = None
# page_next  = None

deck_state = SingletonDeckState()

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
    # global next_image
    # global prev_image
    global start_button
    global black_square
    # global page_next

    thumbs_up = format_image(prep_image('./images/thumbs_up.png'))
    thumbs_down = format_image(prep_image('./images/thumbs_down.png'))
    white_square = format_image(prep_image('./images/white_square.jpg'))
    red_square = format_image(prep_image('./images/Solid_red.svg.png'))
    green_square = format_image(prep_image('./images/green_square.png'))
    blue_square = format_image(prep_image('./images/blue_square.jpeg'))
    yellow_square = format_image(prep_image('./images/yellow_square.jpg'))
    deck_state.next_image = format_image(prep_image('./images/next_icon.png'))
    deck_state.prev_image = format_image(prep_image('./images/prev_icon.png'))
    start_button = format_image(prep_image('./images/start_icon.png'))
    deck_state.full_logo = format_image(prep_image('./images/full_logo.png'))
    black_square = format_image(prep_image('./images/black_square.png'))
    deck_state.page_next = format_image(create_text_overlay('./images/page_icon.png', "Next", font_path='OpenSans-ExtraBold.ttf' ,font_color='#60acf7', font_y_offset=6))

def apply_red_hue(image, intensity=0.5):
    """
    Applies a red hue to the given PIL Image object.
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

