# Base Sensor

import datetime
from matplotlib import pyplot as plt
import bme280
import smbus2
import json
import os.path


class Base:
    temp_c = 0.0
    rh = 0.0
    sea_level_pressure = 0.0
    abs_pressure = 0.0
    max_slp = 0.0
    min_slp = 0.0
    max_slp_time = "00:00:00"
    min_slp_time = "00:00:00"
    max_temp_c = 0.0
    min_temp_c = 0.0
    max_temp_time = "00:00:00"
    min_temp_time = "00:00:00"
    max_rh = 0.0
    min_rh = 0.0
    max_rh_time = "00:00:00"
    min_rh_time = "00:00:00"
    first = 0
    pressure_rate = 0.0
    pressure_offset = 1.0

    # Data structure with all the max/mins in it.
    basedict = {
        "timestamp": "01/01/00 00:00:00",
        "max_slp": 0.0,
        "min_slp": 0.0,
        "max_slp_time": "00:00:00",
        "min_slp_time": "00:00:00",
        "max_temp_c": 0.0,
        "min_temp_c": 0.0,
        "max_temp_time": "00:00:00",
        "min_temp_time": "00:00:00",
        "max_rh": 0.0,
        "min_rh": 0.0,
        "max_rh_time": "00:00:00",
        "min_rh_time": "00:00:00",
        "pressure_rate": 0.0,
        "max_pressure_rate": 0.0,
        "min_pressure_rate": 0.0,
        "yest_max_slp": 0.0,
        "yest_min_slp": 0.0,
        "yest_max_temp_c": 0.0,
        "yest_min_temp_c": 0.0,
        "yest_max_temp_time": "00:00:00",
        "yest_min_temp_time": "00:00:00",
        "yest_max_rh": 0.0,
        "yest_min_rh": 0.0,
        "yest_max_rh_time": "00:00:00",
        "yest_min_rh_time": "00:00:00",
        "month_max_slp": 0.0,
        "month_min_slp": 0.0,
        "month_max_slp_time": "00:00:00",
        "month_min_slp_time": "00:00:00",
        "year_max_slp": 0.0,
        "year_min_slp": 0.0,
        "year_max_slp_time": "00:00:00",
        "year_min_slp_time": "00:00:00",
        "alltime_max_slp": 0.0,
        "alltime_min_slp": 0.0,
        "alltime_max_slp_time": "00:00:00",
        "alltime_min_slp_time": "00:00:00",
        "month_max_temp_c": 0.0,
        "month_min_temp_c": 0.0,
        "month_max_temp_time": "00:00:00",
        "month_min_temp_time": "00:00:00",
        "year_max_temp_c": 0.0,
        "year_min_temp_c": 0.0,
        "year_max_temp_time": "00:00:00",
        "year_min_temp_time": "00:00:00",
        "alltime_max_temp_c": 0.0,
        "alltime_min_temp_c": 0.0,
        "alltime_max_temp_time": "00:00:00",
        "alltime_min_temp_time": "00:00:00",
        "month_max_rh": 0.0,
        "month_min_rh": 0.0,
        "month_max_rh_time": "00:00:00",
        "month_min_rh_time": "00:00:00",
        "year_max_rh": 0.0,
        "year_min_rh": 0.0,
        "year_max_rh_time": "00:00:00",
        "year_min_rh_time": "00:00:00",
        "alltime_max_rh": 0.0,
        "alltime_min_rh": 0.0,
        "alltime_max_rh_time": "00:00:00",
        "alltime_min_rh_time": "00:00:00"

    }

    def __init__(self):
        self.temp_data = []
        self.rh_data = []
        self.slp_data = []
        self.x_times = []
        self.port = 1
        self.address = 0x76
        self.bus = smbus2.SMBus(self.port)
        bme280.load_calibration_params(self.bus, self.address)

    # Returns the current temperature in degrees Farenheit
    def get_temp_F(self):
        return self.temp_c * 9 / 5 + 32

    def update(self):
        self.check_max_min()
        self.calculate_pressure_rate()
        self.check_max_min_temp_dict()
        self.check_max_min_rh_dict()
        self.check_max_min_slp_dict()

    # Checks if today's maximum or minimum have been exceeded
    # and updates them if required.
    def check_max_min(self):
        now = datetime.datetime.now()
        fmt = "%H:%M:%S"
        time1 = now.strftime(fmt)
        if self.first == 0:
            self.max_temp_c = self.temp_c
            self.min_temp_c = self.temp_c
            self.max_temp_time = time1
            self.min_temp_time = time1
            self.max_rh = self.rh
            self.min_rh = self.rh
            self.max_rh_time = time1
            self.min_rh_time = time1
            self.max_slp = self.sea_level_pressure
            self.min_slp = self.sea_level_pressure
            self.max_slp_time = time1
            self.min_slp_time = time1
            self.first = 1
        else:
            if self.temp_c > self.max_temp_c:
                self.max_temp_c = self.temp_c
                self.max_temp_time = time1
            if self.temp_c < self.min_temp_c:
                self.min_temp_c = self.temp_c
                self.min_temp_time = time1
            if self.rh > self.max_rh:
                self.max_rh = self.rh
                self.max_rh_time = time1
            if self.rh < self.min_rh:
                self.min_rh = self.rh
                self.min_rh_time = time1
            if self.sea_level_pressure > self.max_slp:
                self.max_slp = self.sea_level_pressure
                self.max_slp_time = time1
            if self.sea_level_pressure < self.min_slp:
                self.min_slp = self.sea_level_pressure
                self.min_slp_time = time1

    # Checks the max/min temperatures in the dictionary and updates accordingly
    def check_max_min_temp_dict(self):
        now = datetime.datetime.now()
        fmt = "%H:%M:%S"
        fmt2 = "%d/%m/%Y, %H:%M:%S"
        time1 = now.strftime(fmt)   # Time only
        time2 = now.strftime(fmt2)  # Date and time
        if self.temp_c > self.basedict["max_temp_c"]:
            self.basedict["max_temp_c"] = self.temp_c
            self.basedict["max_temp_time"] = time1

        if self.temp_c < self.basedict["min_temp_c"]:
            self.basedict["min_temp_c"] = self.temp_c
            self.basedict["min_temp_time"] = time1

        if self.temp_c > self.basedict["month_max_temp_c"]:
            self.basedict["month_max_temp_c"] = self.temp_c
            self.basedict["month_max_temp_time"] = time2

        if self.temp_c < self.basedict["month_min_temp_c"]:
            self.basedict["month_min_temp_c"] = self.temp_c
            self.basedict["month_min_temp_time"] = time2
            
        if self.temp_c > self.basedict["year_max_temp_c"]:
            self.basedict["year_max_temp_c"] = self.temp_c
            self.basedict["year_max_temp_time"] = time2

        if self.temp_c < self.basedict["year_min_temp_c"]:
            self.basedict["year_min_temp_c"] = self.temp_c
            self.basedict["year_min_temp_time"] = time2
            
        if self.temp_c > self.basedict["alltime_max_temp_c"]:
            self.basedict["alltime_max_temp_c"] = self.temp_c
            self.basedict["alltime_max_temp_time"] = time2

        if self.temp_c < self.basedict["alltime_min_temp_c"]:
            self.basedict["alltime_min_temp_c"] = self.temp_c
            self.basedict["alltime_min_temp_time"] = time2

    # Checks the max/min RHs in the dictionary and updates accordingly
    def check_max_min_rh_dict(self):
        now = datetime.datetime.now()
        fmt = "%H:%M:%S"
        fmt2 = "%d/%m/%Y, %H:%M:%S"
        time1 = now.strftime(fmt)  # Time only
        time2 = now.strftime(fmt2)  # Date and time
        if self.rh > self.basedict["max_rh"]:
            self.basedict["max_rh"] = self.rh
            self.basedict["max_rh_time"] = time1

        if self.rh < self.basedict["min_rh"]:
            self.basedict["min_rh"] = self.rh
            self.basedict["min_rh_time"] = time1

        if self.rh > self.basedict["month_max_rh"]:
            self.basedict["month_max_rh"] = self.rh
            self.basedict["month_max_rh_time"] = time2

        if self.rh < self.basedict["month_min_rh"]:
            self.basedict["month_min_rh"] = self.rh
            self.basedict["month_min_rh_time"] = time2

        if self.rh > self.basedict["year_max_rh"]:
            self.basedict["year_max_rh"] = self.rh
            self.basedict["year_max_rh_time"] = time2

        if self.rh < self.basedict["year_min_rh"]:
            self.basedict["year_min_rh"] = self.temp_c
            self.basedict["year_min_rh_time"] = time2

        if self.rh > self.basedict["alltime_max_rh"]:
            self.basedict["alltime_max_rh"] = self.rh
            self.basedict["alltime_max_rh_time"] = time2

        if self.rh < self.basedict["alltime_min_rh"]:
            self.basedict["alltime_min_rh"] = self.rh
            self.basedict["alltime_min_rh_time"] = time2
            
    # Checks the max/min sea level pressures in the dictionary and updates accordingly
    def check_max_min_slp_dict(self):
        now = datetime.datetime.now()
        fmt = "%H:%M:%S"
        fmt2 = "%d/%m/%Y, %H:%M:%S"
        time1 = now.strftime(fmt)  # Time only
        time2 = now.strftime(fmt2)  # Date and time
        if self.sea_level_pressure > self.basedict["max_slp"]:
            self.basedict["max_slp"] = self.sea_level_pressure
            self.basedict["max_slp_time"] = time1

        if self.sea_level_pressure < self.basedict["min_slp"]:
            self.basedict["min_slp"] = self.sea_level_pressure
            self.basedict["min_slp_time"] = time1

        if self.sea_level_pressure > self.basedict["month_max_slp"]:
            self.basedict["month_max_slp"] = self.sea_level_pressure
            self.basedict["month_max_slp_time"] = time2

        if self.sea_level_pressure < self.basedict["month_min_slp"]:
            self.basedict["month_min_slp"] = self.sea_level_pressure
            self.basedict["month_min_slp_time"] = time2

        if self.sea_level_pressure > self.basedict["year_max_slp"]:
            self.basedict["year_max_slp"] = self.sea_level_pressure
            self.basedict["year_max_slp_time"] = time2

        if self.sea_level_pressure < self.basedict["year_min_slp"]:
            self.basedict["year_min_slp"] = self.sea_level_pressure
            self.basedict["year_min_slp_time"] = time2

        if self.sea_level_pressure > self.basedict["alltime_max_slp"]:
            self.basedict["alltime_max_slp"] = self.sea_level_pressure
            self.basedict["alltime_max_slp_time"] = time2

        if self.sea_level_pressure < self.basedict["alltime_min_slp"]:
            self.basedict["alltime_min_slp"] = self.sea_level_pressure
            self.basedict["alltime_min_slp_time"] = time2

    def save_dict(self):
        now = datetime.datetime.now()
        fmt = "%d/%m/%Y, %H:%M:%S"
        time1 = now.strftime(fmt)
        self.basedict["timestamp"] = time1
        with open('base.json', 'w') as fp:
            json.dump(self.basedict, fp)

    def load_dict(self):
        print("Loading base.json")
        if os.path.exists('base.json'):
            with open('base.json', 'r') as fp:
                self.basedict = json.load(fp)
            print("Done loading base.json")
        else:
            print("base.json does not exist")

    # Call this at end of day to reset the day max and mins
    def reset_max_min(self):
        now = datetime.datetime.now()
        fmt = "%H:%M:%S"
        time1 = now.strftime(fmt)
        self.max_temp_c = self.temp_c
        self.min_temp_c = self.temp_c
        self.max_temp_time = time1
        self.min_temp_time = time1
        self.max_rh = self.rh
        self.min_rh = self.rh
        self.max_rh_time = time1
        self.min_rh_time = time1
        self.max_slp = self.sea_level_pressure
        self.min_slp = self.sea_level_pressure
        self.max_slp_time = time1
        self.min_slp_time = time1

    # Adds current data to all the internal lists and adds the
    # current timestamp to the x_times list
    def add_data(self):
        if len(self.temp_data) > 1440:
            self.temp_data.pop(0)
            self.rh_data.pop(0)
            self.slp_data.pop(0)
            self.x_times.pop(0)
        # Add new data to end of lists
        self.temp_data.append(self.temp_c)
        self.rh_data.append(self.rh)
        self.slp_data.append(self.sea_level_pressure)
        self.x_times.append(datetime.datetime.now())
        # print("Base sensor data stored")

    def draw_pressure_graph(self, plot_to_file=False, file_name=""):
        plt.plot(self.x_times, self.slp_data)
        plt.gcf().autofmt_xdate()
        plt.xlabel("Time")
        plt.ylabel("SLP (hPa)")
        fig = plt.gcf()
        fig.canvas.set_window_title("Sea Level Pressure 24-hour Graph")
        if plot_to_file == True:
            plt.savefig(file_name)
            plt.clf()
            plt.close(fig)
        else:
            plt.show()

    def draw_temp_graph(self, plot_to_file=False, file_name=""):
        plt.plot(self.x_times, self.temp_data)
        plt.gcf().autofmt_xdate()
        plt.xlabel("Time")
        plt.ylabel("Temperature (\N{DEGREE SIGN} C)")
        fig = plt.gcf()
        fig.canvas.set_window_title("Indoor Temperature 24-hour Graph")
        if plot_to_file == True:
            plt.savefig(file_name)
            plt.clf()
            plt.close(fig)
        else:
            plt.show()

    def draw_rh_graph(self, plot_to_file=False, file_name=""):
        plt.plot(self.x_times, self.rh_data)
        plt.gcf().autofmt_xdate()
        plt.xlabel("Time")
        plt.ylabel("RH (%)")
        fig = plt.gcf()
        fig.canvas.set_window_title("Indoor Relative Humidity 24-hour Graph")
        if plot_to_file == True:
            plt.savefig(file_name)
            plt.clf()
            plt.close(fig)
        else:
            plt.show()

    # The rate we require is pressure change in hPa per hour but over a 3-hour period.
    # self.slp_data holds historical pressure data for up to the last 24 hours.
    # When the program starts however, it will be empty and will slowly build up data.
    # Newest data is at the highest index, oldest data is at index 0
    def calculate_pressure_rate(self):
        # First determine whether there is any data and whether there is 3 hours or more of data
        oldest = 0
        length = len(self.slp_data)  # Length of pressure data - this will be in minutes
        if length > 0:
            # Some data available

            if len(self.slp_data) > 180:
                # More than 3 hours of data available
                newest = self.slp_data[-1]  # The newest value entered into the list
                three_hours_ago = self.slp_data[-181]  # The value 3 hours ago
                change = newest - three_hours_ago
                self.pressure_rate = change / 3  # Pressure rate averaged over three hours
            else:
                oldest = self.slp_data[0]  # The oldest recorded value
                newest = self.slp_data[-1]  # The newest recorded value
                change = newest - oldest  # Pressure change
                self.pressure_rate = change / length * 60  # Pressure rate
        # print("Pressure rate ", self.pressure_rate)

    def get_data(self):
        bme280_data = bme280.sample(self.bus, self.address)
        self.rh = bme280_data.humidity
        self.sea_level_pressure = bme280_data.pressure + self.pressure_offset
        self.temp_c = bme280_data.temperature

    # Returns a description of the rate of change of pressure given a
    # rate of change in hPa/hour
    def get_pressure_rate_description(self, rate):
        ret_string = "steady"
        if rate>0.1 and rate<1.6:
            ret_string = "rising slowly"
        elif rate>=1.6 and rate<3.6:
            ret_string = "rising"
        elif rate>=3.6 and rate<6:
            ret_string = "rising quickly"
        elif rate>=6:
            ret_string = "rising very rapidly"
        elif rate<-0.1 and rate>-1.6:
            ret_string = "falling slowly"
        elif rate<=-1.6 and rate>-3.6:
            ret_string = "falling"
        elif rate<=-3.6 and rate>-6:
            ret_string = "falling quickly"
        elif rate<=-6:
            ret_string = "falling very rapidly"
        return ret_string

    # Resets the monthly max/min temp.  Call this if you need to reset,
    # particularly when starting fresh if it doesn't do this automatically
    # or if there is an error.  It resets them to current internal temperature.
    def reset_month_max_min_temp(self):
        print("Int Temp Month Max/Min Temp Reset")
        now = datetime.datetime.now()
        fmt2 = "%d/%m/%Y, %H:%M:%S"
        time2 = now.strftime(fmt2)  # Date and time
        self.basedict["month_max_temp_c"] = self.temp_c
        self.basedict["month_max_temp_time"] = time2
        self.basedict["month_min_temp_c"] = self.temp_c
        self.basedict["month_min_temp_time"] = time2

    # Resets the yearly max/min temp.  Call this if you need to reset,
    # particularly when starting fresh if it doesn't do this automatically
    # or if there is an error.  It resets them to current internal temperature.
    def reset_year_max_min_temp(self):
        print("Int Temp Year Max/Min Temp Reset")
        now = datetime.datetime.now()
        fmt2 = "%d/%m/%Y, %H:%M:%S"
        time2 = now.strftime(fmt2)  # Date and time
        self.basedict["year_max_temp_c"] = self.temp_c
        self.basedict["year_max_temp_time"] = time2
        self.basedict["year_min_temp_c"] = self.temp_c
        self.basedict["year_min_temp_time"] = time2

    # Resets the all time max/min temp.  Call this if you need to reset,
    # particularly when starting fresh if it doesn't do this automatically
    # or if there is an error.  It resets them to current internal temperature.
    def reset_alltime_max_min_temp(self):
        print("Int Temp All Time Max/Min Temp Reset")
        now = datetime.datetime.now()
        fmt2 = "%d/%m/%Y, %H:%M:%S"
        time2 = now.strftime(fmt2)  # Date and time
        self.basedict["alltime_max_temp_c"] = self.temp_c
        self.basedict["alltime_max_temp_time"] = time2
        self.basedict["alltime_min_temp_c"] = self.temp_c
        self.basedict["alltime_min_temp_time"] = time2

    # Resets the monthly max/min pressure.  Call this if you need to reset,
    # particularly when starting fresh if it doesn't do this automatically
    # or if there is an error.  It resets them to current pressure.
    def reset_month_max_min_pressure(self):
        print("Int Temp Year Max/Min Temp Reset")
        now = datetime.datetime.now()
        fmt2 = "%d/%m/%Y, %H:%M:%S"
        time2 = now.strftime(fmt2)  # Date and time
        self.basedict["year_max_slp"] = self.sea_level_pressure
        self.basedict["year_max_slp_time"] = time2
        self.basedict["year_min_slp"] = self.sea_level_pressure
        self.basedict["year_min_slp_time"] = time2
