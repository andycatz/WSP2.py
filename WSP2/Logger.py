# Logger
"""
Logs data to CSV files.  Part of the WSP program.
Version 1   10 June 2022
"""

from os.path import exists
import csv
from datetime import datetime

from ApparentTemp import ApparentTemp
from ExtTRH import ExtTRH
from HeatIndex import HeatIndex
from UV_Light import UV_Light
from Sferic import Sferic
from Rainfall import Rainfall
from Wind import Wind
from Base import Base

# Base sensor
from WindChill import WindChill

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

# Wind chill sensor
wind_chill_sensor = WindChill()

# Apparent temperature sensor
apparent_temp_sensor = ApparentTemp()

# Heat Index Sensor
heat_index_sensor = HeatIndex()


class Logger(ExtTRH, UV_Light, Sferic, Rainfall, Wind, Base, WindChill, ApparentTemp, HeatIndex):
    daylogfilename = "dayFile.txt"
    dayfileheader = ['Date', 'MaxGust', 'GustBRG', 'GustTime', 'MinExtTemp',
                     'MinExtTempTime', 'MaxExtTemp', 'MaxExtTempTime', 'MinSLP', 'MinSLPTime',
                     'MaxSLP', 'MaxSLPTime', 'MaxRR', 'MaxRRTime', 'Rain', 'AvTemp', 'WindRun',
                     'MaxAvWind', 'MaxAvWindTime', 'MinExtRH', 'MinExtRHTime', 'MaxExtRH', 'MaxExtRHTime'
                                                                                           'Evapo', 'SunHours',
                     'HHIndex', 'HAppTemp', 'HAppTempTime', 'LAppTemp',
                     'LAppTempTime', 'HHRain', 'HHRainTime', 'MaxWChill', 'MaxWChillTime',
                     'HDP', 'HDPTime', 'LDP', 'LDPTime', 'DomDir', 'HDD', 'CDD', 'HSR', 'HSRTime',
                     'HUVIX', 'HUVIXTime', 'HFLTemp', 'HFLTempTime', 'LFLTemp', 'LFLTempTime',
                     'HHMDX', 'HHMDXTime', 'LHMDX', 'LHMDXTime', 'CUMCH', 'UVAMax', 'UVAMaxTime',
                     'UVBMax', 'UVBMaxTime', 'UVIMax', 'UVIMaxTime', 'VisMax', 'VisMaxTime',
                     'SF1Tot', 'SF2Tot', 'SF1MaxRate', 'SF1MaxRateTime', 'SF2MaxRate',
                     'SF2MaxRateTime', 'RadMax', 'RadMaxTime', 'EFMax', 'EFMaxTime',
                     'EFMin', 'EFMinTime'
                     ]

    trhheader = ['Date', 'Time', 'ExtTemp', 'ExtRH', 'ExtDP', 'STemp', 'VMCU', 'VS', 'VF', 'RSSI', 'SNR', 'MC']
    baseheader = ['Date', 'Time', 'IntTemp', 'IntRH', 'SLP', 'AbsP']
    uvlheader = ['Date', 'Time', 'Vis', 'UVA', 'UVB', 'UVI', 'INDEX', 'STemp', 'VMCU', 'RSSI', 'SNR', 'MC']
    rainheader = ['Date', 'Time', 'Rain', 'Tips', 'Rate', 'STemp', 'VMCU', 'RSSI', 'SNR', 'MC']
    sfericheader = ['Date', 'Time', 'Count1', 'Count2', 'Today1', 'Today2', 'STemp', 'VMCU', 'RSSI', 'SNR', 'MC']
    windheader = ['Date', 'Time', 'Speed', 'Gust', 'Dir', 'STemp', 'VMCU', 'RSSI', 'SNR', 'MC']

    def __init__(self, trhs, uvls, sfs, rfs, wfs, bs, wcs, ats, his):
        self.data = []
        self.trh_sensor = trhs
        self.uvl_sensor = uvls
        self.sferic_sensor = sfs
        self.rainfall_sensor = rfs
        self.wind_sensor = wfs
        self.base_sensor = bs
        self.wind_chill_sensor = wcs
        self.apparent_temp_sensor = ats
        self.heat_index_sensor = his

    def save_minute_log(self):
        # File names are of format TRH_JAN22log.txt
        self.save_trh_data()
        self.save_base_data()
        self.save_uvl_data()
        self.save_rain_data()
        self.save_sferic_data()
        self.save_wind_data()
        x = 0

    def save_trh_data(self):
        # print("Saving TRH data")
        now = datetime.now()
        format = "%d-%m-%Y"
        date1 = now.strftime(format)
        format2 = "%H:%M:%S"
        time1 = now.strftime(format2)
        year1 = now.year
        month1 = now.month
        # print("Year ", year1, " month ", month1)
        filename = "TRH"
        if (month1 < 10):
            filename = filename + "0"
        filename = filename + str(month1) + str(year1) + ".txt"
        # print(filename)
        file_exists = exists(filename)
        if not (file_exists):
            # print("Creating new TRH log file with header...")
            # create file with header
            # open the file in write mode
            f = open(filename, 'w')

            # Create the csv writer
            writer = csv.writer(f)

            # Write the header
            writer.writerow(self.trhheader)

            # Close the file
            f.close()
        # print("Appending data to TRH file")
        # Now open the file and append data
        f = open(filename, 'a')
        writer = csv.writer(f)
        row = []  # Blank list
        # Compile data into list from all sources
        row.append(date1)  # Date
        row.append(time1)  # Time
        row.append(self.trh_sensor.temp_c)  # Ext Temp
        row.append(self.trh_sensor.rh)  # Ext RH
        row.append(self.trh_sensor.dp)  # Dew point
        row.append(self.trh_sensor.s_temp)  # Sensor temp
        row.append(self.trh_sensor.v_mcu)  # VMCU
        row.append(self.trh_sensor.v_supply)  # VSUPPLY
        row.append(self.trh_sensor.v_fan)  # VFAN
        row.append(self.trh_sensor.rssi)
        row.append(self.trh_sensor.snr)
        row.append(self.trh_sensor.m_count)  # Message count

        # Write the row data to the file
        writer.writerow(row)

        # Close the file.  All done.
        f.close()

    def save_base_data(self):
        # print("Saving base data")
        now = datetime.now()
        format = "%d-%m-%Y"
        date1 = now.strftime(format)
        format2 = "%H:%M:%S"
        time1 = now.strftime(format2)
        year1 = now.year
        month1 = now.month
        # print("Year ", year1, " month ", month1)
        filename = "Base"
        if (month1 < 10):
            filename = filename + "0"
        filename = filename + str(month1) + str(year1) + ".txt"
        # print(filename)
        file_exists = exists(filename)
        if not (file_exists):
            # print("Creating new base log file with header...")
            # create file with header
            # open the file in write mode
            f = open(filename, 'w')

            # Create the csv writer
            writer = csv.writer(f)

            # Write the header
            writer.writerow(self.baseheader)

            # Close the file
            f.close()
        # print("Appending data to base file")
        # Now open the file and append data
        f = open(filename, 'a')
        writer = csv.writer(f)
        row = []  # Blank list
        # Compile data into list from all sources
        row.append(date1)  # Date
        row.append(time1)  # Time
        row.append(self.base_sensor.temp_c)  # Int Temp
        row.append(self.base_sensor.rh)  # Int RH
        row.append(self.base_sensor.sea_level_pressure)  # Pressure
        row.append(self.base_sensor.abs_pressure)  # Sensor pressure

        # Write the row data to the file
        writer.writerow(row)

        # Close the file.  All done.
        f.close()

    def save_uvl_data(self):
        # print("Saving UVL data")
        now = datetime.now()
        format = "%d-%m-%Y"
        date1 = now.strftime(format)
        format2 = "%H:%M:%S"
        time1 = now.strftime(format2)
        year1 = now.year
        month1 = now.month
        # print("Year ", year1, " month ", month1)
        filename = "UVL"
        if (month1 < 10):
            filename = filename + "0"
        filename = filename + str(month1) + str(year1) + ".txt"
        # print(filename)
        file_exists = exists(filename)
        if not (file_exists):
            # print("Creating new TRH log file with header...")
            # create file with header
            # open the file in write mode
            f = open(filename, 'w')

            # Create the csv writer
            writer = csv.writer(f)

            # Write the header
            writer.writerow(self.uvlheader)

            # Close the file
            f.close()
        # print("Appending data to TRH file")
        # Now open the file and append data
        f = open(filename, 'a')
        writer = csv.writer(f)
        row = []  # Blank list
        # Compile data into list from all sources
        row.append(date1)  # Date
        row.append(time1)  # Time
        row.append(self.uvl_sensor.visible)  # Visible
        row.append(self.uvl_sensor.uva)  # UVA
        row.append(self.uvl_sensor.uvb)  # UVB
        row.append(self.uvl_sensor.uvi)  # UVI
        row.append(self.uvl_sensor.uv_index)  # UV Index
        row.append(self.uvl_sensor.s_temp)  # Sensor temp
        row.append(self.uvl_sensor.v_mcu)  # VMCU
        row.append(self.uvl_sensor.rssi)
        row.append(self.uvl_sensor.snr)
        row.append(self.uvl_sensor.m_count)  # Message count

        # Write the row data to the file
        writer.writerow(row)

        # Close the file.  All done.
        f.close()

    def save_rain_data(self):
        # print("Saving RAIN data")
        now = datetime.now()
        format = "%d-%m-%Y"
        date1 = now.strftime(format)
        format2 = "%H:%M:%S"
        time1 = now.strftime(format2)
        year1 = now.year
        month1 = now.month
        # print("Year ", year1, " month ", month1)
        filename = "RAIN"
        if (month1 < 10):
            filename = filename + "0"
        filename = filename + str(month1) + str(year1) + ".txt"
        # print(filename)
        file_exists = exists(filename)
        if not (file_exists):
            # print("Creating new RAIN log file with header...")
            # create file with header
            # open the file in write mode
            f = open(filename, 'w')

            # Create the csv writer
            writer = csv.writer(f)

            # Write the header
            writer.writerow(self.rainheader)

            # Close the file
            f.close()
        # print("Appending data to RAIN file")
        # Now open the file and append data
        f = open(filename, 'a')
        writer = csv.writer(f)
        row = []  # Blank list
        # Compile data into list from all sources
        row.append(date1)  # Date
        row.append(time1)  # Time
        row.append(self.rainfall_sensor.rain_mm)  # Today's rainfall
        row.append(self.rainfall_sensor.rain_tips)  # Sensor total tips
        row.append(self.rainfall_sensor.rain_rate)  # Rainfall rate
        row.append(self.rainfall_sensor.s_temp)  # Sensor temp
        row.append(self.rainfall_sensor.v_mcu)  # VMCU
        row.append(self.rainfall_sensor.rssi)
        row.append(self.rainfall_sensor.snr)
        row.append(self.rainfall_sensor.m_count)  # Message count

        # Write the row data to the file
        writer.writerow(row)

        # Close the file.  All done.
        f.close()

    def save_sferic_data(self):
        # print("Saving SF data")
        now = datetime.now()
        format = "%d-%m-%Y"
        date1 = now.strftime(format)
        format2 = "%H:%M:%S"
        time1 = now.strftime(format2)
        year1 = now.year
        month1 = now.month
        # print("Year ", year1, " month ", month1)
        filename = "SF"
        if (month1 < 10):
            filename = filename + "0"
        filename = filename + str(month1) + str(year1) + ".txt"
        # print(filename)
        file_exists = exists(filename)
        if not (file_exists):
            # print("Creating new SFERIC log file with header...")
            # create file with header
            # open the file in write mode
            f = open(filename, 'w')

            # Create the csv writer
            writer = csv.writer(f)

            # Write the header
            writer.writerow(self.sfericheader)

            # Close the file
            f.close()
        # print("Appending data to SFERIC file")
        # Now open the file and append data
        f = open(filename, 'a')
        writer = csv.writer(f)
        row = []  # Blank list
        # Compile data into list from all sources
        row.append(date1)  # Date
        row.append(time1)  # Time
        row.append(self.sferic_sensor.count1)  # Total count 1
        row.append(self.sferic_sensor.count2)  # Total count 2
        row.append(self.sferic_sensor.today_count1)  # Today count 1
        row.append(self.sferic_sensor.today_count2)  # Today count 2
        row.append(self.sferic_sensor.s_temp)  # Sensor temp
        row.append(self.sferic_sensor.v_mcu)  # VMCU
        row.append(self.sferic_sensor.rssi)
        row.append(self.sferic_sensor.snr)
        row.append(self.sferic_sensor.m_count)  # Message count

        # Write the row data to the file
        writer.writerow(row)

        # Close the file.  All done.
        f.close()

    def save_wind_data(self):
        # print("Saving WIND data")
        now = datetime.now()
        format = "%d-%m-%Y"
        date1 = now.strftime(format)
        format2 = "%H:%M:%S"
        time1 = now.strftime(format2)
        year1 = now.year
        month1 = now.month
        # print("Year ", year1, " month ", month1)
        filename = "WIND"
        if (month1 < 10):
            filename = filename + "0"
        filename = filename + str(month1) + str(year1) + ".txt"
        # print(filename)
        file_exists = exists(filename)
        if not (file_exists):
            # print("Creating new WIND log file with header...")
            # create file with header
            # open the file in write mode
            f = open(filename, 'w')

            # Create the csv writer
            writer = csv.writer(f)

            # Write the header
            writer.writerow(self.windheader)

            # Close the file
            f.close()
        # print("Appending data to WIND file")
        # Now open the file and append data
        f = open(filename, 'a')
        writer = csv.writer(f)
        row = []  # Blank list
        # Compile data into list from all sources
        row.append(date1)  # Date
        row.append(time1)  # Time
        row.append(self.wind_sensor.speed)  # Current wind speed
        row.append(self.wind_sensor.gust)  # Latest wind gust
        row.append(self.wind_sensor.direction)  # Latest wind direction
        row.append(self.wind_sensor.s_temp)  # Sensor temp
        row.append(self.wind_sensor.v_mcu)  # VMCU
        row.append(self.wind_sensor.rssi)
        row.append(self.wind_sensor.snr)
        row.append(self.wind_sensor.m_count)  # Message count

        # Write the row data to the file
        writer.writerow(row)

        # Close the file.  All done.
        f.close()

    def save_day_log(self):
        # global trh_sensor, rainfall_sensor
        # print("Saving dayFile.txt")
        now = datetime.now()
        format = "%d-%m-%Y"
        date1 = now.strftime(format)

        file_exists = exists(self.daylogfilename)
        if not (file_exists):
            # print("Creating new day file with header...")
            # create file with header
            # open the file in write mode
            f = open(self.daylogfilename, 'w')

            # Create the csv writer
            writer = csv.writer(f)

            # Write the header
            writer.writerow(self.dayfileheader)

            # Close the file
            f.close()

        # print("Appending data to TRH file")
        # Now open the file and append data
        f = open(self.daylogfilename, 'a')
        writer = csv.writer(f)
        row = []  # Blank list
        # Compile data into list from all sources
        row.append(date1)  # Date
        row.append(self.wind_sensor.max_gust)  # Max Gust
        row.append(self.wind_sensor.max_gust_dir)  # Max Gust bearing
        row.append(self.wind_sensor.max_gust_time)  # Max Gust time
        row.append(self.trh_sensor.min_temp_c)  # Min ext temp
        row.append(self.trh_sensor.min_temp_time)  # Min ext temp time
        row.append(self.trh_sensor.max_temp_c)  # Max ext temp
        row.append(self.trh_sensor.max_temp_time)  # Max ext temp time
        row.append(self.base_sensor.min_slp)  # Min sea level pressure
        row.append(self.base_sensor.min_slp_time)  # Min SLP time
        row.append(self.base_sensor.max_slp)  # Max sea level pressure
        row.append(self.base_sensor.max_slp_time)  # Max SLP time
        row.append(self.rainfall_sensor.max_rain_rate)  # Max rain rate
        row.append(self.rainfall_sensor.max_rain_rate_time)  # Max rain rate time
        row.append(self.rainfall_sensor.rain_mm)  # Today's rainfall
        row.append(self.trh_sensor.av_temp)  # Average temperature
        row.append(self.wind_sensor.wind_run)  # Wind run
        row.append(self.wind_sensor.max_speed)  # Max Average windspeed
        row.append(self.wind_sensor.max_speed_time)  # Max average windspeed time
        row.append(self.trh_sensor.min_rh) # Lowest RH
        row.append(self.trh_sensor.min_rh_time) # Time of lowest RH
        row.append(self.trh_sensor.max_rh) # Highest RH
        row.append(self.trh_sensor.max_rh_time) # Time of highest RH
        row.append(0) # Total evapotranspiration
        row.append(0) # Total sunshine hours
        row.append(heat_index_sensor.max_heat_index) # High heat index
        row.append(heat_index_sensor.max_heat_index_time) # Time of high heat index
        row.append(apparent_temp_sensor.max_app_temp) # High apparent temperature
        row.append(apparent_temp_sensor.max_app_temp_time) # Time of high apparent temperature
        row.append(apparent_temp_sensor.min_app_temp) # Low apparent temperature
        row.append(apparent_temp_sensor.min_app_temp_time) # Time of low apparent temperature
        row.append(0) # High hourly rain
        row.append(0) # Time of high hourly rain
        row.append(wind_chill_sensor.min_wind_chill) # Greatest wind chill
        row.append(wind_chill_sensor.min_wind_chill_time) # Time of greatest wind chill
        row.append(trh_sensor.max_dp) # High dew point
        row.append(trh_sensor.max_dp_time) # Time of high dew point
        row.append(trh_sensor.min_dp) # Low dew point
        row.append(trh_sensor.min_dp_time) # Time of low dew point
        row.append(0) # Today's dominant wind direction
        row.append(0) # Heating degree days
        row.append(0) # Cooling degree days
        row.append(0) # High solar radiation
        row.append(0) # Time of high solar radiation
        row.append(uvl_sensor.max_uv_index) # High UV index
        row.append(uvl_sensor.max_uv_index_time) # Time of high UV index
        row.append(0) # High feels like temperature
        row.append(0) # Time of high feels like temperature
        row.append(0) # Low feels like temperature
        row.append(0) # Time of low feels like temperature
        row.append(0) # High Canadian humidex
        row.append(0) # Time of high Canadian humidex
        row.append(0) # Low Canadian humidex
        row.append(0) # Time of low humidex
        row.append(0) # Cumulative chill hours
        row.append(uvl_sensor.max_uva) # UVA MAX
        row.append(uvl_sensor.max_uva_time) # UVA MAX TIME
        row.append(uvl_sensor.max_uvb) # UVB MAX
        row.append(uvl_sensor.max_uvb_time) # UVB MAX TIME
        row.append(uvl_sensor.max_uvi) # UVI MAX
        row.append(uvl_sensor.max_uvi_time) # UVI MAX TIME
        row.append(uvl_sensor.max_visible) # VIS MAX
        row.append(uvl_sensor.max_visible_time) # VIS MAX TIME
        row.append(sferic_sensor.today_count1) # SF1 TOT
        row.append(sferic_sensor.today_count2) # SF2 TOT
        row.append(0) # SF1 MAX RATE
        row.append(0) # SF1 MAX RATE TIME
        row.append(0) # SF2 MAX RATE
        row.append(0) # SF2 MAX RATE TIME
        row.append(0) # RAD MAX
        row.append(0) # RAD MAX TIME
        row.append(0) # EF MAX
        row.append(0) # EF MAX TIME
        row.append(0) # EF MIN
        row.append(0) # EF MIN TIME

        # Write the row data to the file
        writer.writerow(row)

        # Close the file.  All done.
        f.close()
