"""Automatically insert minute markers in my interview notes during the interview.

Prior attempts:
- original inserting attempt was with pyautogui.typewrite() but this
  inserted the marker character by character, split if I was typing.
  I was not able to get pyautogui.hotkey("command", "v") to work (like
  many testified on the web)
- original timing attempt was with time.sleep() in a while loop but promises
  seemed rough.

Reference:

After my PyAutoGui struggles I attempted Automator, and successfully found how
to paste, but couldn't identify how to run from terminal. Then realized I could
run an AppleScript.
- g[automater paste]:
=> https://stackoverflow.com/questions/25747253/applescript-to-paste-clipboard
- then g[run automater quick action from terminal]
  and g[run appscript from terminal]:
=> https://support.apple.com/lt-lt/guide/terminal/trml1003/mac

Then for timing:
- g[print on exactly on the iminute python]:
=> https://stackoverflow.com/questions/19645720/trigger-a-python-function-exactly-on-the-minute


I may need to learn to have it trigger on the minute but on the second on which it was triggered.
OK. I think it is with the current second.

g[sched.add_job(fn, trigger=CronTrigger(second=00))]
=> https://apscheduler.readthedocs.io/en/3.x/modules/triggers/cron.html

Then I played w/ this in Python:
>>> from datetime import datetime
>>> help(datetime.now())

>>> datetime.now().second
32


WEIRD FAIL STATE: the script provides a Space while the AppleScript has command
down. That opens Finder and then various window switching as I frantically try
to return to the terminal to end.

I could simply not test it that way, but I is also possible that I'd press a
space at the minute marker as well, throwing off an interview.

I realized this paradigm is perhaps overwrought and I can instead write a
listener that reconstructs the notes, not intervening directly in the creation.

"""

# Imports
import sys
import subprocess
from datetime import datetime

import pyperclip

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

# Body
MINUTE = 0
TESTING = False


def set_marker_sched(start_second):
    sched = BlockingScheduler()
    # Execute fn() at the start of each minute.
    sched.add_job(fn, trigger=CronTrigger(second=start_second))
    sched.start()


def fn():
    global MINUTE
    pyperclip.copy("\n# {}:00\n\n".format(MINUTE))
    subprocess.call(("osascript", "paste.scpt"))
    if TESTING:
        pyperclip.copy(str(datetime.now()))
        subprocess.call(("osascript", "paste.scpt"))
    MINUTE += 1


def main(testing=False):
    if (sys.argv[-1] == "-t") or (testing is True):
        print("Testing add_minute_markers...")
        global TESTING
        TESTING = True
    print("Running add_minute_markers...")
    set_marker_sched(datetime.now().second)

if __name__ == "__main__":
    main()