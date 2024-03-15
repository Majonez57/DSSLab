import time
from pynput import keyboard

name = 'labels2'

def on_press(key):
    try:
        if key.char in key_mappings:
            message = key_mappings[key.char]
            timestamp = time.time()
            log_message = f"{timestamp},{message}\n"
            with open(f"Labels/{name}.txt", "a") as file:
                file.write(log_message)
                print(f"Logged: {log_message.strip()}")

    except AttributeError:
        # Ignore key presses that are not characters
        pass

def on_release(key):
    if key == keyboard.Key.enter:
        # Stop listener
        return False

key_mappings = {
    'q': "hi-weak",
    'w': "hi-mid",
    'e': "hi-strong",
    'a': "mid-weak",
    's': "mid-mid",
    'd': "mid-strong",
    'z': "lo-weak",
    'x': "lo-mid",
    'c': "lo-strong"
}

def main():
    print("Press keys to log messages, press Enter to finish.")
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    print("Logging finished. See 'key_log.txt' for the log.")

if __name__ == "__main__":
    main()
