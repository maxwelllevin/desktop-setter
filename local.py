import os
import sys
import time
import ctypes
import platform
import datetime as dt
from subprocess import Popen, PIPE, call



# Global settings
screen_width = 2560
screen_height = 1600


def set_background(filename):
    """
    Sets the desktop background.
    """
    if platform.system() == "Darwin":
        # Applescript:
        cmd = f'/usr/bin/osascript<<END\ntell application "Finder"\nset desktop picture to POSIX file "{filename}"\nend tell\nEND'
        Popen(cmd, shell=True)
        call(["killall Dock"], shell=True)
        return
    if platform.system() == "Windows":
        ctypes.windll.user32.SystemParametersInfoW(20, 0, filename, 0)
        return


def loop(folder, interval):
    """
    Collects .jpg files from the folder and calls 'set_background' once every interval.
    """
    files = os.listdir(folder)
    images = list(filter(lambda file: file[-4:] == ".jpg", files))
    if images is None or len(images) == 0:
        print(f"No .jpg images found in {folder}")
        return
    i = 0
    while i < len(images):
        img = os.path.abspath(os.path.join(folder, images[i]))
        set_background(img)
        print(f"Set {images[i]} as background image at {str(dt.datetime.now())}")
        time.sleep(60 * interval)
        i += 1
        i = i % len(images)


def print_instructions():
    """
    Prints instructions for how to use the program. 
    """
    print("This script takes two parameters:")
    print("1. The path to the folder you want to grab images from. (Can be relative or absolute)")
    print("2. The number of minutes you want to wait before changing backgrounds again.")
    print()
    print("EX: python3 local.py images/ 60")
    print("EX: python3 local.py /Users/maxwelllevin/Pictures/California/ 0.5")
    print()


if __name__ == "__main__":
    if len(sys.argv) < 3: 
        print_instructions()
        exit(0)
    image_folder = sys.argv[1]
    loop_interval = float(sys.argv[2])
    loop(image_folder, loop_interval)


.
