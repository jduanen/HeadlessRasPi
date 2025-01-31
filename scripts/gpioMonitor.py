#!/usr/bin/env python3
# -*- coding: utf-8 -*-
################################################################################
#
# Script that will trigger the information display when a button is pushed
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
import subprocess

import gpiod
from gpiod.line import Bias, Direction, Edge, Value


PIN_NUMBER = 20
LOG_LEVEL = "WARNING"
PROG_PATH = "/home/jdn/Code/HeadlessRasPi/scripts/gpioTrigger.sh"


if __name__ == "__main__":
    logging.basicConfig(level=LOG_LEVEL)

    logging.debug("get request")
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
            logging.debug("Wait for event")
            for lineEvent in rqst.read_edge_events():
                logging.debug(f"Got event: {lineEvent}")
                if lineEvent.event_type == lineEvent.Type.FALLING_EDGE:
                    logging.debug(f"Line {PIN_NUMBER} Falling Edge @ {lineEvent.timestamp_ns}: calling script")
                    subprocess.run([PROG_PATH])
    except KeyboardInterrupt:
        logging.debug("Exiting")
    finally:
        rqst.release()
