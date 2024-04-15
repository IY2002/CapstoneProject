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

def calculator_images_setup():
    '''
    Function to setup and save the calculator images for the StreamDeck.
    '''
    for i in range(3):
        deck_state.calc_pages[i] = format_image(create_text_overlay('./images/black_square.png', str(i + 1), font_path='OpenSans-ExtraBold.ttf', font_color='#60acf7', font_y_offset=6, font_size=28))
        deck_state.calc_red_pages[i] = format_image(apply_red_hue(create_text_overlay('./images/black_square.png', str(i + 1), font_path='OpenSans-ExtraBold.ttf', font_color='#60acf7', font_y_offset=6, font_size=28)))

        deck_state.calc_pages[i + 5] = format_image(create_text_overlay('./images/black_square.png', str(i + 4), font_path='OpenSans-ExtraBold.ttf', font_color='#60acf7', font_y_offset=6, font_size=28))
        deck_state.calc_red_pages[i + 5] = format_image(apply_red_hue(create_text_overlay('./images/black_square.png', str(i + 4), font_path='OpenSans-ExtraBold.ttf', font_color='#60acf7', font_y_offset=6, font_size=28)))

        deck_state.calc_pages[i + 10] = format_image(create_text_overlay('./images/black_square.png', str(i + 7), font_path='OpenSans-ExtraBold.ttf', font_color='#60acf7', font_y_offset=6, font_size=28))
        deck_state.calc_red_pages[i + 10] = format_image(apply_red_hue(create_text_overlay('./images/black_square.png', str(i + 7), font_path='OpenSans-ExtraBold.ttf', font_color='#60acf7', font_y_offset=6, font_size=28)))

    deck_state.calc_pages[13] = format_image(create_text_overlay('./images/black_square.png', "0", font_path='OpenSans-ExtraBold.ttf', font_color='#60acf7', font_y_offset=6, font_size=28))
    deck_state.calc_red_pages[13] = format_image(apply_red_hue(create_text_overlay('./images/black_square.png', "0", font_path='OpenSans-ExtraBold.ttf', font_color='#60acf7', font_y_offset=6, font_size=28)))

    deck_state.calc_pages[8] = format_image(create_text_overlay('./images/black_square.png', ".", font_path='OpenSans-ExtraBold.ttf', font_color='#60acf7', font_y_offset=6, font_size=28))
    deck_state.calc_red_pages[8] = format_image(apply_red_hue(create_text_overlay('./images/black_square.png', ".", font_path='OpenSans-ExtraBold.ttf', font_color='#60acf7', font_y_offset=6, font_size=28)))

    deck_state.calc_pages[9] = format_image(prep_image('./images/delete_logo.png'))
    deck_state.calc_red_pages[9] = format_image(apply_red_hue(prep_image('./images/delete_logo.png')))

    deck_state.calc_pages[14] = format_image(prep_image('./images/enter_logo.png'))
    deck_state.calc_red_pages[14] = format_image(apply_red_hue(prep_image('./images/enter_logo.png')))

    deck_state.calc_pages[3] = format_image(create_text_overlay('./images/black_square.png', "Enter Weight:", font_path='OpenSans-ExtraBold.ttf', font_color='#60acf7', font_y_offset=6))

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

from PIL import Image, ImageDraw, ImageFont

def split_text(text, font, max_width, draw):
    """
    Splits the text into lines, each of which is shorter than max_width.
    """
    words = text.split()
    lines = []
    current_line = []

    for word in words:
        # Check width with the current line plus the new word
        test_line = ' '.join(current_line + [word])
        test_width, _ = draw.textsize(test_line, font=font)
        if test_width <= max_width:
            current_line.append(word)
        else:
            # Commit the current line and start a new one
            lines.append(' '.join(current_line))
            current_line = [word]

    # Add the last line
    lines.append(' '.join(current_line))
    return lines

def create_text_overlay(image_path, text_to_overlay, font_path="./Copyduck.ttf", font_size=18, font_color='white', font_y_offset=0, subtext=None, subtext_font_size=12, subtext_font_color='white', apply_red_hue=False):
    try:
        base_image = Image.open(image_path)
    except FileNotFoundError:
        print("Error: The specified image file was not found.")
        return None
    except IOError:
        print("Error: There was an issue opening the image file. The file may be corrupted or in an unsupported format.")
        return None

    overlay_image = Image.new("RGBA", base_image.size, (255, 255, 255, 0))  # Create a transparent overlay
    draw = ImageDraw.Draw(overlay_image)
    font = ImageFont.truetype(font_path, font_size)

    lines = split_text(text_to_overlay, font, base_image.width - 20, draw)
    positions = calculate_text_position(draw, overlay_image, lines, font, font_y_offset)

    for (text_x, text_y), line in zip(positions, lines):
        draw.text((text_x, text_y), line, font=font, fill=font_color)

    if subtext:
        sub_font = ImageFont.truetype(font_path, subtext_font_size)
        subtext_width, subtext_height = draw.textsize(subtext, font=sub_font)
        subtext_x = (base_image.width - subtext_width) / 2
        subtext_y = text_y + 25
        draw.text((subtext_x, subtext_y), subtext, fill=subtext_font_color, font=sub_font)

    base_image.paste(overlay_image, (0, 0), overlay_image)

    resized_image = PILHelper.create_scaled_image(deck_state.deck, base_image, margins=[0,0,0,0])
    return resized_image

def calculate_text_position(draw, image, lines, font, y_offset=0):
    '''
    Calculate the position for the text to be centered on the image, adjusted for multiple lines.
    '''
    total_height = sum(draw.textsize(line, font=font)[1] for line in lines) + 10 * (len(lines) - 1)  # Add spacing between lines
    text_y = (image.height - total_height) / 2 - y_offset

    positions = []
    for line in lines:
        text_width, text_height = draw.textsize(line, font=font)
        text_x = (image.width - text_width) / 2
        positions.append((text_x, text_y))
        text_y += text_height + 5  # Move to the next line position with some spacing

    return positions



