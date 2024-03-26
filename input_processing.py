from SingletonDeckState import SingletonDeckState
from page_handler import idle_screen, display_page, next_page, prev_page, page_update, display_row
from pre_image_processing import pages, red_pages, black_square, page_0_row_1
import time, threading, os, psutil

deck_state = SingletonDeckState()

def print_memory_usage():
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    # Convert bytes to megabytes
    memory_used = memory_info.rss / 1024 / 1024
    print(f"Memory used: {memory_used:.2f} MB")

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

def time_waiting(key):
    # Simulate a long-running task with a loop
    time.sleep(1.5)
    
    # Once the task is done, set process_input back to True
    deck_state.deck.set_key_image(key, pages[deck_state.current_page][key])
    deck_state.process_input = True

def key_helper(key):
    if key == 4 or key == 9 or pages[deck_state.current_page][key] == black_square:
        return
    elif deck_state.current_page == 0 and key == 8:
        deck_state.current_row = (deck_state.current_row + 1) % (len(page_0_row_1) - 1)
        page_update()
        display_row()
    else:
        deck_state.deck.set_key_image(key, red_pages[deck_state.current_page][key])
        deck_state.process_input = False
        
        threading.Thread(target=time_waiting, args=(key,)).start()
    return