from Location import Location
from datetime import datetime, date
import math


class TimeAndSpace:

    def __init__(self):
        pass

    def get_latitude_radians(self):
        lat = Location.latitude
        return math.radians(lat)

    # Gets the day of the year 1 to 366
    def get_day_of_year(self):
        day_of_year = datetime.now().timetuple().tm_yday
        return day_of_year

    # Gets the inverse relative distance Earth-Sun dr
    def get_inverse_relative_distance_earth_sun(self):
        j = self.get_day_of_year()
        dr = 1 + 0.033 * math.cos((2 * math.pi) * j / 365)
        return dr

    # Gets the solar declination d
    def get_solar_declination(self):
        j = self.get_day_of_year()
        d = 0.409 * math.sin((2 * math.pi) * j / 365 - 1.39)
        return d

    # Gets the sunset hour angle ws
    def get_sunset_hour_angle(self):
        phi = self.get_latitude_radians()
        d = self.get_solar_declination()
        ws = math.acos(-math.tan(phi) * math.tan(d))
        return ws

    # Gets extraterrestrial radiation
    def get_et_radiation(self):
        ws = self.get_sunset_hour_angle()
        d = self.get_solar_declination()
        dr = self.get_inverse_relative_distance_earth_sun()
        phi = self.get_latitude_radians()
        a = math.sin(phi) * math.sin(d)
        b = math.cos(phi) * math.cos(d)
        gsc = 0.0820    # Solar constant 0.0820 MJ/m2 per minute
        ra = 24 * 60/math.pi * gsc * dr * (ws * a + b * math.sin(ws))
        return ra

    # Get daylight hours
    def get_daylight_hours(self):
        ws = self.get_sunset_hour_angle()
        print("WS ", ws)
        n = 24.0/math.pi * ws
        return n

