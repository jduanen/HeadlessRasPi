#!/usr/bin/env python3
# -*- coding: utf-8 -*-
################################################################################
#
# Script for a service (i.e., infoDisplay) that will trigger the information
#  display when a button is pushed.
#
# N.B. documentation for gpiod: https://github.com/brgl/libgpiod/tree/master
#      and https://github.com/brgl/libgpiod/tree/master/bindings/python
#
# LineSettings(
#    direction: gpiod.line.Direction = <Direction.AS_IS: 1>,
#    edge_detection: gpiod.line.Edge = <Edge.NONE: 1>,
#    bias: gpiod.line.Bias = <Bias.AS_IS: 1>,
#    drive: gpiod.line.Drive = <Drive.PUSH_PULL: 1>,
#    active_low: bool = False,
#    debounce_period: datetime.timedelta = datetime.timedelta(0),
#    event_clock: gpiod.line.Clock = <Clock.MONOTONIC: 1>,
#    output_value: gpiod.line.Value = <Value.INACTIVE: 0>) -> None
#
################################################################################

from datetime import timedelta
import logging
import platform
import psutil
import subprocess
from time import sleep

import gpiod
from gpiod.line import Bias, Direction, Edge, Value


LOG_LEVEL = "WARNING"
PIN_NUMBER = 20
PROG_PATH = "/home/jdn/Code/HeadlessRasPi/src/infoDisplay.py"


logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger(__name__)


def getRunningProgramsArg(progName, arg1):
    return {p.pid: p.cmdline() for p in psutil.process_iter() if (p.name() == progName) and (len(p.cmdline()) > 1) and (p.cmdline()[1].endswith(arg1))}

def runScript():
    while getRunningProgramsArg("python3", "infoDisplay.py"):
        logger.debug("infoDisplay.py running, waiting...")
        sleep(1)

    logger.debug("Starting infoDisplay.py")
    subprocess.run([PROG_PATH])
    logger.debug("infoDisplay.py done")

def main():
    logger.debug("get request")
    rqst = gpiod.request_lines(
        "/dev/gpiochip0",
        consumer="gpioMonitor",
        config={PIN_NUMBER: gpiod.LineSettings(
                direction=Direction.INPUT,
                bias=Bias.PULL_UP,
                edge_detection=Edge.FALLING,
                debounce_period=timedelta(milliseconds=10)
            )
        }
    )

    try:
        while True:
            logger.debug("Wait for event")
            for lineEvent in rqst.read_edge_events():
                logger.debug(f"Got event: {lineEvent}")
                if lineEvent.event_type == lineEvent.Type.FALLING_EDGE:
                    logger.debug(f"Line {PIN_NUMBER} Falling Edge @ {lineEvent.timestamp_ns}: calling script")
                    runScript()
    except KeyboardInterrupt:
        logger.debug("Exiting")
    except Exception as ex:
        logger.error(f"Exiting: {ex}")
    finally:
        rqst.release()

if __name__ == "__main__":
    main()
