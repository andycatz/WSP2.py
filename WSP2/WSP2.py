# Weather Station Program 2
# (C)2022 Andy Page
# Version 1     17th July 2022
# With direct LoRa receiver.

from tkinter import *
from datetime import datetime
from ExtTRH import ExtTRH
from UV_Light import UV_Light
from Sferic import Sferic
from Rainfall import Rainfall
from Wind import Wind
from Base import Base
import math
from Logger import Logger
from WindChill import *
from ApparentTemp import ApparentTemp
from HeatIndex import HeatIndex
from time import sleep
from SX127x.LoRa import *
from SX127x.LoRaArgumentParser import LoRaArgumentParser
from SX127x.board_config import BOARD
from LoRaRcvCont import *
from CRC16 import CRC16
from Web_Parser import Web_Parser
from Units import Units
from WSP2_FTP import WSP2_FTP
from Info import Info
from TimeAndSpace import TimeAndSpace

busy_processing = False
close_requested = False

BOARD.setup()

parser = LoRaArgumentParser("Continuous LoRa receiver.")
lora = LoRaRcvCont(verbose=False)

degree_sign = u'\N{DEGREE SIGN}'
temp_angle = 0

counter = 0
one_minute = 12  # When counter gets to this, one minute has elapsed

# Base sensor
base_sensor = Base()

# External temp/RH sensor
trh_sensor = ExtTRH()

# Visible and UV light sensor
uvl_sensor = UV_Light()

# Sferic sensor
sferic_sensor = Sferic()

# Rainfall sensor
rainfall_sensor = Rainfall()

# Wind sensor
wind_sensor = Wind()

wind_chill_sensor = WindChill()  # A virtual wind chill sensor (value derived from other sensors)

app_temp_sensor = ApparentTemp()  # A virtual apparent temperature sensor (value derived from other sensors)

heat_index_sensor = HeatIndex()  # A virtual heat index sensor (value derived from other sensors)

logger = Logger(trh_sensor, uvl_sensor, sferic_sensor, rainfall_sensor, wind_sensor, base_sensor, wind_chill_sensor,
                app_temp_sensor, heat_index_sensor)

crc16_calculator = CRC16()

units = Units()

web_parser = Web_Parser(units, trh_sensor, uvl_sensor, sferic_sensor, rainfall_sensor, wind_sensor, base_sensor,
                        wind_chill_sensor, app_temp_sensor, heat_index_sensor)

wsp2_ftp = WSP2_FTP()

info = Info()

ts = TimeAndSpace()


def decode_data(list_of_data, snr, rssi):
    # Need to check CRC16 before allowing data to be processed since sometimes the messages have errors.
    crc_16 = crc16_calculator.crc16_modbus(list_of_data)

    # print("CRC16: ", hex(crc_16))

    if crc_16 == 0:
        # print("CRC OK")
        if list_of_data[0] == 0x32:
            # print("Valid data from a sensor")
            if list_of_data[1] == 0x00:
                if list_of_data[2] == 0x01:
                    # print("Rain sensor")
                    rainfall_sensor.receive_message(list_of_data, snr, rssi)
                    rainfall_sensor.update()
                elif list_of_data[2] == 0x02:
                    # print("UVL Sensor")
                    uvl_sensor.receive_message(list_of_data, snr, rssi)
                    uvl_sensor.update()
                elif list_of_data[2] == 0x03:
                    # print("TRH Sensor")
                    trh_sensor.receive_message(list_of_data, snr, rssi)
                    trh_sensor.update()
                elif list_of_data[2] == 0x06:
                    # print("SF Sensor")
                    sferic_sensor.receive_message(list_of_data, snr, rssi)
                    sferic_sensor.update()
                elif list_of_data[2] == 0x08:
                    # print("Wind Sensor")
                    wind_sensor.receive_message(list_of_data, snr, rssi)
                    wind_sensor.update()
            else:
                print("Invalid message")
        else:
            print("Invalid message/CRC error")
    else:
        print("CRC ERROR")


# Do various calculations of weather values
def do_calculations():
    do_wind_chill()
    do_apparent_temp()
    do_heat_index()
    do_feels_like_temp()


# Do wind chill calculations
def do_wind_chill():
    vkmh = wind_sensor.get_wind_speed_kmh()
    v_valid = wind_sensor.rx  # Check if a valid wind speed value has been recently received
    ta = trh_sensor.temp_c
    t_valid = trh_sensor.rx  # Check if a valid outside temperature value has been recently received
    if v_valid > 0 and t_valid > 0:
        wc = wind_chill_sensor.calculate_wind_chill(ta, vkmh)
        wind_chill_sensor.wind_chill = wc
        wind_chill_sensor.wind_chill_valid = 1  # A valid wind chill value has been calculated
        wind_chill_sensor.check_min_wind_chill()
    else:
        wind_chill_sensor.wind_chill_valid = 0  # Wind chill value is now not valid


# Do apparent temperature calculations
def do_apparent_temp():
    # print("Doing app temp ")
    vms = wind_sensor.get_wind_speed_ms()
    v_valid = wind_sensor.rx  # Check if a valid wind speed value has been recently received
    ta = trh_sensor.temp_c
    t_valid = trh_sensor.rx  # Check if a valid outside temperature value has been recently received
    rh = trh_sensor.rh
    if v_valid > 0 and t_valid > 0:
        # print("Values valid for app temp calculation. ")
        at = app_temp_sensor.calculate_app_temp(ta, vms, rh)
        app_temp_sensor.app_temp = at  # Set apparent temperature value
        app_temp_sensor.app_temp_valid = 1  # Apparent temperature value is valid
        app_temp_sensor.check_max_min()
        # print("App Temp ", app_temp_sensor.app_temp)

    else:
        # print("Values not valid for app temp calculation. ")
        app_temp_sensor.app_temp_valid = 0  # Apparent temperature value is not valid


# Do "feels like" temperature calculations
def do_feels_like_temp():
    # print("Doing app temp ")
    vms = wind_sensor.get_wind_speed_ms()
    v_valid = wind_sensor.rx  # Check if a valid wind speed value has been recently received
    ta = trh_sensor.temp_c
    t_valid = trh_sensor.rx  # Check if a valid outside temperature value has been recently received
    rh = trh_sensor.rh
    at = app_temp_sensor.app_temp
    atv = app_temp_sensor.app_temp_valid
    if v_valid > 0 and t_valid > 0:
        # print("Values valid for feels like temp calculation. ")
        if ta <= 10:
            fl = app_temp_sensor.calculate_feels_like_temp(ta, vms, rh)
        elif ta >= 20:
            if atv > 0:
                fl = at
            else:
                fl = ta
        else:
            fl = ta
        app_temp_sensor.feels_like = fl  # Set feels like temperature value
        app_temp_sensor.feels_like_valid = 1  # Feels like temperature value is valid
        app_temp_sensor.check_max_min()

    else:
        # print("Values not valid for feels like temp calculation. ")
        app_temp_sensor.feels_like_valid = 0  # Apparent temperature value is not valid


# Do heat index calculations
def do_heat_index():
    # print("Doing heat index ")
    tc = trh_sensor.temp_c
    # print("Temp in Celsius ", tc)
    rh = trh_sensor.rh
    # print("RH ", rh)
    valid = trh_sensor.rx
    if valid > 0:
        hi = heat_index_sensor.calculate_heat_index_C(tc, rh)
        heat_index_sensor.heat_index_C = hi
        heat_index_sensor.heat_index_valid = 1
        heat_index_sensor.check_max_min()
        # print("Heat index ", hi, " C")
        hi_string = heat_index_sensor.get_heat_index_warning(hi)
        # print("Heat index warning level: ", hi_string)
    else:
        heat_index_sensor.heat_index_valid = 0


# Dummy function to call as a placeholder
def do_nothing():
    pass


def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x - r, y - r, x + r, y + r, **kwargs)


Canvas.create_circle = _create_circle


def _create_circle_arc(self, x, y, r, **kwargs):
    if "start" in kwargs and "end" in kwargs:
        kwargs["extent"] = kwargs["end"] - kwargs["start"]
        del kwargs["end"]
    return self.create_arc(x - r, y - r, x + r, y + r, **kwargs)


Canvas.create_circle_arc = _create_circle_arc


# Requests that each sensor store a set of data
def store_data():
    # print("Storing data...\r\n")
    trh_sensor.add_data()
    base_sensor.add_data()
    uvl_sensor.add_data()
    sferic_sensor.add_data()
    rainfall_sensor.add_data()
    wind_sensor.add_data()


def make_plot_files():
    trh_sensor.draw_ext_temp_graph(True, info.extTemp24hr_filename)
    trh_sensor.draw_ext_rh_graph(True, info.extRH24hr_filename)
    base_sensor.draw_pressure_graph(True, info.press24hr_filename)
    rainfall_sensor.draw_24hr_rainfall_graph(True, info.rain24hr_filename)
    rainfall_sensor.draw_24hr_rainrate_graph(True, info.rainrate24hr_filename)
    uvl_sensor.draw_vis_graph(True, info.vis24hr_filename)
    uvl_sensor.draw_uv_graph(True, info.uv24hr_filename)
    wind_sensor.draw_wind_graph(True, info.wind24hr_filename)
    wind_sensor.draw_dir_graph(True, info.dir24hr_filename)
    base_sensor.draw_temp_graph(True, info.intTemp24hr_filename)
    base_sensor.draw_rh_graph(True, info.intRH24hr_filename)


