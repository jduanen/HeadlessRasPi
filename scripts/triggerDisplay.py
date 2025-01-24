#!/usr/bin/env python3
# -*- coding: utf-8 -*-
################################################################################
#
# Script that will trigger the information display when a button is pushed
#
################################################################################

from gpiozero import Button
import logging
import platform
import psutil
import subprocess
from time import sleep


LOG_LEVEL = "DEBUG"  # "WARNING"


def isRunning(progName):
    return any(progName in p.name().lower() for p in psutil.process_iter())

def runScript():
    if isRunning(systemDisplay.py):
        logging.debug("systemDisplay.py running, waiting")
        sleep(1)

    logging.debug("Starting systemDisplay.py")
    subprocess.run(["${HOME}/Code/HeadlessRasPi/src/systemDisplay.py"])
    logging.debug("systemDisplay.py done")


if __name__ == "__main__":
    logging.basicConfig(level=LOG_LEVEL)

    button = Button(20, pull_up=True, hold_time=30)
    button.when_held = runScript
    logging.debug("Polling for display button")
    while True:
        sleep(10)
