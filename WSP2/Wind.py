import datetime
from matplotlib import pyplot as plt
import math

# Convert mph to kmh
def mph_to_kmh(mph):
    return mph * 1.609344


# Convert mph to knots
def mph_to_knots(mph):
    return mph * 0.8689762


# Convert mph to meters per second
def mph_to_ms(mph):
    return mph * 0.44704


class Wind:
    speed = 0.0     # Wind speed in MPH
    gust = 0.0      # Latest wind gust in MPH
    direction = 0.0     # Wind direction in degrees
    s_temp = 0.0        # Wind sensor temperature
    v_mcu = 0.0         # Wind sensor microcontroller ambient temperature
    rssi = 0            # Wind sensor received signal strength indicator
    snr = 0.0           # Wind sensor signal to noise ratio
    m_count = 0         # Wind sensor message count
    old_m_count = 0     # Wind sensor old message count
    new_message = 0
    last_received_message_time = "00:00:00"  # Wind sensor time of last message received
    rx = 0              # Wind sensor valid received message flag
    first = 0           # Wind sensor first time received message flag

    max_speed = 0.0     # Maximum wind speed today in MPH
    max_speed_time = "00:00:00"     # Time of maximum wind speed today
    max_gust = 0.0      # Maximum wind gust today in MPH
    max_gust_time = "00:00:00"  # Time of maximum wind gust today
    max_gust_dir = 0.0      # Direction in degrees of maximum wind gust today
    wind_run = 0.0

    # Temporary holding registers until data is validated
    temp_speed = 0.0
    temp_gust = 0.0
    temp_direction = 0.0
    temp_s_temp = 0.0
    temp_v_mcu = 0.0
    temp_rssi = 0
    temp_snr = 0.0
    temp_m_count = 0

    # Alarm levels
    minimum_battery_voltage = 2.3   # VMCU voltage below this will cause battery flat alarm
    battery_warning_voltage = 2.5   # VMCU voltage below this will cause battery warning alarm
    rx_timeout_seconds = 180    # If sensor has not sent a new message for longer than this then rx_timeout_alarm will be set
    maximum_sensor_temp = 70    # Sensor temperature above this may be a problem! (battery may not work well)
    minimum_sensor_temp = -20   # Sensor temperature below this may be a problem! (battery may not work well)

    # Alarm flags
    battery_flat_voltage_alarm = 0       # Sensor VMCU (battery) flat voltage alarm
    battery_low_voltage_alarm = 0        # Sensor VMCU (battery) low voltage alarm
    rx_timeout_alarm = 0    # Receiver timeout alarm
    max_temp_alarm = 0      # Sensor over temperature alarm
    min_temp_alarm = 0      # Sensor under temperature alarm

    key = [0x78, 0xCE, 0x7F, 0x6D, 0x39, 0x75, 0xA6, 0x78]  # The key that must match for this sensor

    def __init__(self):
        # 24 hour (1440 minutes) data lists
        self.speed_data = []
        self.gust_data = []
        self.direction_data = []
        self.x_times = []
        self.s_temp_data = []
        self.v_mcu_data = []
        self.rssi_data = []
        self.snr_data = []

    # Call this method after putting received values into temporary holding registers.
    # If the reception was valid, the values will be transferred to the real parameters.
    def update(self):
        # print("Wind sensor update")
        self.check_max_min()

        # Check alarm levels
        if self.v_mcu < self.minimum_battery_voltage:
            self.battery_flat_voltage_alarm = 1     # Set alarm flag for flat battery
            print("Wind Sensor - Flat Battery alarm!", self.v_mcu)
        else:
            self.battery_flat_voltage_alarm = 0     # Clear alarm flag for flat battery
        if self.v_mcu < self.battery_warning_voltage:
            self.battery_low_voltage_alarm = 1     # Set alarm flag for low battery
            print("Wind Sensor - Low Battery alarm!", self.v_mcu)
        else:
            self.battery_low_voltage_alarm = 0     # Clear alarm flag for low battery
        if self.s_temp > self.maximum_sensor_temp:
            self.max_temp_alarm = 1     # Set max temp alarm
            print("Wind Sensor - Over temperature alarm!", self.s_temp)
        else:
            self.max_temp_alarm = 0     # Clear max temp alarm

        if self.s_temp < self.minimum_sensor_temp:
            self.min_temp_alarm = 1     # Set min temp alarm
            print("Wind Sensor - Under temperature alarm!", self.s_temp)
        else:
            self.min_temp_alarm = 0     # Clear min temp alarm

        # Check message reception
        if self.m_count != self.old_m_count:
            time_now = datetime.datetime.now()
            self.last_received_message_time = time_now     # Capture the time when a new message was received
            # We can use this last received time to determine if a sensor has stopped sending data
            self.old_m_count = self.m_count  # Remember message count
            self.rx_timeout_alarm = 0   # Turn off rx alarm as we received a message
        else:
            time_now = datetime.datetime.now()
            tdelta = time_now - self.last_received_message_time
            tdelta_secs = tdelta.total_seconds()
            if tdelta_secs > self.rx_timeout_seconds:
                self.rx_timeout_alarm = 1   # Set the alarm flag
                print("Wind Sensor RX Timeout Alarm!", tdelta_secs)
                rx = 0
            # print("New wind message was ", tdelta, " ago.")


    # Call this to check if max/mins have been exceeded, usually
    # call after new values have been set.
    def check_max_min(self):
        time_now = datetime.datetime.now()
        fmt = "%H:%M:%S"
        time1 = time_now.strftime(fmt)
        if self.first == 0:
            self.max_gust = self.gust
            self.max_speed = self.speed
            self.max_gust_dir = self.direction
            self.max_gust_time = time1
            self.max_speed_time = time1
            self.first = 1
        else:
            if self.gust > self.max_gust:
                self.max_gust = self.gust
                self.max_gust_time = time1
            if self.speed > self.max_speed:
                self.max_speed = self.speed
                self.max_speed_time = time1

    # Call this to reset max/min, usually at end of day
    def reset_max_min(self):
        now = datetime.datetime.now()
        fmt = "%H:%M:%S"
        time1 = now.strftime(fmt)
        self.max_gust = self.gust
        self.max_speed = self.speed
        self.max_gust_dir = self.direction
        self.max_gust_time = time1
        self.max_speed_time = time1
        self.wind_run = 0

    # Adds current data to all the internal lists and adds the
    # current timestamp to the x_times list
    def add_data(self):
        # Remove oldest data if more than 24 hours worth
        if len(self.speed_data) > 1440:
            self.speed_data.pop(0)
            self.gust_data.pop(0)
            self.direction_data.pop(0)
            self.s_temp_data.pop(0)
            self.v_mcu_data.pop(0)
            self.rssi_data.pop(0)
            self.snr_data.pop(0)
            self.x_times.pop(0)
        # Add new data to end of lists
        self.speed_data.append(self.speed)
        self.gust_data.append(self.gust)
        self.direction_data.append(self.direction)
        self.s_temp_data.append(self.s_temp)
        self.v_mcu_data.append(self.v_mcu)
        self.rssi_data.append(self.rssi)
        self.snr_data.append(self.snr)
        self.x_times.append(datetime.datetime.now())
        # print("Wind data stored")

    # Get current wind speed in kmh
    def get_wind_speed_kmh(self):
        return mph_to_kmh(self.speed)

    # Get current wind speed in knots
    def get_wind_speed_knots(self):
        return mph_to_knots(self.speed)

    # Get current wind speed in meters per second
    def get_wind_speed_ms(self):
        return mph_to_ms(self.speed)

    # Draws a 24-hour wind graph with points at 1 minute intervals.
    # Plots 1 minute average wind speed and wind gust
    def draw_wind_graph(self, plot_to_file=False, file_name=""):
        plt.plot(self.x_times, self.speed_data, "-b", label="Speed")
        plt.plot(self.x_times, self.gust_data, "-r", label="Gust")
        plt.legend(loc="upper left")
        plt.gcf().autofmt_xdate()
        plt.xlabel("Time")
        plt.ylabel("Speed (MPH)")
        fig = plt.gcf()
        fig.canvas.set_window_title("Wind Speed 24-hour Graph")
        if plot_to_file == True:
            plt.savefig(file_name)
            plt.clf()
            plt.close(fig)
        else:
            plt.show()

    # Draws a 24-hour wind direction graph at 1 minute intervals.
    def draw_dir_graph(self, plot_to_file=False, file_name=""):
        plt.plot(self.x_times, self.direction_data)
        plt.gcf().autofmt_xdate()
        plt.xlabel("Time")
        plt.ylabel("Wind Direction (degrees)")
        fig = plt.gcf()
        fig.canvas.set_window_title("Wind Direction 24-hour Graph")
        if plot_to_file == True:
            plt.savefig(file_name)
            plt.clf()
            plt.close(fig)
        else:
            plt.show()

    def draw_sensor_temp_graph(self, plot_to_file=False, file_name=""):
        plt.plot(self.x_times, self.s_temp_data)
        plt.gcf().autofmt_xdate()
        plt.xlabel("Time")
        plt.ylabel("Temperature (\N{DEGREE SIGN} C)")
        fig = plt.gcf()
        fig.canvas.set_window_title("Wind Sensor Temperature 24-hour Graph")
        if plot_to_file == True:
            plt.savefig(file_name)
            plt.clf()
            plt.close(fig)
        else:
            plt.show()

    def draw_v_mcu_graph(self, plot_to_file=False, file_name=""):
        plt.plot(self.x_times, self.v_mcu_data)
        plt.gcf().autofmt_xdate()
        plt.xlabel("Time")
        plt.ylabel("Voltage (V)")
        fig = plt.gcf()
        fig.canvas.set_window_title("Wind Sensor MCU Voltage 24-hour Graph")
        if plot_to_file == True:
            plt.savefig(file_name)
            plt.clf()
            plt.close(fig)
        else:
            plt.show()

    def draw_rssi_graph(self, plot_to_file=False, file_name=""):
        plt.plot(self.x_times, self.rssi_data)
        plt.gcf().autofmt_xdate()
        plt.xlabel("Time")
        plt.ylabel("RSSI (dB)")
        fig = plt.gcf()
        fig.canvas.set_window_title("Wind Sensor RSSI 24-hour Graph")
        if plot_to_file == True:
            plt.savefig(file_name)
            plt.clf()
            plt.close(fig)
        else:
            plt.show()

    def draw_snr_graph(self, plot_to_file=False, file_name=""):
        plt.plot(self.x_times, self.snr_data)
        plt.gcf().autofmt_xdate()
        plt.xlabel("Time")
        plt.ylabel("SNR (dB)")
        fig = plt.gcf()
        fig.canvas.set_window_title("Wind Sensor SNR 24-hour Graph")
        if plot_to_file == True:
            plt.savefig(file_name)
            plt.clf()
            plt.close(fig)
        else:
            plt.show()

    def convert_adc_to_temp(self, adc):
        adc_max = 1023.0
        r1 = 10000
        rt = r1 * (adc_max/adc-1)
        r_ratio = r1/rt
        beta = 3950
        t1 = 298.15
        zero_k = 273.15
        tk = t1 * beta/math.log10(r_ratio)/(beta/math.log10(r_ratio)-t1)
        return tk - zero_k

    def calculate_wind_direction_degrees(self, dir_code):
        return float(dir_code * 22.5)

    def calculate_wind_speed_kmh(self, clicks):
            average_radius = 70.0
            anemometer_transmit_interval = 65.536
            anemometer_factor = 3.0
            clicks_per_rev = 2.0
            circumference = 2 * math.pi * average_radius
            rpm = float(clicks/clicks_per_rev)/anemometer_transmit_interval * 60.0
            speed_kmh = anemometer_factor * rpm * circumference * 60.0/1000000.0
            return speed_kmh

    def calculate_wind_gust_kmh(self, clicks):
            average_radius = 70.0
            anemometer_gust_interval = 2.048
            anemometer_factor = 3.0
            clicks_per_rev = 2.0
            circumference = 2 * math.pi * average_radius
            rpm = float(clicks/clicks_per_rev)/anemometer_gust_interval * 60.0
            gust_kmh = anemometer_factor * rpm * circumference * 60.0/1000000.0
            return gust_kmh

    def kmh_to_mph(self, kmh):
        return kmh * 0.621371

    # Returns the beaufort number for a given wind speed in knots
    def get_beaufort_number(self, knots):
        bf = 0
        if knots>=1 and knots<3:
            bf = 1
        elif knots>=3 and knots<7:
            bf = 2
        elif knots>=7 and knots<11:
            bf = 3
        elif knots>=11 and knots<17:
            bf = 4
        elif knots>=17 and knots<22:
            bf = 5
        elif knots>=22 and knots<28:
            bf = 6
        elif knots>=28 and knots<34:
            bf = 7
        elif knots>=34 and knots<41:
            bf = 8
        elif knots>=41 and knots<48:
            bf = 9
        elif knots>=48 and knots<56:
            bf = 10
        elif knots>=56 and knots<64:
            bf = 11
        elif knots>=64:
            bf = 12
        return bf

    # Return the beaufort description for a given wind speed in knots
    def get_beaufort_description(self, knots):
        bfd = "Calm"
        if knots>=1 and knots<3:
            bfd = "Light air"
        elif knots>=3 and knots<7:
            bfd = "Light breeze"
        elif knots>=7 and knots<11:
            bfd = "Gentle breeze"
        elif knots>=11 and knots<17:
            bfd = "Moderate breeze"
        elif knots>=17 and knots<22:
            bfd = "Fresh breeze"
        elif knots>=22 and knots<28:
            bfd = "Strong breeze"
        elif knots>=28 and knots<34:
            bfd = "Near gale"
        elif knots>=34 and knots<41:
            bfd = "Gale"
        elif knots>=41 and knots<48:
            bfd = "Strong gale"
        elif knots>=48 and knots<56:
            bfd = "Storm"
        elif knots>=56 and knots<64:
            bfd = "Severe storm"
        elif knots>=64:
            bfd = "Hurricane"
        return bfd

    # Convert mph to knots
    def mph_to_knots(self, mph):
        return mph / 1.15078

    # Call this function with a message received for a wind sensor.
    def receive_message(self, data_list, s, r):
        # print("Wind checking message")

        # Check for key match
        match = 1
        for i in range (0,8):
            if data_list[3+i] != self.key[i]:
                match = 0
        if match > 0:
            # print("Wind key match")
            self.rx = 1
            self.snr = s
            self.rssi = r
            self.m_count = data_list[12]*16777216 + data_list[13]*65536 + data_list[14]*256 + data_list[15]
            mcu_supply_raw = data_list[16] * 256 + data_list[17]
            self.v_mcu = float(mcu_supply_raw/250.0)
            # print("VMCU: ", self.v_mcu)
            s_temp_raw = data_list[18] * 256 + data_list[19]
            self.s_temp = self.convert_adc_to_temp(s_temp_raw)
            # print("S Temp:", self.s_temp)
            gust_clicks = data_list[24] * 256 + data_list[25]
            av_clicks = data_list[26] * 256 + data_list[27]
            raw_dir = data_list[28]
            self.direction = self.calculate_wind_direction_degrees(raw_dir)
            wind_kmh = self.calculate_wind_speed_kmh(av_clicks)
            gust_kmh = self.calculate_wind_gust_kmh(gust_clicks)
            self.speed = self.kmh_to_mph(wind_kmh)
            self.gust = self.kmh_to_mph(gust_kmh)
            self.wind_run = self.wind_run + self.speed / 60 # Add on the amount of miles for this minute

    # Gets a text direction for a given angle. e.g. "N" for 0 degrees
    # Will return 16 possible points
    def get_direction_text(self, angle):
        ret_string = "N"
        if angle>11.25 and angle <= 33.75:
            ret_string = "NNE"
        elif angle>33.75 and angle <=56.25:
            ret_string = "NE"
        elif angle>56.25 and angle <=78.75:
            ret_string = "ENE"
        elif angle>78.75 and angle <=101.25:
            ret_string = "E"
        elif angle>101.25 and angle<=123.75:
            ret_string = "ESE"
        elif angle>123.75 and angle<=146.25:
            ret_string = "SE"
        elif angle>146.25 and angle<=168.75:
            ret_string = "SSE"
        elif angle>168.75 and angle<=191.25:
            ret_string = "S"
        elif angle>191.25 and angle<=213.75:
            ret_string = "SSW"
        elif angle>213.25 and angle<=236.25:
            ret_string = "SW"
        elif angle>236.25 and angle<=258.75:
            ret_string = "WSW"
        elif angle>258.75 and angle<=281.25:
            ret_string = "W"
        elif angle>281.25 and angle<=303.75:
            ret_string = "WNW"
        elif angle>303.75 and angle<=326.25:
            ret_string = "NW"
        elif angle>326.25 and angle<=348.75:
            ret_string = "NNW"

        return ret_string