def do_stuff_every_so_often():
    global temp_angle, counter, one_minute, old_minute, old_day, temp_rh, wsg_x, wsg_y, p_length, temp_value, busy_processing
    if not close_requested:
        busy_processing = True
        time_now = datetime.datetime.now()
        current_time = time_now.strftime("%H:%M:%S")
        # print(current_time)
        update_canvas_time(c, current_time)
        base_sensor.get_data()
        base_sensor.update()
        if lora.new_data > 0:
            # print("New data available:")
            data_list = lora.get_data()
            snr = lora.get_snr()
            rssi = lora.get_rssi()
            """
            for x in data_list:
                print(hex(x) , end = " ")
                print(",", end = " ")
            print(" ")
            """
            decode_data(data_list, snr, rssi)

        # Do these things every 5 seconds
        if time_now.second % 5 == 0:

            do_calculations()

            pts = calculate_points_for_compass_dir(comp_x, comp_y, p_length, wind_sensor.direction)
            ext_temp_points = calculate_points_for_temp_gauge(extt_x, extt_y, p_length, trh_sensor.temp_c)
            int_temp_points = calculate_points_for_temp_gauge(intt_x, intt_y, p_length, base_sensor.temp_c)
            ext_rh_points = calculate_points_for_rh_gauge(extrh_x, extrh_y, p_length, trh_sensor.rh)
            int_rh_points = calculate_points_for_rh_gauge(intrh_x, intrh_y, p_length, base_sensor.rh)
            pressure_points = calculate_points_for_pressure_gauge(pr_x, pr_y, p_length, base_sensor.sea_level_pressure)
            gust_points = calculate_points_for_wind_speed(wsg_x, wsg_y, p_length, wind_sensor.gust)
            speed_points = calculate_points_for_wind_speed(wsg_x, wsg_y, p_length, wind_sensor.speed)
            vis_points = calculate_points_for_vis_gauge(visg_x, visg_y, p_length, uvl_sensor.visible)
            uvindex_points = calculate_points_for_uvindex_gauge(uvig_x, uvig_y, p_length, uvl_sensor.uv_index)
            rainrate_points = calculate_points_for_rainrate_gauge(rrg_x, rrg_y, p_length, rainfall_sensor.rain_rate)
            rain_points = calculate_points_for_rainrate_gauge(rng_x, rng_y, p_length, rainfall_sensor.rain_mm)
            prr_points = calculate_points_for_pressure_rate_gauge(prr_x, prr_y, p_length, base_sensor.pressure_rate)
            sf_points = calculate_points_for_sferic_gauge(sf_x, sf_y, p_length, sferic_sensor.get_average_count())
            sfr_points = calculate_points_for_sferic_gauge(sfr_x, sfr_y, p_length, sferic_sensor.get_average_rate())

            update_canvas_extt_gauge(c, str(round(trh_sensor.temp_c, 1)) + degree_sign + "C", ext_temp_points)
            update_canvas_compass(c, str(wind_sensor.direction) + degree_sign, pts)
            update_canvas_rh_gauge(c, str(round(trh_sensor.rh, 1)) + "%", ext_rh_points)
            update_canvas_pressure_gauge(c, str(round(base_sensor.sea_level_pressure, 1)) + "hPa", pressure_points)
            update_canvas_wind_speed_gauge(c, str(round(wind_sensor.gust, 1)) + "MPH", gust_points,
                                           str(round(wind_sensor.speed, 1)) + "MPH", speed_points)
            update_canvas_vis_gauge(c, str(round(uvl_sensor.visible, 1)) + "lux", vis_points)
            update_canvas_uvindex_gauge(c, str(round(uvl_sensor.uv_index, 1)), uvindex_points)
            update_canvas_rain_gauge(c, str(round(rainfall_sensor.rain_mm, 1)) + "mm", rain_points)
            update_canvas_rainrate_gauge(c, str(round(rainfall_sensor.rain_rate, 1)) + "mm/hr", rainrate_points)
            update_canvas_intt_gauge(c, str(round(base_sensor.temp_c, 1)) + degree_sign + "C", int_temp_points)
            update_canvas_int_rh_gauge(c, str(round(base_sensor.rh, 1)) + "%", int_rh_points)
            update_canvas_pressure_rate_gauge(c, str(round(base_sensor.pressure_rate, 1)) + "hPa/hr", prr_points)
            update_canvas_sferic_gauge(c, str(round(sferic_sensor.get_average_count(), 0)) + " strikes", sf_points)
            update_canvas_sferic_rate_gauge(c, str(round(sferic_sensor.get_average_rate(), 1)) + " str/hr", sfr_points)

            av_temp_value_text.set(str(round(trh_sensor.av_temp, 1)) + degree_sign + "C")

            if app_temp_sensor.app_temp_valid > 0:
                at_value_text.set(str(round(app_temp_sensor.app_temp, 1)) + degree_sign + "C")
            else:
                at_value_text.set("---")

            if wind_chill_sensor.wind_chill_valid > 0:
                wc_value_text.set(str(round(wind_chill_sensor.wind_chill, 1)) + degree_sign + "C")
            else:
                wc_value_text.set("---")

            if heat_index_sensor.heat_index_valid > 0:
                hi_value_text.set(str(round(heat_index_sensor.heat_index_C, 1)) + degree_sign + "C")
            else:
                hi_value_text.set("---")

        if time_now.minute != old_minute:
            # print("New minute")
            store_data()
            old_minute = time_now.minute
            counter = 0
            logger.save_minute_log()
            # Create graph files
            make_plot_files()
            # Update the web files
            web_parser.populate_web_tags()
            web_parser.parse_file()
            wsp2_ftp.do_ftp()
            # print("Av temp ", trh_sensor.av_temp)

        if time_now.day != old_day:
            logger.save_day_log()
            # print("New day")
            base_sensor.reset_max_min()
            trh_sensor.reset_max_min()
            wind_sensor.reset_max_min()
            rainfall_sensor.reset_max_min()
            sferic_sensor.reset_today_counts()
            wind_chill_sensor.reset_min_wind_chill()
            app_temp_sensor.reset_max_min()
            heat_index_sensor.reset_max_min()
            old_day = time_now.day
        busy_processing = False
        window.after(500, do_stuff_every_so_often)
    else:
        print("Destroying GUI")
        print("Goodbye!")
        BOARD.teardown()
        try:
            window.destroy()
        except:
            exit(0)


def calculate_points_for_compass_dir(x, y, length, wind_dir):
    pointer_base_width = 10
    b = pointer_base_width / 2
    wd = 360.0 - wind_dir
    x1 = x + length * math.sin(math.radians(wd + 180))
    y1 = y + length * math.cos(math.radians(wd + 180))
    x2 = x + b * math.sin(math.radians(wd + 90))
    y2 = y + b * math.cos(math.radians(wd + 90))
    x3 = x + b * math.sin(math.radians(wd - 90))
    y3 = y + b * math.cos(math.radians(wd - 90))
    return [x1, y1, x2, y2, x3, y3]


def calculate_points_for_temp_gauge(x, y, length, temp):
    pointer_base_width = 10
    b = pointer_base_width / 2
    if temp < 15:
        angle = 225 + (temp + 20) * (135 / 35)
    else:
        angle = (temp - 15) * 135 / 35
    if temp < -20:
        angle = 225
    if temp > 50:
        angle = 135
    wd = 360.0 - angle
    x1 = x + length * math.sin(math.radians(wd + 180))
    y1 = y + length * math.cos(math.radians(wd + 180))
    x2 = x + b * math.sin(math.radians(wd + 90))
    y2 = y + b * math.cos(math.radians(wd + 90))
    x3 = x + b * math.sin(math.radians(wd - 90))
    y3 = y + b * math.cos(math.radians(wd - 90))
    return [x1, y1, x2, y2, x3, y3]


def calculate_points_for_rh_gauge(x, y, length, rh):
    pointer_base_width = 10
    b = pointer_base_width / 2
    angle = 225 - (rh / 100 * 270)
    if rh < 0:
        angle = 225
    if rh > 100:
        angle = 135
    wd = 360 - angle
    x1 = x + length * math.cos(math.radians(wd))
    y1 = y + length * math.sin(math.radians(wd))
    x2 = x + b * math.cos(math.radians(wd + 90))
    y2 = y + b * math.sin(math.radians(wd + 90))
    x3 = x + b * math.cos(math.radians(wd - 90))
    y3 = y + b * math.sin(math.radians(wd - 90))
    return [x1, y1, x2, y2, x3, y3]


# Calculate the x, y points for the triangle of the pressure rate gauge pointer
def calculate_points_for_pressure_rate_gauge(x, y, length, prate):
    pointer_base_width = 10
    b = pointer_base_width / 2
    angle = 225 - ((prate + 10) / 20 * 270)
    if prate < -10:
        angle = 225
    if prate > 10:
        angle = 135
    wd = 360 - angle
    x1 = x + length * math.cos(math.radians(wd))
    y1 = y + length * math.sin(math.radians(wd))
    x2 = x + b * math.cos(math.radians(wd + 90))
    y2 = y + b * math.sin(math.radians(wd + 90))
    x3 = x + b * math.cos(math.radians(wd - 90))
    y3 = y + b * math.sin(math.radians(wd - 90))
    return [x1, y1, x2, y2, x3, y3]


# Works for both wind speed and gust as they are on the same gauge
def calculate_points_for_wind_speed(x, y, length, speed):
    pointer_base_width = 10
    b = pointer_base_width / 2
    angle = 225 - (speed / 50 * 270)
    if speed < 0:
        angle = 225
    if speed > 50:
        angle = 135
    wd = 360 - angle
    x1 = x + length * math.cos(math.radians(wd))
    y1 = y + length * math.sin(math.radians(wd))
    x2 = x + b * math.cos(math.radians(wd + 90))
    y2 = y + b * math.sin(math.radians(wd + 90))
    x3 = x + b * math.cos(math.radians(wd - 90))
    y3 = y + b * math.sin(math.radians(wd - 90))
    return [x1, y1, x2, y2, x3, y3]


def calculate_points_for_pressure_gauge(x, y, length, p):
    pointer_base_width = 10
    b = pointer_base_width / 2
    angle = 225 - ((p - 950) / 100 * 270)
    if p < 950:
        angle = 225
    if p > 1050:
        angle = 135
    wd = 360 - angle
    x1 = x + length * math.cos(math.radians(wd))
    y1 = y + length * math.sin(math.radians(wd))
    x2 = x + b * math.cos(math.radians(wd + 90))
    y2 = y + b * math.sin(math.radians(wd + 90))
    x3 = x + b * math.cos(math.radians(wd - 90))
    y3 = y + b * math.sin(math.radians(wd - 90))
    return [x1, y1, x2, y2, x3, y3]


