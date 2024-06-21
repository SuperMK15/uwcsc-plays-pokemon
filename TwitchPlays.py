import concurrent.futures
import random
import keyboard
import pydirectinput
import pyautogui
import TwitchPlays_Connection
from TwitchPlays_KeyCodes import *

##################### GAME VARIABLES #####################

TWITCH_CHANNEL = 'uwcsclub'
BUTTON_DOWN_TIME = 0.25

##################### MESSAGE QUEUE VARIABLES #####################

MESSAGE_RATE = 0.1
MAX_QUEUE_LENGTH = 20
MAX_WORKERS = 100

last_time = time.time()
message_queue = []
thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS)
active_tasks = []
pyautogui.FAILSAFE = False

##########################################################

countdown = 5
while countdown > 0:
    print(countdown)
    countdown -= 1
    time.sleep(1)

t = TwitchPlays_Connection.Twitch()
t.twitch_connect(TWITCH_CHANNEL)

def handle_message(message):
    try:
        msg = message['message'].lower()
        username = message['username'].lower()

        print("Got this message from " + username + ": " + msg)

        # Use the "HoldKey(KEYCODE)" function to permanently press and hold down a key.
        # Use the "ReleaseKey(KEYCODE)" function to release a specific keyboard key.
        # Use the "HoldAndReleaseKey(KEYCODE, SECONDS)" function press down a key for X seconds, then release it.
        # Use the pydirectinput library to press or move the mouse



        if msg == "up" or msg == "u": 
            HoldAndReleaseKey(W, BUTTON_DOWN_TIME)

        if msg == "down" or msg == "d": 
            HoldAndReleaseKey(S, BUTTON_DOWN_TIME)
        
        if msg == "left" or msg == "l":
            HoldAndReleaseKey(A, BUTTON_DOWN_TIME)
        
        if msg == "right" or msg == "r":
            HoldAndReleaseKey(D, BUTTON_DOWN_TIME)

        if msg == "shift":
            HoldAndReleaseKey(LEFT_SHIFT, BUTTON_DOWN_TIME)

        if msg == "menu":
            HoldAndReleaseKey(ENTER, BUTTON_DOWN_TIME)

        if msg == "select" or msg == "a":
            HoldAndReleaseKey(X, BUTTON_DOWN_TIME)

        if msg == "back" or msg == "b":
            HoldAndReleaseKey(Z, BUTTON_DOWN_TIME)

        ####################################
        ####################################

    except Exception as e:
        print("Encountered exception: " + str(e))


while True:

    active_tasks = [t for t in active_tasks if not t.done()]

    #Check for new messages
    new_messages = t.twitch_receive_messages();
    if new_messages:
        message_queue += new_messages; # New messages are added to the back of the queue
        message_queue = message_queue[-MAX_QUEUE_LENGTH:] # Shorten the queue to only the most recent X messages

    messages_to_handle = []
    if not message_queue:
        # No messages in the queue
        last_time = time.time()
    else:
        # Determine how many messages we should handle now
        r = 1 if MESSAGE_RATE == 0 else (time.time() - last_time) / MESSAGE_RATE
        n = int(r * len(message_queue))
        if n > 0:
            # Pop the messages we want off the front of the queue
            messages_to_handle = message_queue[0:n]
            del message_queue[0:n]
            last_time = time.time();

    # If user presses Shift+Backspace, automatically end the program
    if keyboard.is_pressed('shift+backspace'):
        exit()

    if not messages_to_handle:
        continue
    else:
        for message in messages_to_handle:
            if len(active_tasks) <= MAX_WORKERS:
                active_tasks.append(thread_pool.submit(handle_message, message))
            else:
                print(f'WARNING: active tasks ({len(active_tasks)}) exceeds number of workers ({MAX_WORKERS}). ({len(message_queue)} messages in the queue)')
 