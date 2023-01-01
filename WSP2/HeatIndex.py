# HeatIndex.py
import datetime


# Convert Farenheit to Celsius
def get_temp_C(tf):
    return (tf - 32) * 5 / 9


class HeatIndex:
    first = 0
    heat_index_C = 0.0
    heat_index_valid = 0
    max_heat_index = 0.0
    min_heat_index = 0.0
    max_heat_index_time = "--:--:--"
    min_heat_index_time = "--:--:--"
    # Constants for calculate heat index in degrees Farenheit
    C1f = -42.379
    C2f = 2.04901523
    C3f = 10.14333127
    C4f = -0.22475541
    C5f = -6.83783e-3
    C6f = -5.481717e-2
    C7f = 1.22874e-3
    C8f = 8.5282e-4
    C9f = -1.99e-6

    # Constants for calculating heat index in degrees Celsius
    C1c = -8.78469475556
    C2c = 1.61139411
    C3c = 2.33854883889
    C4c = -0.14611605
    C5c = -0.012308094
    C6c = -0.0164248277778
    C7c = 2.211732e-3
    C8c = 7.2546e-4
    C9c = -3.582e-6

    # Checks if maxmimum or minimum has been exceeded, if so update and record time of occurrence.
    def check_max_min(self):
        now = datetime.datetime.now()
        fmt = "%H:%M:%S"
        time1 = now.strftime(fmt)
        if self.first == 1 and self.heat_index_valid == 1:
            if self.heat_index_C < self.min_heat_index:
                self.min_heat_index = self.heat_index_C
                self.min_heat_index_time = time1  # Record the time of occurrence
            if self.heat_index_C > self.max_heat_index:
                self.max_heat_index = self.heat_index_C
                self.max_heat_index_time = time1  # Record the time of occurrence
        else:
            if self.heat_index_valid == 1:
                self.min_heat_index = self.heat_index_C
                self.first = 1
                self.min_heat_index_time = time1
                self.max_heat_index = self.heat_index_C
                self.max_heat_index_time = time1

    # Resets the minimum and maximum - call at end of day
    def reset_max_min(self):
        now = datetime.datetime.now()
        fmt = "%H:%M:%S"
        time1: str = now.strftime(fmt)
        self.max_heat_index = self.heat_index_C
        self.max_heat_index_time = time1
        self.min_heat_index = self.heat_index_C
        self.min_heat_index_time = time1

    # Calculates heat index from temperature tf in degrees Farenheit
    # and relative humidity.  Returns heat index value in degrees Farenheit
    def calculate_heat_index_F(self, tf, rh):
        hi = self.C1f + self.C2f * tf + self.C3f * rh + self.C4f * tf * rh + self.C5f * tf * tf + self.C6f * rh * rh + self.C7f * tf * tf * rh + self.C8f * tf * rh * rh + self.C9f * tf * tf * rh * rh
        return hi

    # Calculates heat index from temperature tc in degrees Celsius
    # and relative humidity.  Returns heat index value in degrees Celsius.
    def calculate_heat_index_C(self, tc, rh):
        hi = self.C1c + self.C2c * tc + self.C3c * rh + self.C4c * tc * rh + self.C5c * tc * tc + self.C6c * rh * rh + self.C7c * tc * tc * rh + self.C8c * tc * rh * rh + self.C9c * tc * tc * rh * rh
        return hi

    # Returns a textual warning level depending on the value of the heat index
    def get_heat_index_warning(self, hi):
        if hi < 27:
            return "OK"
        elif 27 <= hi < 33:
            return "Caution"
        elif 33 <= hi < 40:
            return "Extreme Caution"
        elif 40 <= hi < 52:
            return "Danger"
        else:
            return "Extreme Danger"