def calculate_points_for_vis_gauge(x, y, length, light):
    pointer_base_width = 10
    b = pointer_base_width / 2
    angle = 225 - (light / 100000 * 270)
    if light < 0:
        angle = 225
    if light > 100000:
        angle = 135
    wd = 360 - angle
    x1 = x + length * math.cos(math.radians(wd))
    y1 = y + length * math.sin(math.radians(wd))
    x2 = x + b * math.cos(math.radians(wd + 90))
    y2 = y + b * math.sin(math.radians(wd + 90))
    x3 = x + b * math.cos(math.radians(wd - 90))
    y3 = y + b * math.sin(math.radians(wd - 90))
    return [x1, y1, x2, y2, x3, y3]


# Calculation of the points that make up the UV index gauge pointer
def calculate_points_for_uvindex_gauge(x, y, length, index):
    pointer_base_width = 10
    b = pointer_base_width / 2
    angle = 225 - (index / 11 * 270)
    if index < 0:
        angle = 225
    if index > 11:
        angle = 135
    wd = 360 - angle
    x1 = x + length * math.cos(math.radians(wd))
    y1 = y + length * math.sin(math.radians(wd))
    x2 = x + b * math.cos(math.radians(wd + 90))
    y2 = y + b * math.sin(math.radians(wd + 90))
    x3 = x + b * math.cos(math.radians(wd - 90))
    y3 = y + b * math.sin(math.radians(wd - 90))
    return [x1, y1, x2, y2, x3, y3]


# Calculation of the points that make up the rain rate gauge pointer
def calculate_points_for_rainrate_gauge(x, y, length, rr):
    pointer_base_width = 10
    b = pointer_base_width / 2
    angle = 225
    if rr >= 0.1:
        angle = 157.5 - 67.5 * (1 + math.log10(rr))
    if rr > 100:
        angle = 135
    wd = 360 - angle
    x1 = x + length * math.cos(math.radians(wd))
    y1 = y + length * math.sin(math.radians(wd))
    x2 = x + b * math.cos(math.radians(wd + 90))
    y2 = y + b * math.sin(math.radians(wd + 90))
    x3 = x + b * math.cos(math.radians(wd - 90))
    y3 = y + b * math.sin(math.radians(wd - 90))
    return [x1, y1, x2, y2, x3, y3]


# Calculates points of a line on the temperature gauges
# representing a maximum or minimum
def calculate_limit_points(x, y, temp_value):
    length = 10
    if temp_value < 15:
        angle = 225 + (temp_value + 20) * (135 / 35)
    else:
        angle = (temp_value - 15) * 135 / 35
    if temp_value < -20:
        angle = 225
    if temp_value > 50:
        angle = 135
    wd = 360.0 - angle
    x1 = x + (85 - length) * math.sin(math.radians(wd + 180))
    x2 = x + 85 * math.sin(math.radians(wd + 180))
    y1 = y + (85 - length) * math.cos(math.radians(wd + 180))
    y2 = y + 85 * math.cos(math.radians(wd + 180))
    return [x1, y1, x2, y2]


# Calculates points of a line on the rh gauges
# representing a maximum or minimum
def calculate_rh_limit_points(x, y, rh_value):
    length = 10
    angle = 225 - (rh_value / 100 * 270)
    if rh_value < 0:
        angle = 225
    if rh_value > 100:
        angle = 135
    wd = angle
    x1 = x + (85 - length) * math.sin(math.radians(wd + 90))
    x2 = x + 85 * math.sin(math.radians(wd + 90))
    y1 = y + (85 - length) * math.cos(math.radians(wd + 90))
    y2 = y + 85 * math.cos(math.radians(wd + 90))

    return [x1, y1, x2, y2]


# Calculation of the points that make up the sferic gauge pointer
def calculate_points_for_sferic_gauge(x, y, length, sf):
    pointer_base_width = 10
    b = pointer_base_width / 2
    angle = 225
    if sf >= 0.1:
        angle = 157.5 - 67.5 * (1 + math.log10(sf / 100))
    if sf > 10000:
        angle = 135
    wd = 360 - angle
    x1 = x + length * math.cos(math.radians(wd))
    y1 = y + length * math.sin(math.radians(wd))
    x2 = x + b * math.cos(math.radians(wd + 90))
    y2 = y + b * math.sin(math.radians(wd + 90))
    x3 = x + b * math.cos(math.radians(wd - 90))
    y3 = y + b * math.sin(math.radians(wd - 90))
    return [x1, y1, x2, y2, x3, y3]


# Draw the wind compass at the x,y coordinates of the canvass cv
def draw_compass(x, y, cv):
    cv.create_circle(x, y, 99, outline="black", width=6)  # BBB
    cv.create_circle(x, y, 95, fill="white")
    cv.create_text(x, y - 83, fill="darkblue", font="Arial 10 bold", text="N")
    cv.create_text(x, y + 83, fill="darkblue", font="Arial 10 bold", text="S")
    cv.create_text(x + 83, y, fill="darkblue", font="Arial 10 bold", text="E")
    cv.create_text(x - 83, y, fill="darkblue", font="Arial 10 bold", text="W")
    cv.create_circle(x, y, 96, outline="darkblue", width=2)
    cv.create_circle(x, y, 8, fill="red")
    r1 = 94
    r2 = 89
    for z in range(0, 16):
        a = z * 22.5
        x1 = x + math.sin(math.radians(a)) * r1
        x2 = x + math.sin(math.radians(a)) * r2
        y1 = y + math.cos(math.radians(a)) * r1
        y2 = y + math.cos(math.radians(a)) * r2
        cv.create_line(x1, y1, x2, y2)


# Draw the temperature gauge at the x,y coordinates of the canvas cv
def draw_temp_gauge(x, y, cv, name):
    cv.create_circle(x, y, 98, outline="black", width=6)
    cv.create_circle(x, y, 96, outline="darkblue", width=2)
    cv.create_circle(x, y, 95, fill="white")
    r1 = 94
    r2 = 85
    cv.create_circle_arc(x, y, 95, start=-45, end=-6.429, fill="red", outline="red")
    cv.create_circle_arc(x, y, 95, start=-6.429, end=32.142, fill="orange", outline="orange")
    cv.create_circle_arc(x, y, 95, start=32.142, end=70.713, fill="yellow", outline="yellow")
    cv.create_circle_arc(x, y, 95, start=70.713, end=109.284, fill="green", outline="green")
    cv.create_circle_arc(x, y, 95, start=109.284, end=147.855, fill="cyan", outline="cyan")
    cv.create_circle_arc(x, y, 95, start=147.855, end=186.426, fill="blue", outline="blue")
    cv.create_circle_arc(x, y, 95, start=186.426, end=224.997, fill="magenta", outline="magenta")
    cv.create_circle(x, y, 85, fill="white", outline="white")
    cv.create_circle_arc(x, y, 85, start=224.997, end=-45, outline="darkblue", style=ARC)
    cv.create_circle(x, y, 8, fill="red")
    for z in range(0, 8):
        a = 45 + z * 38.571
        x1 = x + math.sin(math.radians(a)) * r1
        x2 = x + math.sin(math.radians(a)) * r2
        y1 = y + math.cos(math.radians(a)) * r1
        y2 = y + math.cos(math.radians(a)) * r2
        cv.create_line(x1, y1, x2, y2)
    r1 = 85
    r2 = 80
    for z in range(0, 15):
        a = 45 + z * 19.2855
        x1 = x + math.sin(math.radians(a)) * r1
        x2 = x + math.sin(math.radians(a)) * r2
        y1 = y + math.cos(math.radians(a)) * r1
        y2 = y + math.cos(math.radians(a)) * r2
        cv.create_line(x1, y1, x2, y2)
    cv.create_text(x - 48, y + 52, fill="darkblue", font="Arial 10 bold", text="-20")
    cv.create_text(x - 65, y + 8, fill="darkblue", font="Arial 10 bold", text="-10")
    cv.create_text(x - 60, y - 42, fill="darkblue", font="Arial 10 bold", text="0")
    cv.create_text(x - 23, y - 65, fill="darkblue", font="Arial 10 bold", text="10")
    cv.create_text(x + 23, y - 65, fill="darkblue", font="Arial 10 bold", text="20")
    cv.create_text(x + 60, y - 42, fill="darkblue", font="Arial 10 bold", text="30")
    cv.create_text(x + 68, y + 8, fill="darkblue", font="Arial 10 bold", text="40")
    cv.create_text(x + 48, y + 52, fill="darkblue", font="Arial 10 bold", text="50")
    cv.create_text(x, y + 70, fill="darkblue", font="Arial 10 bold", text=name)


