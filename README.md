# RPIWakeup
Sets LEDs on/off based on [configuration file](https://github.com/Atihinen/RPIwakeup/blob/master/unittests/data/valid.cfg)

Example:

start_time is set to 7:00 and red led pin is 23, then red led is set on at 6:59.
wakeup_time is set to 7:30 and green led pin is 24, then red led is set off at 7:29 and green led is set on at 7:29.
end_time is set to 8:30 and then both leds are set of at 8:29.

## Requirements

### Hardware

* Raspberry PI x (doesn't really matter which one as long as you can connect to GPIO pins)
* SD card
* 2 x LED (e.g. green and red)
* 4 x jumper cables (2 goes to ground and 2 goes to pins)
* 2 x resistors
* Rasbian or something else distro that supports python3
* (optional, but really recommended) network access (wifi/lan) in order to keep the clock in sync

### Software

* python3
* python3-pip
* git


## Setuo

* install needed dependencies and setup cables
* git clone this repository
* run `pip3 install -r requirements.txt` inside cloned repository
* run `nohup python3 src/wakeupchecker.py <config_file_path> &` in order to start running the process (to kill run `kill -2 <pid>`)

### Protip
* you might want to set that nohup command so that it'll be run always when machine boots up


# Development

## Static code analysis

Run command `pylint src`

## Unittests

Run command `nosetests --with-coverage unittests`

## Static dependencies security check

Run command `safety -r requirements`