""" Red led is set on when given time set from configuration is met.
    After red led the green led is set on when given time from configuration is met.
    Both leds are set off when given time from configuration is met.
"""
import sys
import os
import configparser
import datetime
import logging
from gpiozero import LED

def get_configuration(cfg_file):
    """ Returns configuration
    System exit 1 if configuration file is not found on filesystem
    """
    if not os.path.isfile(cfg_file):
        logging.error("Config file %s not found", cfg_file)
        sys.exit(1)
    cfg = configparser.ConfigParser()
    cfg.read(cfg_file)
    return cfg

def set_leds(led_config):
    """ Returns red and green led based on given led configuration
    """
    green_led_ind = int(led_config["green_led"])
    red_led_ind = int(led_config["red_led"])
    gled = LED(green_led_ind)
    gled.off()
    rled = LED(red_led_ind)
    rled.off()
    return gled, rled

def get_time(time_str):
    """ Returns datetime time object from given strimg
    String needs to be in format hours:minutes
    e.g. "12:00"
    """
    time_data = time_str.split(":")
    hour = int(time_data[0])
    minute = int(time_data[1])
    return datetime.time(hour, minute)

def get_times(time_config):
    """ Returns start, wakeup and end times
    as datetime time objects
    """
    stime = get_time(time_config["start_time"])
    wtime = get_time(time_config["wakeup_time"])
    etime = get_time(time_config["end_time"])
    return stime, wtime, etime

def get_calculated_time(time_obj):
    """ Returns given datetime time object with minus 1 minute
    """
    calculated = (datetime.datetime.combine(
        datetime.date(1, 1, 1), time_obj) - datetime.timedelta(minutes=1)).time()
    return calculated

def light_leds(current_time, time_container, r_led, g_led, flags):
    """ Sets green led and red led on and off depending on given times versus current time
    """
    e_time = time_container["end_time"]
    s_time = time_container["start_time"]
    w_time = time_container["wakeup_time"]
    if get_calculated_time(e_time) < current_time < e_time and \
       flags["has_started"] and flags["has_woken"]:
        logging.info("shutting off")
        g_led.off()
        r_led.off()
        flags["has_started"] = False
        flags["has_woken"] = False
    elif get_calculated_time(w_time) < current_time < w_time and \
        flags["has_started"] and not flags["has_woken"]:
        logging.info("waking")
        g_led.on()
        r_led.off()
        flags["has_woken"] = True
    elif get_calculated_time(s_time) < current_time < s_time and \
        not flags["has_started"] and not flags["has_woken"]:
        logging.info("delaying")
        r_led.on()
        g_led.off()
        flags["has_started"] = True

if __name__ == "__main__":
    logging.basicConfig(filename="wakeup.log", filemode="w",
                        format='%(asctime)s %(message)s', level=logging.INFO)
    CONFIG = get_configuration(sys.argv[1])
    GREEN_LED, RED_LED = set_leds(CONFIG["leds"])
    START_TIME, WAKEUP_TIME, END_TIME = get_times(CONFIG["wakeup"])
    TIME_CONTAINER = {
        "start_time": START_TIME,
        "end_time": END_TIME,
        "wakeup_time": WAKEUP_TIME
    }
    FLAGS = {
        "has_started": False,
        "has_woken": False
    }
    while True:
        CURRENT = datetime.datetime.now().time()
        light_leds(CURRENT, TIME_CONTAINER, RED_LED, GREEN_LED, FLAGS)