# Draw the relative humidity gauge at the x,y coordinates of the canvas cv
def draw_rh_gauge(x, y, cv, name):
    cv.create_circle(x, y, 98, outline="black", width=6)
    cv.create_circle(x, y, 96, outline="darkblue", width=2)
    cv.create_circle(x, y, 95, fill="white")
    cv.create_circle_arc(x, y, 95, start=-45, end=-18, fill="blue", outline="blue")
    cv.create_circle_arc(x, y, 95, start=-18, end=9, fill="cyan", outline="cyan")
    cv.create_circle_arc(x, y, 95, start=9, end=117, fill="green", outline="green")
    cv.create_circle_arc(x, y, 95, start=117, end=144, fill="yellow", outline="yellow")
    cv.create_circle_arc(x, y, 95, start=144, end=171, fill="orange", outline="orange")
    cv.create_circle_arc(x, y, 95, start=171, end=198, fill="red", outline="red")
    cv.create_circle_arc(x, y, 95, start=198, end=225, fill="magenta", outline="magenta")
    cv.create_circle(x, y, 85, fill="white", outline="white")
    cv.create_circle_arc(x, y, 85, start=225, end=-45, outline="darkblue", style=ARC)
    cv.create_circle(x, y, 8, fill="red")

    r1 = 85
    r2 = 80
    for z in range(0, 11):
        a = 45 + z * 27
        x1 = x + math.sin(math.radians(a)) * r1
        x2 = x + math.sin(math.radians(a)) * r2
        y1 = y + math.cos(math.radians(a)) * r1
        y2 = y + math.cos(math.radians(a)) * r2
        cv.create_line(x1, y1, x2, y2)
    cv.create_text(x - 52, y + 52, fill="darkblue", font="Arial 10 bold", text="0")
    cv.create_text(x - 68, y + 22, fill="darkblue", font="Arial 10 bold", text="10")
    cv.create_text(x - 70, y - 12, fill="darkblue", font="Arial 10 bold", text="20")
    cv.create_text(x - 58, y - 42, fill="darkblue", font="Arial 10 bold", text="30")
    cv.create_text(x - 30, y - 65, fill="darkblue", font="Arial 10 bold", text="40")
    cv.create_text(x, y - 72, fill="darkblue", font="Arial 10 bold", text="50")
    cv.create_text(x + 30, y - 65, fill="darkblue", font="Arial 10 bold", text="60")
    cv.create_text(x + 58, y - 42, fill="darkblue", font="Arial 10 bold", text="70")
    cv.create_text(x + 70, y - 12, fill="darkblue", font="Arial 10 bold", text="80")
    cv.create_text(x + 68, y + 22, fill="darkblue", font="Arial 10 bold", text="90")
    cv.create_text(x + 46, y + 52, fill="darkblue", font="Arial 10 bold", text="100")
    cv.create_text(x, y + 70, fill="darkblue", font="Arial 10 bold", text=name)


# Draw the pressure gauge at the x,y coordinates of the canvas cv
def draw_pressure_gauge(x, y, cv, name):
    cv.create_circle(x, y, 98, outline="black", width=6)
    cv.create_circle(x, y, 96, outline="darkblue", width=2)
    cv.create_circle(x, y, 95, fill="white")
    cv.create_circle_arc(x, y, 95, start=-45, end=90, fill="green", outline="green")
    cv.create_circle_arc(x, y, 95, start=90, end=117, fill="yellow", outline="yellow")
    cv.create_circle_arc(x, y, 95, start=117, end=144, fill="orange", outline="orange")
    cv.create_circle_arc(x, y, 95, start=144, end=225, fill="red", outline="red")
    cv.create_circle(x, y, 85, fill="white", outline="white")
    cv.create_circle_arc(x, y, 85, start=225, end=-45, outline="darkblue", style=ARC)
    cv.create_circle(x, y, 8, fill="red")

    r1 = 85
    r2 = 80
    for z in range(0, 11):
        a = 45 + z * 27
        x1 = x + math.sin(math.radians(a)) * r1
        x2 = x + math.sin(math.radians(a)) * r2
        y1 = y + math.cos(math.radians(a)) * r1
        y2 = y + math.cos(math.radians(a)) * r2
        cv.create_line(x1, y1, x2, y2)
    cv.create_text(x - 52, y + 52, fill="darkblue", font="Arial 10 bold", text="950")
    cv.create_text(x - 65, y + 22, fill="darkblue", font="Arial 10 bold", text="960")
    cv.create_text(x - 67, y - 12, fill="darkblue", font="Arial 10 bold", text="970")
    cv.create_text(x - 58, y - 42, fill="darkblue", font="Arial 10 bold", text="980")
    cv.create_text(x - 30, y - 65, fill="darkblue", font="Arial 10 bold", text="990")
    cv.create_text(x, y - 72, fill="darkblue", font="Arial 10 bold", text="1000")
    cv.create_text(x + 30, y - 65, fill="darkblue", font="Arial 10 bold", text="1010")
    cv.create_text(x + 53, y - 42, fill="darkblue", font="Arial 10 bold", text="1020")
    cv.create_text(x + 65, y - 12, fill="darkblue", font="Arial 10 bold", text="1030")
    cv.create_text(x + 63, y + 22, fill="darkblue", font="Arial 10 bold", text="1040")
    cv.create_text(x + 46, y + 52, fill="darkblue", font="Arial 10 bold", text="1050")
    cv.create_text(x, y + 70, fill="darkblue", font="Arial 10 bold", text=name)


# Draw the wind speed at the x,y coordinates of the canvas cv
def draw_wind_speed_gauge(x, y, cv, name):
    cv.create_circle(x, y, 98, outline="black", width=6)
    cv.create_circle(x, y, 96, outline="darkblue", width=2)
    cv.create_circle(x, y, 95, fill="white")
    cv.create_circle_arc(x, y, 95, start=-45, end=-18, fill="red", outline="red")
    cv.create_circle_arc(x, y, 95, start=-18, end=9, fill="orange", outline="orange")
    cv.create_circle_arc(x, y, 95, start=9, end=36, fill="yellow", outline="yellow")
    cv.create_circle_arc(x, y, 95, start=36, end=225, fill="green", outline="yellow")
    cv.create_circle(x, y, 85, fill="white", outline="white")
    cv.create_circle_arc(x, y, 85, start=225, end=-45, outline="darkblue", style=ARC)
    cv.create_circle(x, y, 8, fill="red")

    r1 = 85
    r2 = 80
    for z in range(0, 11):
        a = 45 + z * 27
        x1 = x + math.sin(math.radians(a)) * r1
        x2 = x + math.sin(math.radians(a)) * r2
        y1 = y + math.cos(math.radians(a)) * r1
        y2 = y + math.cos(math.radians(a)) * r2
        cv.create_line(x1, y1, x2, y2)
    cv.create_text(x - 52, y + 52, fill="darkblue", font="Arial 10 bold", text="0")
    cv.create_text(x - 68, y + 22, fill="darkblue", font="Arial 10 bold", text="5")
    cv.create_text(x - 70, y - 12, fill="darkblue", font="Arial 10 bold", text="10")
    cv.create_text(x - 58, y - 42, fill="darkblue", font="Arial 10 bold", text="15")
    cv.create_text(x - 30, y - 65, fill="darkblue", font="Arial 10 bold", text="20")
    cv.create_text(x, y - 72, fill="darkblue", font="Arial 10 bold", text="25")
    cv.create_text(x + 30, y - 65, fill="darkblue", font="Arial 10 bold", text="30")
    cv.create_text(x + 58, y - 42, fill="darkblue", font="Arial 10 bold", text="35")
    cv.create_text(x + 70, y - 12, fill="darkblue", font="Arial 10 bold", text="40")
    cv.create_text(x + 68, y + 22, fill="darkblue", font="Arial 10 bold", text="45")
    cv.create_text(x + 46, y + 52, fill="darkblue", font="Arial 10 bold", text="50")
    cv.create_text(x, y + 70, fill="darkblue", font="Arial 10 bold", text=name)


# Draw the visible light gauge at the x,y coordinates of the canvas cv
def draw_vis_gauge(x, y, cv, name):
    cv.create_circle(x, y, 98, outline="black", width=6)
    cv.create_circle(x, y, 96, outline="darkblue", width=2)
    cv.create_circle(x, y, 95, fill="white")
    cv.create_circle_arc(x, y, 95, start=-45, end=225, fill="yellow", outline="yellow")
    cv.create_circle(x, y, 85, fill="white", outline="white")
    cv.create_circle_arc(x, y, 85, start=225, end=-45, outline="darkblue", style=ARC)
    cv.create_circle(x, y, 8, fill="red")
    r1 = 85
    r2 = 80
    for z in range(0, 11):
        a = 45 + z * 27
        x1 = x + math.sin(math.radians(a)) * r1
        x2 = x + math.sin(math.radians(a)) * r2
        y1 = y + math.cos(math.radians(a)) * r1
        y2 = y + math.cos(math.radians(a)) * r2
        cv.create_line(x1, y1, x2, y2)
    cv.create_text(x - 52, y + 52, fill="darkblue", font="Arial 10 bold", text="0")
    cv.create_text(x - 68, y + 22, fill="darkblue", font="Arial 10 bold", text="10k")
    cv.create_text(x - 70, y - 12, fill="darkblue", font="Arial 10 bold", text="20k")
    cv.create_text(x - 58, y - 42, fill="darkblue", font="Arial 10 bold", text="30k")
    cv.create_text(x - 30, y - 65, fill="darkblue", font="Arial 10 bold", text="40k")
    cv.create_text(x, y - 72, fill="darkblue", font="Arial 10 bold", text="50k")
    cv.create_text(x + 30, y - 65, fill="darkblue", font="Arial 10 bold", text="60k")
    cv.create_text(x + 58, y - 42, fill="darkblue", font="Arial 10 bold", text="70k")
    cv.create_text(x + 70, y - 12, fill="darkblue", font="Arial 10 bold", text="80k")
    cv.create_text(x + 68, y + 22, fill="darkblue", font="Arial 10 bold", text="90k")
    cv.create_text(x + 46, y + 52, fill="darkblue", font="Arial 10 bold", text="100k")
    cv.create_text(x, y + 70, fill="darkblue", font="Arial 10 bold", text=name)


