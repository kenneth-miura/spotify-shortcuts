from pynput.keyboard import Key, Listener
from pynput import keyboard

current = set()
PREVIOUS_SONG_COMBINATION = [
    {keyboard.Key.alt_l, keyboard.KeyCode(char=',')},
    {keyboard.Key.alt_r, keyboard.KeyCode(char=',')}
]
NEXT_SONG_COMBINATION = [
    {keyboard.Key.alt_l, keyboard.KeyCode(char='.')},
    {keyboard.Key.alt_r, keyboard.KeyCode(char='.')}
]
PAUSE_SONG_COMBINATION = [
    {keyboard.Key.alt_l, keyboard.KeyCode(char='/')},
    {keyboard.Key.alt_r, keyboard.KeyCode(char='/')}
]

ALL_COMBINATIONS = [PREVIOUS_SONG_COMBINATION,
                    NEXT_SONG_COMBINATION, PAUSE_SONG_COMBINATION]


def combination_pressed(desired_combination):
    if any(all(k in current for k in COMBO) for COMBO in desired_combination):
        return True
    return False


def on_press(key):
    for SHORTCUT_COMBINATIONS in ALL_COMBINATIONS:
        if any([key in COMBO for COMBO in SHORTCUT_COMBINATIONS]):
            current.add(key)
            if combination_pressed(PREVIOUS_SONG_COMBINATION):
                print("prev song")
            if combination_pressed(NEXT_SONG_COMBINATION):
                print("next song")
            if combination_pressed(PAUSE_SONG_COMBINATION):
                print("pause song")


def on_release(key):
    try:
        current.remove(key)
    except KeyError:
        pass
    if key == Key.esc:
        return False


with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
