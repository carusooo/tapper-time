# Tapper Time

Tapper time is a touchscren Pomodoro for use with Raspberry Pi and eInk display

This code makes a touchscreen eInk to-do list and pomodoro timer for your desk.

<img src="https://user-images.githubusercontent.com/33580338/158860069-fe996b13-2fff-48f5-9eaa-e757386be1f4.png" width="400">
<img src="https://user-images.githubusercontent.com/33580338/158860118-8ff35251-7bee-4518-8ef2-91c402b4fb0d.png" width="400">


## User Flow 

1. Enter your to-do list in a list making app (like [Todoist](todoist.com))
1. Set up the Raspberry Pi with your credentials and to-do list ID
1. Scroll through your to-do list and select an item
1. The Pomodoro timer will count down
1. When the timer is finished, you can mark the task as done or not 


## Hardware 

This project uses the [eInk touchscreen with case](https://www.waveshare.com/product/displays/e-paper/epaper-3/2.13inch-touch-e-paper-hat-with-case.htm) and a Raspberry Pi Zero WH.

The drivers and demo are available from [Waveshare](https://github.com/waveshare/Touch_e-Paper_HAT).

## Setup 


### Set Up the Raspberry Pi

Run the following steps on the Raspberry Pi
1. Create a fresh SD Card image with Raspbian Lite
1. Name the Raspberry Pi `pomodoro`
1. Log in to the terminal on the Rasbperry Pi
1. Using `raspi-config`, enable SPI and I2C  
1. Install pip3
```bash
sudo apt-get install libopenjp2-7
sudo apt-get update && sudo apt-get install python3-pip
```

### Install TapperTime on your Raspberry Pi

1. Pull the code to your host machine
1. Make a copy of `example_api_config.json` and rename it to `api_config.json`
1. Add your API token and todoist project ID
1. Copy the files to your Raspberry Pi
```bash
rsync -a --mkpath --exclude-from=.rsync-exclude.txt . pi@pomodoro.local:~/pomodoro
```

### Install TapperTime on your Raspberry Pi

1. Install the specific dependencies
``` bash
cd /home/pi/pomodoro
pip3 install -r requirements.txt
```
1. Install TapperTime as a service 
```bash
sudo cp pomodoro.service /etc/systemd/system/pomodoro.service
sudo chmod 644 /etc/systemd/system/pomodoro.service
```

1. Test that the service works 
```bash
sudo systemctl start pomodoro
sudo systemctl status pomodoro
```

## Software

This project uses the Todoist API to retrieve and close tasks. You can set up the task source to point to other todo list apps, like Google Tasks, although authentication becomes more challenging.

All of the image drawing is handled by [Pillow](https://github.com/python-pillow/Pillow).

### Developing 

Sync the source files to the Raspberry Pi using `rsync`. 

NOTE: This assumes that your Raspberry Pi is on your network as `pomodoro.local`

```bash
rsync -a --exclude-from=.rsync-exclude.txt . pi@pomodoro.local:~/pomodoro
```