# Draw the uv index gauge at the x,y coordinates of the canvas cv
def draw_uvindex_gauge(x, y, cv, name):
    cv.create_circle(x, y, 98, outline="black",
                     width=6)  # Circle is x, y, radius.  Our gauges are 200 pixels in diameter
    cv.create_circle(x, y, 96, outline="darkblue", width=2)
    cv.create_circle(x, y, 95, fill="white")
    cv.create_circle_arc(x, y, 95, start=-45, end=-20.455, fill="magenta", outline="magenta")
    cv.create_circle_arc(x, y, 95, start=-20.455, end=53.18, fill="red", outline="red")
    cv.create_circle_arc(x, y, 95, start=53.18, end=102.27, fill="orange", outline="orange")
    cv.create_circle_arc(x, y, 95, start=102.27, end=175.905, fill="yellow", outline="yellow")
    cv.create_circle_arc(x, y, 95, start=175.905, end=225, fill="green", outline="green")
    cv.create_circle(x, y, 85, fill="white", outline="white")
    cv.create_circle_arc(x, y, 85, start=225, end=-45, outline="darkblue", style=ARC)
    cv.create_circle(x, y, 8, fill="red")
    r1 = 85
    r2 = 80
    for z in range(0, 12):
        a = 45 + z * 24.545
        x1 = x + math.sin(math.radians(a)) * r1
        x2 = x + math.sin(math.radians(a)) * r2
        y1 = y + math.cos(math.radians(a)) * r1
        y2 = y + math.cos(math.radians(a)) * r2
        cv.create_line(x1, y1, x2, y2)
    cv.create_text(x - 52, y + 52, fill="darkblue", font="Arial 10 bold", text="0")
    cv.create_text(x - 68, y + 25, fill="darkblue", font="Arial 10 bold", text="1")
    cv.create_text(x - 73, y - 7, fill="darkblue", font="Arial 10 bold", text="2")
    cv.create_text(x - 63, y - 37, fill="darkblue", font="Arial 10 bold", text="3")
    cv.create_text(x - 45, y - 58, fill="darkblue", font="Arial 10 bold", text="4")
    cv.create_text(x - 15, y - 70, fill="darkblue", font="Arial 10 bold", text="5")
    cv.create_text(x + 15, y - 70, fill="darkblue", font="Arial 10 bold", text="6")
    cv.create_text(x + 45, y - 58, fill="darkblue", font="Arial 10 bold", text="7")
    cv.create_text(x + 63, y - 37, fill="darkblue", font="Arial 10 bold", text="8")
    cv.create_text(x + 73, y - 7, fill="darkblue", font="Arial 10 bold", text="9")
    cv.create_text(x + 67, y + 25, fill="darkblue", font="Arial 10 bold", text="10")
    cv.create_text(x + 50, y + 52, fill="darkblue", font="Arial 10 bold", text="11")
    cv.create_text(x, y + 70, fill="darkblue", font="Arial 10 bold", text=name)


# Draw the rain/rain rate gauge at the x,y coordinates of the canvas cv
def draw_rain_gauge(x, y, cv, name):
    cv.create_circle(x, y, 98, outline="black", width=6)
    cv.create_circle(x, y, 96, outline="darkblue", width=2)
    cv.create_circle(x, y, 95, fill="white")
    cv.create_circle_arc(x, y, 95, start=-45, end=-24.68, fill="magenta",
                         outline="magenta")  # 50-100mm/hr or 50mm to 100mm
    cv.create_circle_arc(x, y, 95, start=-24.68, end=30.545, fill="red", outline="red")  # 7.6-50mm/hr or 7.6mm to 50mm
    cv.create_circle_arc(x, y, 95, start=30.545, end=49.36, fill="orange", outline="orange")  # 4-7.5mm/hr
    cv.create_circle_arc(x, y, 95, start=49.36, end=61.989, fill="yellow", outline="yellow")  # 2.6-4mm/hr
    cv.create_circle_arc(x, y, 95, start=61.989, end=225, fill="green", outline="green")  # 0-2.5mm/hr
    cv.create_circle(x, y, 85, fill="white", outline="white")
    cv.create_circle_arc(x, y, 85, start=225, end=-45, outline="darkblue", style=ARC)
    cv.create_circle(x, y, 8, fill="red")

    r1 = 85
    r2 = 80
    # Angle is 157.5 - 67.5 * (1 + log(rainrate))
    draw_angled_line(cv, x, y, 45, r1, r2)  # 100mm/hr marker
    draw_angled_line(cv, x, y, 24.68, r1, r2)  # 50mm/hr marker
    draw_angled_line(cv, x, y, 2.18, r1, r2)  # 20mm/hr marker
    draw_angled_line(cv, x, y, -22.5, r1, r2)  # 10mm/hr marker
    draw_angled_line(cv, x, y, -42.82, r1, r2)  # 5mm/hr marker
    draw_angled_line(cv, x, y, -69.68, r1, r2)  # 2mm/hr marker
    draw_angled_line(cv, x, y, -90, r1, r2)  # 1mm/hr marker
    draw_angled_line(cv, x, y, -110.32, r1, r2)  # 0.5mm/hr
    draw_angled_line(cv, x, y, -157.5, r1, r2)  # 0.1mm/hr
    draw_angled_line(cv, x, y, -225, r1, r2)  # 0mm/hr marker

    cv.create_text(x - 52, y + 52, fill="darkblue", font="Arial 10 bold", text="0")
    cv.create_text(x - 63, y - 30, fill="darkblue", font="Arial 10 bold", text="0.1")
    cv.create_text(x - 25, y - 68, fill="darkblue", font="Arial 10 bold", text="0.5")
    cv.create_text(x, y - 72, fill="darkblue", font="Arial 10 bold", text="1")
    cv.create_text(x + 25, y - 68, fill="darkblue", font="Arial 10 bold", text="2")
    cv.create_text(x + 53, y - 50, fill="darkblue", font="Arial 10 bold", text="5")
    cv.create_text(x + 66, y - 28, fill="darkblue", font="Arial 10 bold", text="10")
    cv.create_text(x + 73, y + 3, fill="darkblue", font="Arial 10 bold", text="20")
    cv.create_text(x + 65, y + 30, fill="darkblue", font="Arial 10 bold", text="50")
    cv.create_text(x + 46, y + 52, fill="darkblue", font="Arial 10 bold", text="100")
    cv.create_text(x, y + 70, fill="darkblue", font="Arial 10 bold", text=name)


# Draw the pressure rate gauge at the x,y coordinates of the canvas cv
def draw_pressure_rate_gauge(x, y, cv, name):
    cv.create_circle(x, y, 98, outline="black", width=6)
    cv.create_circle(x, y, 96, outline="darkblue", width=2)
    cv.create_circle(x, y, 95, fill="white")
    cv.create_circle_arc(x, y, 95, start=-45, end=-18, fill="red", outline="red")
    cv.create_circle_arc(x, y, 95, start=-18, end=9, fill="orange", outline="orange")
    cv.create_circle_arc(x, y, 95, start=9, end=36, fill="yellow", outline="yellow")
    cv.create_circle_arc(x, y, 95, start=36, end=117, fill="green", outline="green")
    cv.create_circle_arc(x, y, 95, start=117, end=144, fill="green", outline="green")
    cv.create_circle_arc(x, y, 95, start=144, end=171, fill="yellow", outline="yellow")
    cv.create_circle_arc(x, y, 95, start=171, end=198, fill="orange", outline="orange")
    cv.create_circle_arc(x, y, 95, start=198, end=225, fill="red", outline="red")
    cv.create_circle(x, y, 85, fill="white", outline="white")
    cv.create_circle_arc(x, y, 85, start=225, end=-45, outline="darkblue", style=ARC)
    cv.create_circle(x, y, 8, fill="red")

    r1 = 85
    r2 = 80
    for z in range(0, 11):
        a = 45 + z * 27
        x1 = x + math.sin(math.radians(a)) * r1
        x2 = x + math.sin(math.radians(a)) * r2
        y1 = y + math.cos(math.radians(a)) * r1
        y2 = y + math.cos(math.radians(a)) * r2
        cv.create_line(x1, y1, x2, y2)
    cv.create_text(x - 52, y + 52, fill="darkblue", font="Arial 10 bold", text="-10")
    cv.create_text(x - 68, y + 22, fill="darkblue", font="Arial 10 bold", text="-8")
    cv.create_text(x - 70, y - 12, fill="darkblue", font="Arial 10 bold", text="-6")
    cv.create_text(x - 58, y - 42, fill="darkblue", font="Arial 10 bold", text="-4")
    cv.create_text(x - 30, y - 65, fill="darkblue", font="Arial 10 bold", text="-2")
    cv.create_text(x, y - 72, fill="darkblue", font="Arial 10 bold", text="0")
    cv.create_text(x + 30, y - 65, fill="darkblue", font="Arial 10 bold", text="+2")
    cv.create_text(x + 58, y - 42, fill="darkblue", font="Arial 10 bold", text="+4")
    cv.create_text(x + 70, y - 12, fill="darkblue", font="Arial 10 bold", text="+6")
    cv.create_text(x + 68, y + 22, fill="darkblue", font="Arial 10 bold", text="+8")
    cv.create_text(x + 46, y + 52, fill="darkblue", font="Arial 10 bold", text="+10")
    cv.create_text(x, y + 70, fill="darkblue", font="Arial 10 bold", text=name)


