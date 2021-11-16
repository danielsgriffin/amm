"""Automatically insert minute markers from listening in my interview notes
during the interview.

Prior attempts:
- original inserting attempt was with pyautogui.typewrite() but this
  inserted the marker character by character, split if I was typing.
  I was not able to get pyautogui.hotkey("command", "v") to work (like
  many testified on the web)
- original timing attempt was with time.sleep() in a while loop but promises
  seemed rough.



"""

# Imports
from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

# Body
TEMP_NOTES = "temp_notes.md"
LIVE_NOTES = "/Users/dsg/Desktop/nidicolous/testing_transcript.md"
NOTES_BY_MINUTE = []


def set_marker_sched(start_second):
    """Establish schedule with the second the script was initiated."""
    sched = BlockingScheduler()
    # Execute listener_fn() every minute on the start_second.
    sched.add_job(listener_fn, trigger=CronTrigger(second=start_second))
    sched.start()


def update_temp_notes():
    """Update TEMP_NOTES file from NOTES_MINUTES."""
    with open(TEMP_NOTES, "r") as fin:
        temp_text = fin.read()
    # base text is pre-interview
    temp_text += NOTES_BY_MINUTE[-1]
    temp_text += "\n\n# {}:00\n\n".format(len(NOTES_BY_MINUTE)-1)
    with open(TEMP_NOTES, "w") as fout:
        fout.write(temp_text)


def listener_fn():
    """Copy all text from notes up to exact minute.

    - reads NOTES_FILE
    - updates NOTES_BY_MINUTE list
    - calls update_temp_notes
    """
    with open(LIVE_NOTES, "r") as fin:
        text = fin.read()
    # append only the text not already logged
    if len(NOTES_BY_MINUTE) > 1:
        NOTES_BY_MINUTE.append(text.strip(NOTES_BY_MINUTE[-1]))
    else:
        NOTES_BY_MINUTE.append(text)
    update_temp_notes()


def main():
    """Prints initializing statement, starts schedule, runs base listener."""
    print("Running add_minute_markers...")
    print("Listening to:", LIVE_NOTES)
    print("TEMP_NOTES:\n", TEMP_NOTES)
    set_marker_sched(datetime.now().second)
    listener_fn()


if __name__ == "__main__":
    main()