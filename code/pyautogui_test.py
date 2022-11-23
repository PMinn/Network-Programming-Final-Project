import pyautogui


def press(): # zh is ok
    pyautogui.keyDown('a')

def holdShift():
    with pyautogui.hold('shift'):
        pyautogui.press(['left', 'left', 'left'])

pyautogui.keyDown('shift')  # hold down the shift key
pyautogui.press('up')     # press the a arrow key
pyautogui.press('a')     # press the a arrow key
pyautogui.press('a')     # press the left arrow keyAA
pyautogui.keyUp('shift')    # release the shift key