# Draw the sferic gauge at the x,y coordinates of the canvas cv
# Value will be the average of the two counters
def draw_sferic_gauge(x, y, cv, name):
    cv.create_circle(x, y, 98, outline="black", width=6)
    cv.create_circle(x, y, 96, outline="darkblue", width=2)
    cv.create_circle(x, y, 95, fill="white")
    cv.create_circle_arc(x, y, 95, start=-45, end=-24.68, fill="magenta",
                         outline="magenta")  # 5-10k strikes
    cv.create_circle_arc(x, y, 95, start=-24.68, end=30.545, fill="red", outline="red")  # 760-5k
    cv.create_circle_arc(x, y, 95, start=30.545, end=49.36, fill="orange", outline="orange")  # 400-750
    cv.create_circle_arc(x, y, 95, start=49.36, end=61.989, fill="yellow", outline="yellow")  # 260-400
    cv.create_circle_arc(x, y, 95, start=61.989, end=225, fill="green", outline="green")  # 0-250
    cv.create_circle(x, y, 85, fill="white", outline="white")
    cv.create_circle_arc(x, y, 85, start=225, end=-45, outline="darkblue", style=ARC)
    cv.create_circle(x, y, 8, fill="red")

    r1 = 85
    r2 = 80
    # Angle is 157.5 - 67.5 * (1 + log(sfericCount))
    draw_angled_line(cv, x, y, 45, r1, r2)
    draw_angled_line(cv, x, y, 24.68, r1, r2)
    draw_angled_line(cv, x, y, 2.18, r1, r2)
    draw_angled_line(cv, x, y, -22.5, r1, r2)
    draw_angled_line(cv, x, y, -42.82, r1, r2)
    draw_angled_line(cv, x, y, -69.68, r1, r2)
    draw_angled_line(cv, x, y, -90, r1, r2)
    draw_angled_line(cv, x, y, -110.32, r1, r2)
    draw_angled_line(cv, x, y, -157.5, r1, r2)
    draw_angled_line(cv, x, y, -225, r1, r2)

    cv.create_text(x - 52, y + 52, fill="darkblue", font="Arial 10 bold", text="0")
    cv.create_text(x - 63, y - 30, fill="darkblue", font="Arial 10 bold", text="10")
    cv.create_text(x - 25, y - 68, fill="darkblue", font="Arial 10 bold", text="50")
    cv.create_text(x, y - 72, fill="darkblue", font="Arial 10 bold", text="100")
    cv.create_text(x + 25, y - 68, fill="darkblue", font="Arial 10 bold", text="200")
    cv.create_text(x + 53, y - 50, fill="darkblue", font="Arial 10 bold", text="500")
    cv.create_text(x + 66, y - 28, fill="darkblue", font="Arial 10 bold", text="1k")
    cv.create_text(x + 73, y + 3, fill="darkblue", font="Arial 10 bold", text="2k")
    cv.create_text(x + 65, y + 30, fill="darkblue", font="Arial 10 bold", text="5k")
    cv.create_text(x + 46, y + 52, fill="darkblue", font="Arial 10 bold", text="10k")
    cv.create_text(x, y + 70, fill="darkblue", font="Arial 10 bold", text=name)


# Draw the sferic rate gauge at the x,y coordinates of the canvas cv
# Value will be the average rate of the two counters
def draw_sferic_rate_gauge(x, y, cv, name):
    cv.create_circle(x, y, 98, outline="black", width=6)
    cv.create_circle(x, y, 96, outline="darkblue", width=2)
    cv.create_circle(x, y, 95, fill="white")
    cv.create_circle_arc(x, y, 95, start=-45, end=-24.68, fill="magenta",
                         outline="magenta")  # 5-10k strikes/hr
    cv.create_circle_arc(x, y, 95, start=-24.68, end=30.545, fill="red", outline="red")  # 1.5-10k
    cv.create_circle_arc(x, y, 95, start=30.545, end=49.36, fill="orange", outline="orange")  # 801-1.5k
    cv.create_circle_arc(x, y, 95, start=49.36, end=61.989, fill="yellow", outline="yellow")  # 501-800
    cv.create_circle_arc(x, y, 95, start=61.989, end=225, fill="green", outline="green")  # 0-500
    cv.create_circle(x, y, 85, fill="white", outline="white")
    cv.create_circle_arc(x, y, 85, start=225, end=-45, outline="darkblue", style=ARC)
    cv.create_circle(x, y, 8, fill="red")

    r1 = 85
    r2 = 80
    # Angle is 157.5 - 67.5 * (1 + log(sfericRate))
    draw_angled_line(cv, x, y, 45, r1, r2)
    draw_angled_line(cv, x, y, 24.68, r1, r2)
    draw_angled_line(cv, x, y, 2.18, r1, r2)
    draw_angled_line(cv, x, y, -22.5, r1, r2)
    draw_angled_line(cv, x, y, -42.82, r1, r2)
    draw_angled_line(cv, x, y, -69.68, r1, r2)
    draw_angled_line(cv, x, y, -90, r1, r2)
    draw_angled_line(cv, x, y, -110.32, r1, r2)
    draw_angled_line(cv, x, y, -157.5, r1, r2)
    draw_angled_line(cv, x, y, -225, r1, r2)

    cv.create_text(x - 52, y + 52, fill="darkblue", font="Arial 10 bold", text="0")
    cv.create_text(x - 63, y - 30, fill="darkblue", font="Arial 10 bold", text="10")
    cv.create_text(x - 25, y - 68, fill="darkblue", font="Arial 10 bold", text="50")
    cv.create_text(x, y - 72, fill="darkblue", font="Arial 10 bold", text="100")
    cv.create_text(x + 25, y - 68, fill="darkblue", font="Arial 10 bold", text="200")
    cv.create_text(x + 53, y - 50, fill="darkblue", font="Arial 10 bold", text="500")
    cv.create_text(x + 66, y - 28, fill="darkblue", font="Arial 10 bold", text="1k")
    cv.create_text(x + 73, y + 3, fill="darkblue", font="Arial 10 bold", text="2k")
    cv.create_text(x + 65, y + 30, fill="darkblue", font="Arial 10 bold", text="5k")
    cv.create_text(x + 46, y + 52, fill="darkblue", font="Arial 10 bold", text="10k")
    cv.create_text(x, y + 70, fill="darkblue", font="Arial 10 bold", text=name)


def draw_angled_line(canv, x, y, a, r1, r2):
    x1 = x + math.cos(math.radians(a)) * r1
    x2 = x + math.cos(math.radians(a)) * r2
    y1 = y + math.sin(math.radians(a)) * r1
    y2 = y + math.sin(math.radians(a)) * r2
    canv.create_line(x1, y1, x2, y2)


def update_canvas_compass(cv, d_string, pts):
    if len(pts) == 6:
        try:
            cv.itemconfigure(wind_dir_text, text=d_string)
            cv.coords(wind_dir_pointer, pts)
        except ValueError:
            pass
        except:
            pass


def update_canvas_extt_gauge(cv, et_string, etp):
    try:
        cv.itemconfigure(ext_temp_text, text=et_string)
        cv.coords(ext_temp_pointer, etp)
        get_max_limit_points = calculate_limit_points(extt_x, extt_y, trh_sensor.max_temp_c)
        cv.coords(ext_temp_max_line, get_max_limit_points)
        get_min_limit_points = calculate_limit_points(extt_x, extt_y, trh_sensor.min_temp_c)
        cv.coords(ext_temp_min_line, get_min_limit_points)
    except StopIteration:
        pass


def update_canvas_rh_gauge(cv, rh_string, rh_points):
    try:
        cv.coords(ext_rh_pointer, rh_points)
        cv.itemconfigure(ext_rh_text, text=rh_string)
        max_limit_points = calculate_rh_limit_points(extrh_x, extrh_y, trh_sensor.max_rh)
        # print("Max RH", trh_sensor.max_rh)
        # print("Min RH", trh_sensor.min_rh)
        cv.coords(ext_rh_max_line, max_limit_points)
        min_limit_points = calculate_rh_limit_points(extrh_x, extrh_y, trh_sensor.min_rh)
        cv.coords(ext_rh_min_line, min_limit_points)
    except StopIteration:
        pass


def update_canvas_pressure_gauge(cv, p_string, p_points):
    try:
        cv.coords(pressure_pointer, p_points)
        cv.itemconfigure(pressure_text, text=p_string)
    except StopIteration:
        pass


def update_canvas_time(cv, time_string):
    try:
        cv.itemconfigure(timetext, text=time_string)
    except StopIteration:
        pass


def update_canvas_wind_speed_gauge(cv, g_string, g_points, s_string, s_points):
    try:
        cv.coords(gust_pointer, g_points)
        cv.coords(speed_pointer, s_points)
        cv.itemconfigure(wind_gust_text, text=g_string)
        cv.itemconfigure(wind_speed_text, text=s_string)
    except StopIteration:
        pass


def update_canvas_vis_gauge(cv, l_string, l_points):
    try:
        cv.coords(vis_pointer, l_points)
        cv.itemconfigure(vis_text, text=l_string)
    except StopIteration:
        pass


def update_canvas_uvindex_gauge(cv, string, pts):
    try:
        cv.coords(uvindex_pointer, pts)
        cv.itemconfigure(uvindex_text, text=string)
    except StopIteration:
        pass


def update_canvas_rain_gauge(cv, string, pts):
    try:
        cv.coords(rain_pointer, pts)
        cv.itemconfigure(rain_text, text=string)
    except StopIteration:
        pass


def update_canvas_rainrate_gauge(cv, string, pts):
    try:
        cv.coords(rainrate_pointer, pts)
        cv.itemconfigure(rainrate_text, text=string)
    except StopIteration:
        pass


def update_canvas_intt_gauge(cv, t_string, temp_points):
    try:
        cv.itemconfigure(int_temp_text, text=t_string)
        cv.coords(int_temp_pointer, temp_points)
        get_max_limit_points = calculate_limit_points(intt_x, intt_y, base_sensor.max_temp_c)
        cv.coords(int_temp_max_line, get_max_limit_points)
        get_min_limit_points = calculate_limit_points(intt_x, intt_y, base_sensor.min_temp_c)
        cv.coords(int_temp_min_line, get_min_limit_points)
    except StopIteration:
        pass


def update_canvas_int_rh_gauge(cv, rh_string, rh_points):
    try:
        cv.coords(int_rh_pointer, rh_points)
        cv.itemconfigure(int_rh_text, text=rh_string)
    except StopIteration:
        pass


# Updates the part of the canvas for the pressure rate gauge
def update_canvas_pressure_rate_gauge(cv, prr_string, p_points):
    try:
        cv.coords(prr_pointer, p_points)
        cv.itemconfigure(prr_text, text=prr_string)
    except StopIteration:
        pass


def update_canvas_sferic_gauge(cv, string, pts):
    try:
        cv.coords(sf_pointer, pts)
        cv.itemconfigure(sf_text, text=string)
    except StopIteration:
        pass


def update_canvas_sferic_rate_gauge(cv, string, pts):
    try:
        cv.coords(sfr_pointer, pts)
        cv.itemconfigure(sfr_text, text=string)
    except StopIteration:
        pass


# Draws the external temperature 24 hour graph to the screen
def draw_ext_temp_graph():
    trh_sensor.draw_ext_temp_graph()


