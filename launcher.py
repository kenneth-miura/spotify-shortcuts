from pynput.keyboard import Key, Listener
from pynput import keyboard
from spotify_controller import SpotifyController

current_pressed = set()
controller = SpotifyController()
# Combinations must match format of [modifier, action key].
PREVIOUS_SONG_COMBINATION = [
    [keyboard.Key.alt_l, keyboard.KeyCode(char=',')],
    [keyboard.Key.alt_r, keyboard.KeyCode(char=',')]
]
NEXT_SONG_COMBINATION = [
    [keyboard.Key.alt_l, keyboard.KeyCode(char='.')],
    [keyboard.Key.alt_r, keyboard.KeyCode(char='.')]
]
REMOVE_SONG_COMBINATION = [
    [keyboard.Key.alt_l, keyboard.KeyCode(char='/')],
    [keyboard.Key.alt_r, keyboard.KeyCode(char='/')]
]

ALL_COMBINATIONS = [PREVIOUS_SONG_COMBINATION,
                    NEXT_SONG_COMBINATION, REMOVE_SONG_COMBINATION]
ACTION_KEYS = []
ACTION_KEY_INDEX = 1
for i in range(len(ALL_COMBINATIONS)):
    # assumes the combination lists indices have identical action keys
    ACTION_KEYS.append(ALL_COMBINATIONS[i][0][ACTION_KEY_INDEX])

# meant to keep from running multiple commands at once
spotify_command_running = False


def combination_pressed(desired_combination):
    if any(all(k in current_pressed for k in COMBO) for COMBO in desired_combination):
        return True
    return False


def on_press(key):
    global spotify_command_running
    for SHORTCUT_COMBINATIONS in ALL_COMBINATIONS:
        if any([key in COMBO for COMBO in SHORTCUT_COMBINATIONS]):
            current_pressed.add(key)
            if not spotify_command_running:
                if combination_pressed(PREVIOUS_SONG_COMBINATION):
                    controller.previous_track()
                    spotify_command_running = True

                if combination_pressed(NEXT_SONG_COMBINATION):
                    controller.next_track()
                    spotify_command_running = True

                if combination_pressed(REMOVE_SONG_COMBINATION):
                    controller.remove_current_track()
                    spotify_command_running = True


def on_release(key):
    global spotify_command_running
    try:
        if key in ACTION_KEYS:
            spotify_command_running = False
        current_pressed.remove(key)
    except KeyError:
        pass
    if key == Key.esc:
        return False


with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
