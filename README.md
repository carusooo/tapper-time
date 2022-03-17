Touchscren Pomodoro for use with Raspberry Pi and eInk display

This code makes a touchscreen eInk to-do list and pomodoro timer for your desk.

## Usage 

1. Enter your to-do list in a list making app (like [Todoist](todoist.com))
1. Set up the Raspberry Pi with your credentials and to-do list ID
1. Scroll through your to-do list and select an item
1. The Pomodoro timer will count down
1. When the timer is finished, you can mark the task as done or not 


## Hardware 

This project uses the [eInk touchscreen with case](https://www.waveshare.com/product/displays/e-paper/epaper-3/2.13inch-touch-e-paper-hat-with-case.htm) and a Raspberry Pi Zero WH.

The drivers and demo are available from [Waveshare](https://github.com/waveshare/Touch_e-Paper_HAT).

## Software

This project uses the Todoist API to retrieve and close tasks. You can set up the task source to point to other todo list apps, like Google Tasks, although authentication becomes more challenging.

All of the image drawing is handled by [Pillow](https://github.com/python-pillow/Pillow).