# Draws the external relative humidity 24 hour graph to the screen
def draw_ext_rh_graph():
    trh_sensor.draw_ext_rh_graph()


def draw_ext_trh_sensor_temp_graph():
    trh_sensor.draw_sensor_temp_graph()


def draw_ext_trh_v_mcu_graph():
    trh_sensor.draw_v_mcu_graph()


def draw_ext_trh_v_supply_graph():
    trh_sensor.draw_v_supply_graph()


def draw_ext_trh_v_fan_graph():
    trh_sensor.draw_v_fan_graph()


def draw_ext_trh_rssi_graph():
    trh_sensor.draw_rssi_graph()


def draw_ext_trh_snr_graph():
    trh_sensor.draw_snr_graph()


def draw_int_temp_graph():
    base_sensor.draw_temp_graph()


def draw_int_rh_graph():
    base_sensor.draw_rh_graph()


def draw_pressure_graph():
    base_sensor.draw_pressure_graph()


def draw_visible_light_graph():
    uvl_sensor.draw_vis_graph()


def draw_uv_graph():
    uvl_sensor.draw_uv_graph()


def draw_uvl_sensor_temp_graph():
    uvl_sensor.draw_sensor_temp_graph()


def draw_uvl_v_mcu_graph():
    uvl_sensor.draw_v_mcu_graph()


def draw_uvl_rssi_graph():
    uvl_sensor.draw_rssi_graph()


def draw_uvl_snr_graph():
    uvl_sensor.draw_snr_graph()


def draw_sferic_graph():
    sferic_sensor.draw_sf_graph()


def draw_sf_sensor_temp_graph():
    sferic_sensor.draw_sensor_temp_graph()


def draw_sf_sensor_v_mcu_graph():
    sferic_sensor.draw_v_mcu_graph()


def draw_sf_sensor_rssi_graph():
    sferic_sensor.draw_rssi_graph()


def draw_sf_sensor_snr_graph():
    sferic_sensor.draw_snr_graph()


def draw_rainfall_graph():
    rainfall_sensor.draw_24hr_rainfall_graph()


def draw_rainfall_rate_graph():
    rainfall_sensor.draw_24hr_rainrate_graph()


def draw_rainfall_sensor_temp_graph():
    rainfall_sensor.draw_sensor_temp_graph()


def draw_rainfall_v_mcu_graph():
    rainfall_sensor.draw_v_mcu_graph()


def draw_rainfall_rssi_graph():
    rainfall_sensor.draw_rssi_graph()


def draw_rainfall_snr_graph():
    rainfall_sensor.draw_snr_graph()


# Displays an extra frame with additional sensor data in it
def display_aux_sensor_window():
    aux_sensor_window.deiconify()


def draw_wind_graph():
    wind_sensor.draw_wind_graph()


def draw_wind_dir_graph():
    wind_sensor.draw_dir_graph()


def draw_wind_temp_graph():
    wind_sensor.draw_sensor_temp_graph()


def draw_wind_vmcu_graph():
    wind_sensor.draw_v_mcu_graph()


def draw_wind_rssi_graph():
    wind_sensor.draw_rssi_graph()


def draw_wind_snr_graph():
    wind_sensor.draw_snr_graph()


# Restores data to data structures in each sensor object at program start
def restore_data():
    # trh_sensor.restore_data()
    base_sensor.load_dict() # Restores the max/min data


def on_closing():
    base_sensor.save_dict() # Saves the max/min data
    global close_requested
    close_requested = True
    # print("Goodbye!")
    # BOARD.teardown()


def reset_int_temp_month_max_min():
    base_sensor.reset_month_max_min_temp()


def reset_int_temp_year_max_min():
    base_sensor.reset_year_max_min_temp()


def reset_int_temp_alltime_max_min():
    base_sensor.reset_alltime_max_min_temp()


def reset_pressure_month_max_min():
    base_sensor.reset_month_max_min_pressure()


print("Weather Station Python Program")

# GUI
window = Tk()
window.title("Weather Station Python Program")
window.protocol("WM_DELETE_WINDOW", on_closing)
frame = Frame(master=window, relief=SUNKEN, borderwidth=5)
frame.pack()

menubar = Menu(window)
file_menu = Menu(menubar, tearoff=0)
file_menu.add_command(label="Exit", command=on_closing)
menubar.add_cascade(label="File", menu=file_menu)
edit_menu = Menu(file_menu, tearoff=0)
reset_menu = Menu(edit_menu, tearoff=0)
reset_menu.add_command(label="Reset Int Temp Month Max/Min", command=reset_int_temp_month_max_min)
reset_menu.add_command(label="Reset Int Temp Year Max/Min", command=reset_int_temp_year_max_min)
reset_menu.add_command(label="Reset Int Temp All Time Max/Min", command=reset_int_temp_alltime_max_min)
reset_menu.add_command(label="Reset Pressure Month Max/Min", command=reset_pressure_month_max_min)
file_menu.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_cascade(label="Reset", menu=reset_menu)

view_menu = Menu(menubar, tearoff=0)
graph_menu = Menu(view_menu, tearoff=0)
ext_trh_graph_menu = Menu(graph_menu, tearoff=0)
base_graph_menu = Menu(graph_menu, tearoff=0)
vis_uv_graph_menu = Menu(graph_menu, tearoff=0)
sferic_graph_menu = Menu(graph_menu, tearoff=0)
rain_graph_menu = Menu(graph_menu, tearoff=0)
wind_graph_menu = Menu(graph_menu, tearoff=0)

ext_trh_graph_menu.add_command(label="Ext Temp Graph", command=draw_ext_temp_graph)
ext_trh_graph_menu.add_command(label="Ext RH Graph", command=draw_ext_rh_graph)
ext_trh_graph_menu.add_command(label="ExtTRH S Temp Graph", command=draw_ext_trh_sensor_temp_graph)
ext_trh_graph_menu.add_command(label="ExtTRH V MCU Graph", command=draw_ext_trh_v_mcu_graph)
ext_trh_graph_menu.add_command(label="ExtTRH V Supply Graph", command=draw_ext_trh_v_supply_graph)
ext_trh_graph_menu.add_command(label="ExtTRH V Fan Graph", command=draw_ext_trh_v_fan_graph)
ext_trh_graph_menu.add_command(label="ExtTRH RSSI Graph", command=draw_ext_trh_rssi_graph)
ext_trh_graph_menu.add_command(label="ExtTRH SNR Graph", command=draw_ext_trh_snr_graph)

base_graph_menu.add_command(label="Int Temp Graph", command=draw_int_temp_graph)
base_graph_menu.add_command(label="Int RH Graph", command=draw_int_rh_graph)
base_graph_menu.add_command(label="Pressure Graph", command=draw_pressure_graph)

vis_uv_graph_menu.add_command(label="Visible Light Graph", command=draw_visible_light_graph)
vis_uv_graph_menu.add_command(label="UV Graph", command=draw_uv_graph)
vis_uv_graph_menu.add_command(label="UVL S Temp Graph", command=draw_uvl_sensor_temp_graph)
vis_uv_graph_menu.add_command(label="UVL V MCU Graph", command=draw_uvl_v_mcu_graph)
vis_uv_graph_menu.add_command(label="UVL RSSI Graph", command=draw_uvl_rssi_graph)
vis_uv_graph_menu.add_command(label="UVL SNR Graph", command=draw_uvl_snr_graph)

sferic_graph_menu.add_command(label="Sferic Graph", command=draw_sferic_graph)
sferic_graph_menu.add_command(label="Sferic S Temp Graph", command=draw_sf_sensor_temp_graph)
sferic_graph_menu.add_command(label="Sferic V MCU Graph", command=draw_sf_sensor_v_mcu_graph)
sferic_graph_menu.add_command(label="Sferic RSSI Graph", command=draw_sf_sensor_rssi_graph)
sferic_graph_menu.add_command(label="Sferic SNR Graph", command=draw_sf_sensor_snr_graph)

rain_graph_menu.add_command(label="Rainfall Graph", command=draw_rainfall_graph)
rain_graph_menu.add_command(label="Rainfall Rate Graph", command=draw_rainfall_rate_graph)
rain_graph_menu.add_command(label="Rainfall S Temp Graph", command=draw_rainfall_sensor_temp_graph)
rain_graph_menu.add_command(label="Rainfall V MCU Graph", command=draw_rainfall_v_mcu_graph)
rain_graph_menu.add_command(label="Rainfall RSSI Graph", command=draw_rainfall_rssi_graph)
rain_graph_menu.add_command(label="Rainfall SNR Graph", command=draw_rainfall_snr_graph)

wind_graph_menu.add_command(label="Wind Speed Graph", command=draw_wind_graph)
wind_graph_menu.add_command(label="Wind Direction Graph", command=draw_wind_dir_graph)
wind_graph_menu.add_command(label="Wind S Temp Graph", command=draw_wind_temp_graph)
wind_graph_menu.add_command(label="Wind V MCU Graph", command=draw_wind_vmcu_graph)
wind_graph_menu.add_command(label="Wind RSSI Graph", command=draw_wind_rssi_graph)
wind_graph_menu.add_command(label="Wind SNR Graph", command=draw_wind_snr_graph)

view_menu.add_command(label="Aux Sensors", command=display_aux_sensor_window)
menubar.add_cascade(label="View", menu=view_menu)
view_menu.add_cascade(label="Graphs", menu=graph_menu)
graph_menu.add_cascade(label="Ext TRH Graphs", menu=ext_trh_graph_menu)
graph_menu.add_cascade(label="Base Sensor Graphs", menu=base_graph_menu)
graph_menu.add_cascade(label="UV/Vis Sensor Graphs", menu=vis_uv_graph_menu)
graph_menu.add_cascade(label="Sferic Graphs", menu=sferic_graph_menu)
graph_menu.add_cascade(label="Rainfall Graphs", menu=rain_graph_menu)
graph_menu.add_cascade(label="Wind Graphs", menu=wind_graph_menu)

