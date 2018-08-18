import unittest
import mock
from src.wakeupchecker import get_configuration, set_leds, get_time, get_times, get_calculated_time, light_leds
import os
import configparser
import datetime
class TestWakeupchecker(unittest.TestCase):
    valid_config = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "valid.cfg")

    @mock.patch('src.wakeupchecker.logging.error')
    def test_get_configuration_with_invalid_file(self, mock_logging_error):
        self.assertFalse(mock_logging_error.called)
        self.assertRaises(SystemExit, get_configuration, "file_does_not_exists")
        self.assertTrue(mock_logging_error.called)
    
    def test_get_configuration_with_valid_file(self):
        config = get_configuration(self.valid_config)
        self.assertTrue(isinstance(config, configparser.ConfigParser))
        self.assertTrue(config.has_section("leds"))
        self.assertTrue(config.has_section("wakeup"))
    
    @mock.patch('src.wakeupchecker.LED.off')
    def test_set_leds(self, mock_led_off):
        config = get_configuration(self.valid_config)
        red_led, green_led = set_leds(config["leds"])
        self.assertEqual(red_led.pin.number, 23)
        self.assertEqual(green_led.pin.number, 24)
        red_led.off.assert_called()
        green_led.off.assert_called()
    
    def test_get_time(self):
        expected = datetime.time(5, 50)
        observed = get_time("05:50")
        self.assertEqual(observed, expected)
    
    @mock.patch('src.wakeupchecker.get_time')
    def test_get_times(self, mock_get_time):
        config = get_configuration(self.valid_config)
        expected = [mock.call('06:50'), mock.call('06:55'), mock.call('12:00')]
        start_time, wakeup_time, end_time = get_times(config["wakeup"])
        self.assertEquals(mock_get_time.call_args_list, expected)
    
    def test_get_calculated_time(self):
        expected = datetime.time(6, 49)
        data = datetime.time(6, 50)
        observed = get_calculated_time(data)
        self.assertEquals(observed, expected)


    def test_light_leds(self):
        end_time = datetime.time(5, 10)
        calculated_end_time = get_calculated_time(end_time)
        start_time = datetime.time(5, 0)
        calculated_start_time = get_calculated_time(start_time)
        wakeup_time = datetime.time(5, 2)
        calculated_wakeup_time = get_calculated_time(wakeup_time)
        current = datetime.time(5, 9, 2)
        green_led = mock.MagicMock()
        red_led = mock.MagicMock()
        light_leds(current, end_time, calculated_end_time, start_time, calculated_start_time, wakeup_time, calculated_wakeup_time, green_led, red_led, True, True)
        self.assertTrue(green_led.off.called and red_led.off.called)
        current = datetime.time(5, 1, 2)
        light_leds(current, end_time, calculated_end_time, start_time, calculated_start_time, wakeup_time, calculated_wakeup_time, green_led, red_led, False, True)
        self.assertTrue(green_led.on.called and red_led.off.called)
        current = datetime.time(4, 59, 1)
        light_leds(current, end_time, calculated_end_time, start_time, calculated_start_time, wakeup_time, calculated_wakeup_time, green_led, red_led, False, False)
        self.assertTrue(green_led.off.called, red_led.on.called)
