# Apparent temperature, also includes "feels like" temperature

import datetime
import math


class ApparentTemp:
    app_temp = 0.0
    app_temp_valid = 0  # Apparent Temperature is only valid if this is 1 (if ta and v were both valid)
    max_app_temp = 0.0
    min_app_temp = 0.0
    first = 0
    max_app_temp_time = "00:00:00"
    min_app_temp_time = "00:00:00"

    feels_like = 0.0
    feels_like_valid = 0
    max_feels_like = 0.0
    min_feels_like = 0.0
    max_feels_like_time = "00:00:00"
    min_feels_like_time = "00:00:00"
    feels_like_first = 0

    # Checks if maxmimum or minimum has been exceeded, if so update and record time of occurrence.
    def check_max_min(self):
        now = datetime.datetime.now()
        fmt = "%H:%M:%S"
        time1 = now.strftime(fmt)
        if self.first == 1 and self.app_temp_valid == 1:
            if self.app_temp < self.min_app_temp:
                self.min_app_temp = self.app_temp
                self.min_app_temp_time = time1  # Record the time of occurrence
            if self.app_temp > self.max_app_temp:
                self.max_app_temp = self.app_temp
                self.max_app_temp_time = time1  # Record the time of occurrence
        else:
            if self.app_temp_valid == 1:
                self.min_app_temp = self.app_temp
                self.first = 1
                self.min_app_temp_time = time1
                self.max_app_temp = self.app_temp
                self.max_app_temp_time = time1

        if self.feels_like_first == 1 and self.feels_like_valid == 1:
            if self.feels_like < self.min_feels_like:
                self.min_feels_like = self.feels_like
                self.min_feels_like_time = time1  # Record the time of occurrence
            if self.feels_like > self.max_feels_like:
                self.max_feels_like = self.feels_like
                self.max_feels_like_time = time1  # Record the time of occurrence
        else:
            if self.feels_like_valid == 1:
                self.min_feels_like = self.feels_like
                self.feels_like_first = 1
                self.min_feels_like_time = time1
                self.max_feels_like = self.feels_like
                self.max_feels_like_time = time1

    # Resets the minimum and maximum - call at end of day
    def reset_max_min(self):
        now = datetime.datetime.now()
        fmt = "%H:%M:%S"
        time1 = now.strftime(fmt)
        self.max_app_temp = self.app_temp
        self.max_app_temp_time = time1
        self.min_app_temp = self.app_temp
        self.min_app_temp_time = time1
        self.max_feels_like = self.feels_like
        self.max_feels_like_time = time1
        self.min_feels_like = self.feels_like
        self.min_feels_like_time = time1

    # Calculate apparent temperature, ta from ambient temperature ta in degrees celsius,
    # wind velocity, v in meters per second
    # and relative humidity, rh in %
    def calculate_app_temp(self, ta, v, rh):
        e = rh / 100 * 6.105 * math.exp(17.27*ta/(237.7+ta))  # Calculate water vapour pressure
        at = ta + 0.33 * e - 0.7 * v - 4.00     # Calculate apparent temperature
        return at

    # Calculate "feels like" temperature, ta from ambient temperature ta in degrees celsius,
    # wind velocity, v in meters per second
    # and relative humidity, rh in %
    # See JAG/TI-2000 (Environment Canada/US NWS) (Wind chill).  Also valid in the UK.
    # Valid for temps from -46deg C to +10deg C and for wind speeds from 1.3 to 49.0ms-1
    def calculate_feels_like_temp(self, ta, v, rh):
        g = 13.12 + 0.6215 * ta - 11.37 * (v * 3.6)**0.16 + 0.3965 * ta * (v * 3.6) * 2.3**0.16
        return g
