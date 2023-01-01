from os.path import exists
from Units import Units
from ExtTRH import ExtTRH
from UV_Light import UV_Light
from Sferic import Sferic
from Rainfall import Rainfall
from Wind import Wind
from Base import Base
from WindChill import *
from ApparentTemp import ApparentTemp
from HeatIndex import HeatIndex
from Location import Location
import time
from astral import LocationInfo
from astral.sun import sun
from astral import moon
import datetime
from pytz import timezone
import pytz


class Web_Parser:
    input_list = ["gaugesT.htm", "indexT.htm", "monthlyrecordT.htm", "recordT.htm", "thismonthT.htm", "thisyearT.htm",
                  "todayT.htm", "trendsT.htm", "yesterdayT.htm"]
    output_list = ["gauges.htm", "index.htm", "monthlyrecord.htm", "record.htm", "thismonth.htm", "thisyear.htm",
                   "today.htm", "trends.htm", "yesterday.htm"]
    # input_file_name = "websitedataT.json"
    # output_file_name = "websitedata.json"
    units = Units()
    # External temp/RH sensor
    # trh_sensor = ExtTRH()
    loc = Location()

    def __init__(self, u, trh, uvls, sfs, rfs, wfs, bs, wcs, ats, his):
        self.units = u
        self.web_tags = {}
        self.trh_sensor = trh
        self.uvl_sensor = uvls
        self.sferic_sensor = sfs
        self.rainfall_sensor = rfs
        self.wind_sensor = wfs
        self.base_sensor = bs
        self.wind_chill_sensor = wcs
        self.apparent_temp_sensor = ats
        self.heat_index_sensor = his

    def populate_web_tags(self):
        print("Populating/updating web tags")
        # MEASUREMENT UNITS
        self.web_tags.update({"<#tempunit>": self.units.temp_unit})
        self.web_tags.update({"<#tempunitnoenc>": self.units.temp_unit_no_enc})
        self.web_tags.update({"<#tempunitnodeg>": self.units.temp_unit_no_deg})
        self.web_tags.update({"<#pressunit>": self.units.press_unit})
        self.web_tags.update({"<#rainunit>": self.units.rain_unit})
        self.web_tags.update({"<#windunit>": self.units.wind_unit})
        self.web_tags.update({"<#windrununit>": self.units.wind_run_unit})
        self.web_tags.update({"<#cloudbaseunit>": self.units.cloud_base_unit})

        # DATE AND TIME
        today = datetime.date.today()
        self.web_tags.update({"<#date>": today.strftime("%d %B %Y")})
        self.web_tags.update({"<#time>": time.strftime("%H:%M:%S")})
        self.web_tags.update({"<#update>": time.strftime("%d/%m/%Y %H:%M:%S")})
        utc = pytz.timezone('UTC')
        now = utc.localize(datetime.datetime.utcnow())
        uk = pytz.timezone('Europe/London')
        local_time = now.astimezone(uk)

        city = self.loc.loc_info
        s = sun(city.observer, date=local_time)
        daylight_length = s["dusk"] - s["dawn"]
        day_length = s["sunset"] - s["sunrise"]

        self.web_tags.update({"<#dawn>": str(s["dawn"]) + " UTC"})
        self.web_tags.update({"<#sunrise>": str(s["sunrise"]) + " UTC"})
        self.web_tags.update({"<#sunset>": str(s["sunset"]) + " UTC"})
        self.web_tags.update({"<#dusk>": str(s["dusk"]) + " UTC"})
        self.web_tags.update({"<#moonphase>": str(moon.phase(local_time))})
        self.web_tags.update({"<#daylightlength>": str(daylight_length)})
        self.web_tags.update({"<#daylength>": str(day_length)})

        # CURRENT CONDITIONS
        self.web_tags.update({"<#temp>": str(round(self.trh_sensor.temp_c, 1))})
        self.web_tags.update({"<#feelslike>": str(round(self.apparent_temp_sensor.feels_like, 1))})
        self.web_tags.update({"<#apptemp>": str(round(self.apparent_temp_sensor.app_temp, 1))})
        self.web_tags.update({"<#wchill>": str(round(self.wind_chill_sensor.wind_chill, 1))})
        self.web_tags.update({"<#heatindex>": str(round(self.heat_index_sensor.heat_index_C, 1))})
        self.web_tags.update({"<#TempChangeLastHour>": str(round(self.trh_sensor.temperature_rate, 1))})
        self.web_tags.update({"<#dew>": str(round(self.trh_sensor.dp, 1))})
        self.web_tags.update({"<#hum>": str(round(self.trh_sensor.rh, 1))})
        self.web_tags.update({"<#rfall>": str(round(self.rainfall_sensor.rain_mm, 1))})
        self.web_tags.update({"<#rrate>": str(round(self.rainfall_sensor.rain_rate, 1))})
        self.web_tags.update({"<#wgust>": str(round(self.wind_sensor.gust, 1))})
        s = self.wind_sensor.speed
        sk = self.wind_sensor.mph_to_knots(s)
        self.web_tags.update({"<#wspeed>": str(round(s, 1))})
        self.web_tags.update({"<#beaufort>": str(self.wind_sensor.get_beaufort_number(sk))})
        self.web_tags.update({"<#beaudesc>": self.wind_sensor.get_beaufort_description(sk)})
        wdir = self.wind_sensor.direction
        self.web_tags.update({"<#avgbearing>": str(round(wdir, 1))})
        self.web_tags.update({"<#wdir>": self.wind_sensor.get_direction_text(wdir)})
        self.web_tags.update({"<#press>": str(round(self.base_sensor.sea_level_pressure, 1))})
        pr = self.base_sensor.pressure_rate
        self.web_tags.update({"<#presstrendval>": str(round(pr, 1))})
        self.web_tags.update({"<#presstrend>": self.base_sensor.get_pressure_rate_description(pr)})
        self.web_tags.update({"<#SolarRad>": str(round(self.uvl_sensor.visible, 1))})
        self.web_tags.update({"<#UVI>": str(round(self.uvl_sensor.uvi, 1))})
        self.web_tags.update({"<#UVA>": str(round(self.uvl_sensor.uva, 1))})
        self.web_tags.update({"<#UVB>": str(round(self.uvl_sensor.uvb, 1))})
        self.web_tags.update({"<#UVIndex>": str(round(self.uvl_sensor.uv_index, 1))})
        self.web_tags.update({"<#Sferic1>": str(round(self.sferic_sensor.today_count1, 1))})
        self.web_tags.update({"<#Sferic2>": str(round(self.sferic_sensor.today_count2, 1))})

        # TODAY MAX/MIN
        self.web_tags.update({"<#tempTH>": str(round(self.trh_sensor.max_temp_c, 1))})
        self.web_tags.update({"<#TtempTH>": self.trh_sensor.max_temp_time})
        self.web_tags.update({"<#tempTL>": str(round(self.trh_sensor.min_temp_c, 1))})
        self.web_tags.update({"<#TtempTL>": self.trh_sensor.min_temp_time})
        self.web_tags.update({"<#temprange>": str(round(self.trh_sensor.max_temp_c - self.trh_sensor.min_temp_c, 1))})
        self.web_tags.update({"<#wchillTL>": str(round(self.wind_chill_sensor.min_wind_chill, 1))})
        self.web_tags.update({"<#TwchillTL>": self.wind_chill_sensor.min_wind_chill_time})
        self.web_tags.update({"<#heatindexTH>": str(round(self.heat_index_sensor.max_heat_index, 1))})
        self.web_tags.update({"<#TheatindexTH>": self.heat_index_sensor.max_heat_index_time})
        self.web_tags.update({"<#humTH>": str(round(self.trh_sensor.max_rh, 1))})
        self.web_tags.update({"<#ThumTH>": self.trh_sensor.max_rh_time})
        self.web_tags.update({"<#humTL>": str(round(self.trh_sensor.min_rh, 1))})
        self.web_tags.update({"<#ThumTL>": self.trh_sensor.min_rh_time})
        self.web_tags.update({"<#rrateTM>": str(round(self.rainfall_sensor.max_rain_rate, 1))})
        self.web_tags.update({"<#TrrateTM>": self.rainfall_sensor.max_rain_rate_time})
        self.web_tags.update({"<#rhour>": str(round(self.rainfall_sensor.hour_rain_mm, 1))})
        self.web_tags.update({"<#LastRainTipISO>": self.rainfall_sensor.last_rain})
        self.web_tags.update({"<#wgustTM>": str(round(self.wind_sensor.max_gust, 1))})
        self.web_tags.update({"<#TwgustTM>": self.wind_sensor.max_gust_time})
        max_speed = self.wind_sensor.max_speed
        max_speed_kts = self.wind_sensor.mph_to_knots(max_speed)
        self.web_tags.update({"<#windTM>": str(round(max_speed, 1))})
        self.web_tags.update({"<#Tbeaufort>": str(self.wind_sensor.get_beaufort_number(max_speed_kts))})
        self.web_tags.update({"<#TwindTM>": self.wind_sensor.max_speed_time})
        self.web_tags.update({"<#windrun>": str(round(self.wind_sensor.wind_run,1))})
        # self.web_tags.update({"<#pressTH>": str(round(self.base_sensor.max_slp, 1))})
        self.web_tags.update({"<#pressTH>": str(round(self.base_sensor.basedict["max_slp"], 1))})
        # self.web_tags.update({"<#TpressTH>": self.base_sensor.max_slp_time})
        self.web_tags.update({"<#TpressTH>": self.base_sensor.basedict["max_slp_time"]})
        # self.web_tags.update({"<#pressTL>": str(round(self.base_sensor.min_slp, 1))})
        self.web_tags.update({"<#pressTL>": str(round(self.base_sensor.basedict["min_slp"], 1))})
        # self.web_tags.update({"<#TpressTL>": self.base_sensor.min_slp_time})
        self.web_tags.update({"<#TpressTL>": self.base_sensor.basedict["min_slp_time"]})
        self.web_tags.update({"<#apptempTH>": str(round(self.apparent_temp_sensor.max_app_temp, 1))})
        self.web_tags.update({"<#TapptempTH>": self.apparent_temp_sensor.max_app_temp_time})
        self.web_tags.update({"<#apptempTL>": str(round(self.apparent_temp_sensor.min_app_temp, 1))})
        self.web_tags.update({"<#TapptempTL>": self.apparent_temp_sensor.min_app_temp_time})
        self.web_tags.update({"<#hourlyrainTH>": str(round(self.rainfall_sensor.max_hour_rain, 1))})
        self.web_tags.update({"<#ThourlyrainTH>": self.rainfall_sensor.max_hour_rain_time})

        # MONTH MAX/MIN/TOTALS
        self.web_tags.update({"<#rmonth>": str(round(self.rainfall_sensor.month_rain_mm, 1))})
        self.web_tags.update({"<#ryear>": str(round(self.rainfall_sensor.year_rain_mm, 1))})

        # YEAR MAX/MIN?TOTALS

        # LOCATION
        self.web_tags.update({"<#location>": self.loc.location})
        self.web_tags.update({"<#longlocation>": self.loc.long_location})
        self.web_tags.update({"<#latitude>": str(self.loc.loc_info.latitude)})
        self.web_tags.update({"<#longitude>": str(self.loc.loc_info.longitude)})
        self.web_tags.update({"<#altitude>": str(self.loc.altitude) + 'm'})

        # OTHER
        self.web_tags.update({"<#stationtypeJsEnc>": "RPi LoRa Custom"})
        self.web_tags.update({"<#stationtype>": "RPi LoRa Custom"})
        self.web_tags.update({"<#interval>": "1"})
        self.web_tags.update({"<#rollovertime>": "midnight"})
        self.web_tags.update({"<#graphperiod>": "24"})
        self.web_tags.update({"<#ConsecutiveRainDays>": str(self.rainfall_sensor.days_since_last_dry_day)})
        self.web_tags.update({"<#ConsecutiveDryDays>": str(self.rainfall_sensor.days_since_it_last_rained)})

        # Software Version
        self.web_tags.update({"<#version>": "1"})
        self.web_tags.update({"<#build>": "1"})

    def parse_file(self):
        length = len(self.input_list)
        for i in range(length):
            input_filename = self.input_list[i]
            output_filename = self.output_list[i]
            file_exists = exists(input_filename)
            print("Web File: ", input_filename, " ", file_exists)
            if file_exists:
                fin = open(input_filename, "rt")
                data = fin.read()
                fin.close()
                # print("Before replace:")
                # print(data)
                # print("After replace:")
                for key, value in self.web_tags.items():
                    data = data.replace(key, value)
                # print(data)
                fout = open(output_filename, "w")
                n = fout.write(data)
                fout.close()
                print(output_filename, " written")
