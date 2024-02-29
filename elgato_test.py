import random
import time
from PIL import Image, ImageDraw, ImageFont
from StreamDeck.DeviceManager import DeviceManager
from StreamDeck.ImageHelpers import PILHelper

# global array to keep track of the state of the buttons for page 0
button_states = [False for _ in range(15)]

# global array to keep track of the icons of the buttons for each page
pages = [[None for _ in range(15)] for _ in range(3)]

# global variables to keep track of the current page number
global current_page
current_page = 0

def create_num_image(deck, number):
    '''
    Create an image with the specified number centered on it.
    '''
    background_color = "white"
    text_color = "black"
    
    # Specify the path to custom font and the font size
    font_path = "/home/user/CapstoneProject/elgato/Copyduck.ttf"  
    font_size = 40  # Adjust the size as needed
    font = ImageFont.truetype(font_path, font_size)

    # Use the size from `deck.key_image_format()`
    image = Image.new("RGB", deck.key_image_format()['size'], background_color)
    draw = ImageDraw.Draw(image)

    text = str(number)

    # Calculate the size of the text
    # text_width, text_height = font.getsize(text)

    # Calculate the position for the text to be centered
    text_x = (image.width - 40) / 2
    text_y = (image.height - 35) / 2

    # Draw the text with the calculated position
    draw.text((text_x, text_y), text, fill=text_color, font=font)

    return PILHelper.to_native_format(deck, image)

# global array to keep simon says sequence
global sequence
sequence = []

def generate_sequence(deck, length):
    '''
    Generate a new sequence of numbers for the Simon Says game.
    '''
    global sequence
    # Check if we need to start a new sequence
    if length == 1:
        # Generate a new sequence from scratch
        sequence = random.sample([0, 1, 2, 3, 5, 6, 7, 8, 10, 11, 12, 13], length)
    else:
        # Append a new number to the existing sequence
        # Ensure the new number is not already in the sequence
        new_number = random.choice([0, 1, 2, 3, 5, 6, 7, 8, 10, 11, 12, 13])
        sequence.append(new_number)

def flash_button(deck, button_number, flash_count=4, interval=0.25):
    '''
    Flash the button with a random color.
    '''
    global red_square
    for _ in range(flash_count):
        random_color_setter(deck, button_number)
        time.sleep(interval)
        deck.set_key_image(button_number, white_square)  # Use image1 (or any "success" image) to flash
        time.sleep(interval)
    # Reset the button to its number image
    deck.set_key_image(button_number, pages[current_page][button_number])

global user_turn
user_turn = False

def random_color_setter(deck, key):
    '''
    Set the key image to a random color.
    '''
    global red_square
    global green_square
    global blue_square
    global yellow_square
    rand_choice = random.choice([red_square, green_square, blue_square, yellow_square])
    deck.set_key_image(key, rand_choice)

def simon_says(deck, key=0):
    '''
    Function to play the Simon Says game.
    '''
    global current_index
    global sequence
    global user_turn
    if not user_turn:
        current_index = 0  # Ensure the sequence starts from the beginning
        for number in sequence: # display the new sequence
            random_color_setter(deck, number)
            time.sleep(0.5)
            deck.set_key_image(number, white_square)
            time.sleep(0.2)
        user_turn = True # switch to user turn
    else:
        check_sequence(deck, key)

def check_sequence(deck, key):
    '''
    Check if the user's input matches the current sequence.
    '''
    global current_index
    global sequence
    global user_turn
    if key == sequence[current_index]:
        if current_index < len(sequence) - 1:
            current_index += 1
        else:
            # Provide positive feedback to the user
            print("Correct sequence! Generating new sequence.")
            flash_button(deck, sequence[current_index], 8, 0.1)
            current_index = 0
            generate_sequence(deck, len(sequence) + 1)
            user_turn = False  # Ensure user_turn is reset before starting the next sequence
            time.sleep(1)  # Give a short delay before starting the next sequence
            deck.set_key_image(14, create_num_image(deck, len(sequence))) # display current score on button 14
            simon_says(deck)
    else:
        # Provide negative feedback to the user
        flash_button(deck, sequence[current_index])
        print("Wrong button! Game over.")
        generate_sequence(deck, 1)
        user_turn = False  # Reset user_turn to start the sequence display
        time.sleep(0.5)  # Give a short delay before restarting the game
        deck.set_key_image(14, start_button)
        
    
def key_function(deck, key):
    '''
    Function to change the state of the button when pressed for page 0.
    '''
    global button_states
    global full_logo
    global num_icon_array
    global current_page
    if not button_states[key]:
        deck.set_key_image(key, full_logo)
        button_states[key] = True
        pages[current_page][key] = full_logo

    else:
        deck.set_key_image(key, num_icon_array[key])
        button_states[key] = False
        pages[current_page][key] = num_icon_array[key]

