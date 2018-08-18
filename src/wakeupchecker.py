import sys
import os
import configparser
from gpiozero import LED
import datetime
import logging

def get_configuration(cfg_file):
    if not os.path.isfile(cfg_file):
        logging.error("Config file %s not found" % cfg_file)
        sys.exit(1)
    config = configparser.ConfigParser()
    config.read(cfg_file)
    return config

def set_leds(led_config):
    green_led_ind = int(led_config["green_led"])
    red_led_ind = int(led_config["red_led"])
    green_led = LED(green_led_ind)
    green_led.off()
    red_led = LED(red_led_ind)
    red_led.off()
    return green_led, red_led

def get_time(time_str):
    time_data = time_str.split(":")
    hour = int(time_data[0])
    minute = int(time_data[1])
    return datetime.time(hour, minute)

def get_times(time_config):
    start_time = get_time(time_config["start_time"])
    wakeup_time = get_time(time_config["wakeup_time"])
    end_time = get_time(time_config["end_time"])
    return start_time, wakeup_time, end_time

def get_calculated_time(time_obj):
    calculated = (datetime.datetime.combine(datetime.date(1, 1, 1), time_obj) - datetime.timedelta(minutes=1)).time()
    return calculated

if __name__ == "__main__":
    logging.basicConfig(filename="wakeup.log", filemode="w", format='%(asctime)s %(message)s', level=logging.INFO)
    config = get_configuration(sys.argv[1])
    green_led, red_led = set_leds(config["leds"])
    start_time, wakeup_time, end_time = get_times(config["wakeup"])
    calculated_start_time = get_calculated_time(start_time)
    calculated_end_time = get_calculated_time(end_time)
    calculated_wakeup_time = get_calculated_time(wakeup_time)
    has_started = False
    has_woken = False
    while True:
        current = datetime.datetime.now().time()
        if (end_time > current and calculated_end_time < current) and has_started and has_woken:
            logging.info("shutting off")
            green_led.off()
            red_led.off()
            has_woken = False
            has_started = False
        elif (wakeup_time > current and calculated_wakeup_time < current) and has_started and not has_woken:
            logging.info("waking")
            green_led.on()
            red_led.off()
            has_woken = True
        elif (start_time > current and calculated_start_time < current) and not has_started:
            logging.info("delaying")
            red_led.on()
            green_led.off()
            has_started = True