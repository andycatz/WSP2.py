import datetime


class WindChill:
    wind_chill = 0.0
    wind_chill_valid = 0  # Wind chill is only valid if this is 1 (if ta and v were both valid)
    min_wind_chill = 0.0
    first = 0
    min_wind_chill_time = "00:00:00"

    # Checks if minimum wind chill has been exceeded, if so update and record time of occurrence.
    def check_min_wind_chill(self):
        now = datetime.datetime.now()
        fmt = "%H:%M:%S"
        time1 = now.strftime(fmt)
        if self.first == 1 and self.wind_chill_valid == 1:
            if self.wind_chill < self.min_wind_chill:
                self.min_wind_chill = self.wind_chill
                self.min_wind_chill_time = time1  # Record the time of occurrence
        else:
            if self.wind_chill_valid == 1:
                self.min_wind_chill = self.wind_chill
                self.first = 1
                self.min_wind_chill_time = time1

    # Resets the minimum wind chill - call at end of day
    def reset_min_wind_chill(self):
        now = datetime.datetime.now()
        fmt = "%H:%M:%S"
        time1 = now.strftime(fmt)
        self.min_wind_chill = self.wind_chill
        self.min_wind_chill_time = time1

    # Calculates the wind chill in degrees Celsius from
    # air temperature in degrees Celsius and wind velocity
    # in km/h.  This is the North American (Canada & U.S.) and U.K. version.
    def calculate_wind_chill(self, ta, v):
        twc = 13.12 + 0.6215 * ta - 11.37 * v ** 0.16 + 0.3965 * ta * v ** 0.16
        return twc
