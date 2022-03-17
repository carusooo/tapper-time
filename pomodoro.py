#!/usr/bin/python
# -*- coding:utf-8 -*-
import json
import logging
import os
import sys
import threading
import time

from TP_lib import gt1151
from TP_lib import epd2in13_V2
import app

fontdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'font')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')

if os.path.exists(libdir):
    sys.path.append(libdir)

logging.basicConfig(level=logging.DEBUG)
touch_flag = 1

def pthread_irq() :
    logging.info("pthread running")
    while touch_flag == 1 :
        if gt.digital_read(gt.INT) == 0:
            GT_Dev.Touch = 1
        else :
            GT_Dev.Touch = 0
    logging.info("thread:exit")

def update_display(display, image, count):
    if count == 5:
        display.init(epd.FULL_UPDATE)
        display.displayPartBaseImage(display.getbuffer(image))
        display.init(epd.PART_UPDATE)
        count = 0
    else:
        display.displayPartial(display.getbuffer(image))
    return count + 1

try:
    logging.info("Starting tasks fetch")

    api_data = None
    with open('api_config.json') as f:
        api_data = json.load(f)

    epd = epd2in13_V2.EPD_2IN13_V2()
    gt = gt1151.GT1151()
    GT_Dev = gt1151.GT_Development()
    GT_Old = gt1151.GT_Development()

    logging.info("init and Clear")
    epd.init(epd.FULL_UPDATE)
    gt.GT_Init()
    epd.Clear(0xFF)

    t = threading.Thread(target = pthread_irq)
    t.setDaemon(True)
    t.start()

    app = app.Application(api_data['api_key'], api_data['project_id'])
    screen = app.start()

    epd.displayPartBaseImage(epd.getbuffer(screen))
    epd.init(epd.PART_UPDATE)

    updates = 0

    while 1:
        if app.redraw: # Reading the redraw value will reset it
            screen = app.draw()
            updates = update_display(epd, screen, updates)
            print("*** Redraw Refresh ***\r\n")
            continue
        # Read the touch input
        gt.GT_Scan(GT_Dev, GT_Old)
        if(GT_Old.X[0] == GT_Dev.X[0]
           and GT_Old.Y[0] == GT_Dev.Y[0]
           and GT_Old.S[0] == GT_Dev.S[0]):
            continue

        if not GT_Dev.TouchpointFlag:
            continue

        GT_Dev.TouchpointFlag = 0
        screen = app.handle_click(GT_Dev)
        updates = update_display(epd, screen, updates)
        epd.displayPartial(epd.getbuffer(screen))

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    touch_flag = 0
    epd.sleep()
    time.sleep(2)
    t.join()
    epd.Dev_exit()
    exit()
