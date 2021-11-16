import pyautogui
import time
import subprocess
def test():
    subprocess.call(("touch", 'testing_transcript.md'))
    subprocess.call(("open", 'testing_transcript.md'))
    time.sleep(30)
    # add_minute_markers.main(testing=True)
    # can only do if threading...
    with open("words.txt", "r") as fin:
        text = fin.readlines()
    while True:
        for word in text:
            pyautogui.typewrite(word.strip() + " ")

test()