def key_change_callback(deck, key, state):
    '''
    Callback function for when a key is pressed.
    '''
    global current_page
    if state:
        print(f"Button {key} pressed")
        if key == 4:
            current_page = (current_page + 1) % 3
            display_page(deck)
            print(f"Current page: {current_page}\n")

        elif key == 9:
            current_page = (current_page - 1) % 3
            display_page(deck)
            print(f"Current page: {current_page}\n")

        elif current_page == 2:
            if key != 14:
                random_color_setter(deck, key)
            simon_says(deck, key)
        
        elif current_page == 0:
            key_function(deck, key)

    else:
        if current_page == 2 and key != 4 and key != 9 and key != 14:
            deck.set_key_image(key, white_square)


# Function to prep image for buton display. 
def prep_image(file_path, streamdeck):
    '''
    Function to prepare an image to be displayed on the StreamDeck.
    '''
    image = Image.open(file_path)
    resized_image = PILHelper.create_scaled_image(streamdeck, image, margins=[0,0,0,0])
    return PILHelper.to_native_format(streamdeck, resized_image)

logo_filenames = ['/home/user/CapstoneProject/elgato/cut_logo/image_part_001.jpg', '/home/user/CapstoneProject/elgato/cut_logo/image_part_002.jpg', 
                  '/home/user/CapstoneProject/elgato/cut_logo/image_part_003.jpg', '/home/user/CapstoneProject/elgato/cut_logo/image_part_004.jpg',
                  '/home/user/CapstoneProject/elgato/cut_logo/image_part_005.jpg', '/home/user/CapstoneProject/elgato/cut_logo/image_part_006.jpg', 
                  '/home/user/CapstoneProject/elgato/cut_logo/image_part_007.jpg', '/home/user/CapstoneProject/elgato/cut_logo/image_part_008.jpg',
                  '/home/user/CapstoneProject/elgato/cut_logo/image_part_009.jpg', '/home/user/CapstoneProject/elgato/cut_logo/image_part_010.jpg',
                  '/home/user/CapstoneProject/elgato/cut_logo/image_part_011.jpg', '/home/user/CapstoneProject/elgato/cut_logo/image_part_012.jpg', 
                  '/home/user/CapstoneProject/elgato/cut_logo/image_part_013.jpg', '/home/user/CapstoneProject/elgato/cut_logo/image_part_014.jpg', 
                  '/home/user/CapstoneProject/elgato/cut_logo/image_part_015.jpg']
            
def page_helper(deck):
    '''
    Function to set the initial images for each page.
    '''
    global next_image
    global prev_image
    global red_square 
    global white_square
    global start_button

    for i in range(15):
        deck.set_key_image(i, white_square)

    for i in range(15):
        for j in range(3):
            if j == 1:
                pages[j][i] = prep_image(logo_filenames[i], deck)
            elif i == 4:
                pages[j][i] = next_image
            elif i == 9:
                pages[j][i] = prev_image
            else:
                if j == 2:
                    if i == 14:
                        pages[j][i] = start_button
                    else:
                        pages[j][i] = white_square
                else:
                    pages[j][i] = create_num_image(deck, i)


def display_page(deck):
    '''
    Function to display the current page.
    '''
    global current_page
    for i in range(15):
        deck.set_key_image(i, pages[current_page][i])
     
def setup_images(deck):
    '''
    Function to setup the images for the program.
    '''
    global image1
    global image2
    global white_square
    global red_square
    global green_square
    global blue_square
    global yellow_square
    global next_image
    global prev_image
    global start_button
    global full_logo

    image1 = prep_image('/home/user/CapstoneProject/elgato/thumbs_up.png', deck)
    image2 = prep_image('/home/user/CapstoneProject/elgato/thumbs_down.png', deck)
    white_square = prep_image('/home/user/CapstoneProject/elgato/white_square.jpg', deck)
    red_square = prep_image('/home/user/CapstoneProject/elgato/Solid_red.svg.png', deck)
    green_square = prep_image('/home/user/CapstoneProject/elgato/green_square.png', deck)
    blue_square = prep_image('/home/user/CapstoneProject/elgato/blue_square.jpeg', deck)
    yellow_square = prep_image('/home/user/CapstoneProject/elgato/yellow_square.jpg', deck)
    next_image = prep_image('/home/user/CapstoneProject/elgato/next_icon.png', deck)
    prev_image = prep_image('/home/user/CapstoneProject/elgato/prev_icon.png', deck)
    start_button = prep_image('/home/user/CapstoneProject/elgato/start_icon.png', deck)
    full_logo = prep_image('/home/user/CapstoneProject/elgato/full_logo.png', deck)



def main():
    # connect to streamdeck
    streamdecks = DeviceManager().enumerate()
    if not streamdecks:
        print("Streamdeck not found")
        return
    
    deck = streamdecks[0]
    deck.open()
    
    try:
        # Everytime a key is pressed the function 'key_change_callback' is called
        deck.set_key_callback(key_change_callback)
        generate_sequence(deck, 1)
        
        global num_icon_array
        num_icon_array = [create_num_image(deck, i) for i in range(15)]

        setup_images(deck)
        
        page_helper(deck)

        display_page(deck)

        # infinite loop to keep the program running
        while True:
            pass

    except KeyboardInterrupt:
        pass

    finally:
        
        deck.close()

if __name__ == "__main__":
    main()