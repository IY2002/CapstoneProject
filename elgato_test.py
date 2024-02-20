from PIL import Image, ImageDraw, ImageFont
from StreamDeck.DeviceManager import DeviceManager
from StreamDeck.ImageHelpers import PILHelper

button_states = [False for _ in range(15)]

# Creates an image with `number` on a white background.
def create_num_image(deck, number):
    background_color = "white"
    text_color = "black"
    font = ImageFont.load_default()

    image = Image.new("RGB", deck.key_image_format()['size'], background_color)
    draw = ImageDraw.Draw(image)

    text = str(number)
    text_x = (image.width ) / 2
    text_y = (image.height ) / 2

    draw.text((text_x, text_y), text, fill=text_color, font=font)

    return PILHelper.to_native_format(deck, image)

# Function that is called everytime a button is pressed. Alternates buttton image between thumbs up and thumbs down. 
def key_change_callback(deck, key, state):
    global button_states
    global image1
    global image2
    if state:
        print (f"Botton {key} pressed")

        if not button_states[key]:
            deck.set_key_image(key, image1)
            button_states[key] = True
        else:
            deck.set_key_image(key, image2)
            button_states[key] = False

# Function to prep image for buton display. 
def prep_image(file_path, streamdeck):
    image = Image.open(file_path)
    resized_image = PILHelper.create_scaled_image(streamdeck, image, margins=[0,0,0,0])
    return PILHelper.to_native_format(streamdeck, resized_image)

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

        # Preload load button images and save them as global variables.
        # Makes the elgato less laggy when working if the images are preprocessed. 
        image1_path = '/home/user/elgato/thumbs_up.png'
        global image1
        image1 = prep_image(image1_path, deck)

        image2_path = '/home/user/elgato/thumbs_down.png'
        global image2
        image2 = prep_image(image2_path, deck)
        
        # Display each button with an image with the button number on it
        for i in range(deck.key_count()):
            num_image = create_num_image(deck, i)
            deck.set_key_image(i, num_image)
        
        # infinite loop to keep the program running
        while True:
            pass

    except KeyboardInterrupt:
        pass

    finally:
        
        deck.close()

if __name__ == "__main__":
    main()