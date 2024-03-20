from SingletonDeckState import SingletonDeckState
from pre_image_processing import page_0_row_1, red_page_0_row_1, pages, red_pages
import time, threading, os, psutil

deck_state = SingletonDeckState()

def print_memory_usage():
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    # Convert bytes to megabytes
    memory_used = memory_info.rss / 1024 / 1024
    print(f"Memory used: {memory_used:.2f} MB")

def page_update():
    global pages
    global red_pages

    for i in range(3):
        pages[0][i+5] = page_0_row_1[deck_state.current_row][i]
        red_pages[0][i+5] = red_page_0_row_1[deck_state.current_row][i]

def display_page():
    '''
    Function to display a page on the StreamDeck.
    '''
    page_update()

    for i in range(15):
        deck_state.deck.set_key_image(i, pages[deck_state.current_page][i])

def next_page():
    '''
    Function to move to the next page on the StreamDeck.
    '''
    deck_state.current_page = (deck_state.current_page + 1) % 2
    display_page()

def prev_page():
    '''
    Function to move to the previous page on the StreamDeck.
    '''
    deck_state.current_page = (deck_state.current_page - 1) % 2
    display_page()

def display_row():
    for i in range(4):
        deck_state.deck.set_key_image(i+5, pages[deck_state.current_page][i+5])

def key_change_callback(deck, key, state):
    '''
    Function to handle key presses on the StreamDeck.
    '''
    if state and deck_state.process_input:
        if key == 4 and deck_state.current_page != 2:
            next_page()
        elif key == 9 and deck_state.current_page != 2:
            prev_page()
        elif key == 14 and deck_state.current_page != 2:
            idle_screen()
        elif key == 14:
            deck_state.current_page = 0
            display_page()
        elif deck_state.current_page == 2:
            return
        else:
            key_helper(key)

def idle_screen():
    '''
    Function to display the idle screen on the StreamDeck.
    '''
    deck_state.current_page = 2
    display_page()

def time_waiting(key):
    # Simulate a long-running task with a loop
    time.sleep(3)
    
    # Once the task is done, set process_input back to True
    deck_state.deck.set_key_image(key, pages[deck_state.current_page][key])
    deck_state.process_input = True

def key_helper(key):
    if key == 4 or key == 9:
        return
    elif deck_state.current_page == 0 and key == 8:
        deck_state.current_row = (deck_state.current_row + 1) % 3
        page_update()
        display_row()
    else:
        deck_state.deck.set_key_image(key, red_pages[deck_state.current_page][key])
        deck_state.process_input = False
        
        threading.Thread(target=time_waiting, args=(key,)).start()
    return