c = Canvas(window, height=768, width=1024)
gif1 = PhotoImage(file='metal.gif')
c.create_image(0, 0, image=gif1, anchor=NW)
timetext = c.create_text(10, 748, anchor=NW, width=80, font=("arial", 10))

p_length = 70  # Length of gauge pointers
comp_x = 920
comp_y = 104
draw_compass(comp_x, comp_y, c)
points = [comp_x - 8, comp_y, comp_x + 8, comp_y, comp_x, comp_y - p_length]
wind_dir_pointer = c.create_polygon(points, fill="red")
wind_dir_text = c.create_text(comp_x, comp_y + 50, width=80, font=("arial", 8), fill="darkblue")

extt_x = 104
extt_y = 104
draw_temp_gauge(extt_x, extt_y, c, "Ext Temp")
ext_temp_points = [extt_x - 8, extt_y, extt_x + 8, extt_y, extt_x, extt_y - p_length]
ext_temp_pointer = c.create_polygon(ext_temp_points, fill="red")
ext_temp_text = c.create_text(extt_x, extt_y + 50, width=80, font=("arial", 8), fill="darkblue")
get_limit_points = calculate_limit_points(extt_x - 8, extt_y, 50)
ext_temp_max_line = c.create_line(get_limit_points, fill="red", width=2)
get_limit_points = calculate_limit_points(extt_x - 8, extt_y, -20)
ext_temp_min_line = c.create_line(get_limit_points, fill="blue", width=2)

extrh_x = 308
extrh_y = 104
draw_rh_gauge(extrh_x, extrh_y, c, "Ext RH")
ext_rh_points = [extrh_x - 8, extrh_y, extrh_x + 8, extrh_y, extrh_x, extrh_y - p_length]
ext_rh_pointer = c.create_polygon(ext_rh_points, fill="red")
ext_rh_text = c.create_text(extrh_x, extrh_y + 50, width=80, font=("arial", 8), fill="darkblue")
rh_limit_points = calculate_rh_limit_points(extrh_x - 8, extrh_y, 50)
ext_rh_max_line = c.create_line(rh_limit_points, fill="red", width=2)
rh_limit_points = calculate_rh_limit_points(extrh_x - 8, extrh_y, -20)
ext_rh_min_line = c.create_line(rh_limit_points, fill="blue", width=2)

pr_x = 512
pr_y = 104
draw_pressure_gauge(pr_x, pr_y, c, "Pressure")
pressure_points = [pr_x - 8, pr_y, pr_x + 8, pr_y, pr_x, pr_y - p_length]
pressure_pointer = c.create_polygon(pressure_points, fill="red")
pressure_text = c.create_text(pr_x, pr_y + 50, width=80, font=("arial", 8), fill="darkblue")

wsg_x = 920
wsg_y = 308
draw_wind_speed_gauge(wsg_x, wsg_y, c, "Wind Speed")
gust_points = [wsg_x - 8, wsg_y, wsg_x + 8, wsg_y, wsg_x, wsg_y - p_length]
speed_points = [wsg_x - 8, wsg_y, wsg_x + 8, wsg_y, wsg_x, wsg_y - p_length]
speed_pointer = c.create_polygon(speed_points, fill="orange")
gust_pointer = c.create_polygon(gust_points, fill="red")
wind_gust_text = c.create_text(wsg_x, wsg_y + 45, width=80, font=("arial", 8), fill="darkblue")
wind_speed_text = c.create_text(wsg_x, wsg_y + 58, width=80, font=("arial", 8), fill="darkblue")

visg_x = 104
visg_y = 308
draw_vis_gauge(visg_x, visg_y, c, "Vis Light")
vis_points = [visg_x - 8, visg_y, visg_x + 8, visg_y, visg_x, visg_y - p_length]
vis_pointer = c.create_polygon(vis_points, fill="red")
vis_text = c.create_text(visg_x, visg_y + 58, width=80, font=("arial", 8), fill="darkblue")

uvig_x = 308
uvig_y = 308
draw_uvindex_gauge(uvig_x, uvig_y, c, "UV Index")
uvindex_points = [uvig_x - 8, uvig_y, uvig_x + 8, uvig_y, uvig_x, uvig_y - p_length]
uvindex_pointer = c.create_polygon(uvindex_points, fill="red")
uvindex_text = c.create_text(uvig_x, uvig_y + 58, width=80, font=("arial", 8), fill="darkblue")

rng_x = 512
rng_y = 308
draw_rain_gauge(rng_x, rng_y, c, "Rain today")
rain_points = [rng_x - 8, rng_y, rng_x + 8, rng_y, rng_x, rng_y - p_length]
rain_pointer = c.create_polygon(rain_points, fill="red")
rain_text = c.create_text(rng_x, rng_y + 58, width=80, font=("arial", 8), fill="darkblue")

rrg_x = 716
rrg_y = 308
draw_rain_gauge(rrg_x, rrg_y, c, "Rain Rate")
rainrate_points = [rrg_x - 8, rrg_y, rrg_x + 8, rrg_y, rrg_x, rrg_y - p_length]
rainrate_pointer = c.create_polygon(rainrate_points, fill="red")
rainrate_text = c.create_text(rrg_x, rrg_y + 58, width=80, font=("arial", 8), fill="darkblue")

intt_x = 104
intt_y = 512
draw_temp_gauge(intt_x, intt_y, c, "Int Temp")
int_temp_points = [intt_x - 8, intt_y, intt_x + 8, intt_y, intt_x, intt_y - p_length]
int_temp_pointer = c.create_polygon(int_temp_points, fill="red")
int_temp_text = c.create_text(intt_x, intt_y + 50, width=80, font=("arial", 8), fill="darkblue")
get_limit_points = calculate_limit_points(intt_x - 8, intt_y, 50)
int_temp_max_line = c.create_line(get_limit_points, fill="red", width=2)
get_limit_points = calculate_limit_points(intt_x - 8, intt_y, -20)
int_temp_min_line = c.create_line(get_limit_points, fill="blue", width=2)

intrh_x = 308
intrh_y = 512
draw_rh_gauge(intrh_x, intrh_y, c, "Int RH")
int_rh_points = [intrh_x - 8, intrh_y, intrh_x + 8, intrh_y, intrh_x, intrh_y - p_length]
int_rh_pointer = c.create_polygon(int_rh_points, fill="red")
int_rh_text = c.create_text(intrh_x, intrh_y + 50, width=80, font=("arial", 8), fill="darkblue")

prr_x = 716
prr_y = 104
draw_pressure_rate_gauge(prr_x, prr_y, c, "P. Rate")
prr_points = [prr_x - 8, prr_y, prr_x + 8, prr_y, prr_x, prr_y - p_length]
prr_pointer = c.create_polygon(prr_points, fill="red")
prr_text = c.create_text(prr_x, prr_y + 50, width=80, font=("arial", 8), fill="darkblue")

sf_x = 512
sf_y = 512
draw_sferic_gauge(sf_x, sf_y, c, "Sferics")
sf_points = [sf_x - 8, sf_y, sf_x + 8, sf_y, sf_x, sf_y - p_length]
sf_pointer = c.create_polygon(sf_points, fill="red")
sf_text = c.create_text(sf_x, sf_y + 50, width=80, font=("arial", 8), fill="darkblue")

sfr_x = 716
sfr_y = 512
draw_sferic_rate_gauge(sfr_x, sfr_y, c, "Sferic Rate")
sfr_points = [sfr_x - 8, sfr_y, sfr_x + 8, sfr_y, sfr_x, sfr_y - p_length]
sfr_pointer = c.create_polygon(sfr_points, fill="red")
sfr_text = c.create_text(sfr_x, sfr_y + 50, width=80, font=("arial", 8), fill="darkblue")

# Toplevel object which will
# be treated as a new window
aux_sensor_window = Toplevel(window)

# Sets the title of the
# Toplevel widget
aux_sensor_window.title("Aux Sensors & Values")

# Sets the geometry of top level
aux_sensor_window.geometry("1024x768")


def disable_event():
    pass


aux_sensor_window.protocol("WM_DELETE_WINDOW", disable_event)  # Stops the aux sensor window from being destroyed

# A label widget to show in toplevel
Label(aux_sensor_window,
      text="Average Temp:").pack()

av_temp_value_text = StringVar()
av_temp_value_text.set(str(trh_sensor.av_temp))
Label(aux_sensor_window, textvariable=av_temp_value_text).pack()

Label(aux_sensor_window, text="Wind Chill:").pack()
wc_value_text = StringVar()
wc_value_text.set(str(wind_chill_sensor.wind_chill) + degree_sign + "C")
Label(aux_sensor_window, textvariable=wc_value_text).pack()

Label(aux_sensor_window, text="App Temp:").pack()
at_value_text = StringVar()
at_value_text.set(str(app_temp_sensor.app_temp) + degree_sign + "C")
Label(aux_sensor_window, textvariable=at_value_text).pack()

Label(aux_sensor_window, text="Heat Index:").pack()
hi_value_text = StringVar()
hi_value_text.set(str(heat_index_sensor.heat_index_C) + degree_sign + "C")
Label(aux_sensor_window, textvariable=hi_value_text).pack()

aux_sensor_window.withdraw()

c.pack()

window.config(menu=menubar)
now = datetime.datetime.now()
old_day = now.day
old_minute = now.minute

args = parser.parse_args(lora)

lora.set_mode(MODE.STDBY)
lora.set_pa_config(pa_select=1)
lora.set_freq(866.5)
lora.set_sync_word(0x55)
print("Starting LoRA continuous receive...")
assert (lora.get_agc_auto_on() == 1)
lora.start()

restore_data()
web_parser.populate_web_tags()
web_parser.parse_file()

print("Calculating some stuff...")
daylight_hours = ts.get_daylight_hours()
print("Daylight hours ", daylight_hours)
ra = ts.get_et_radiation()
print("ET radiation ", ra, "MJ/m2/day")

do_stuff_every_so_often()
window.mainloop()
