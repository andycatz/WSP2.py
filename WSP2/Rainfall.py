import datetime
from matplotlib import pyplot as plt
import math


def get_epochtime_ms():
    return round(datetime.datetime.utcnow().timestamp() * 1000)


class Rainfall:
    rain_mm = 0.0
    old_rain_mm = 0.0  # Used to calculate increases for month/year rain
    old_rain_time_ms = 0  # Used to calculate rainfall rate
    month_rain_mm = 0.0
    year_rain_mm = 0.0
    hour_rain_mm = 0.0  # Rainfall in the last 60 minutes
    rain_tips = 0
    old_rain_tips = 0
    s_temp = 0.0
    v_mcu = 0.0
    rssi = 0
    snr = 0.0
    m_count = 0
    new_message = 0
    old_m_count = 0     # Wind sensor old message count
    last_received_message_time = "00:00:00"  # Wind sensor time of last message received
    rx = 1
    rain_rate = 0.0
    max_rain_rate = 0.0
    max_rain_rate_time = "00:00:00"
    max_hour_rain = 0.0
    max_hour_rain_time = "00:00:00"
    first = 0
    mm_per_tip = 0.33  # Rain mm per tip (scaling factor)
    last_rain = "01/01/00 00:00:00"
    days_since_last_dry_day = 0
    days_since_it_last_rained = 0

    # Alarm levels
    minimum_battery_voltage = 2.3   # VMCU voltage below this will cause battery flat alarm 2.3V
    battery_warning_voltage = 2.5   # VMCU voltage below this will cause battery warning alarm 2.5V
    rx_timeout_seconds = 180    # If sensor has not sent a new message for longer than this then rx_timeout_alarm will be set
    maximum_sensor_temp = 70    # Sensor temperature above this may be a problem! (battery may not work well)
    minimum_sensor_temp = -20   # Sensor temperature below this may be a problem! (battery may not work well)

    # Alarm flags
    battery_flat_voltage_alarm = 0       # Sensor VMCU (battery) flat voltage alarm
    battery_low_voltage_alarm = 0        # Sensor VMCU (battery) low voltage alarm
    rx_timeout_alarm = 0    # Receiver timeout alarm
    max_temp_alarm = 0      # Sensor over temperature alarm
    min_temp_alarm = 0      # Sensor under temperature alarm

    key = [0xE6, 0xBA, 0x08, 0xFB, 0x3A, 0x4F, 0x5E, 0xCE]  # The key that must match for this sensor

    def __init__(self):
        # data lists
        self.rain_mm_data = []
        self.rain_tips_data = []    # Rain sensor tips data (this has counter values which are never reset)
        self.rain_rate_data = []
        self.x_times = []
        self.s_temp_data = []
        self.v_mcu_data = []
        self.rssi_data = []
        self.snr_data = []
        self.rain_mm_days = []  # Rainfall for each day of this month
        self.rain_mm_months = []  # Rainfall totals for each month of this year

    def check_max_min(self):
        now = datetime.datetime.now()
        fmt = "%H:%M:%S"
        time1 = now.strftime(fmt)
        if self.first == 0:
            self.max_rain_rate = self.rain_rate
            self.max_rain_rate_time = time1
            self.old_rain_tips = self.rain_tips
            self.first = 1
        else:
            if self.rain_rate > self.max_rain_rate:
                self.max_rain_rate = self.rain_rate
                self.max_rain_rate_time = time1
        if self.hour_rain_mm > self.max_hour_rain:
            self.max_hour_rain = self.hour_rain_mm
            self.max_hour_rain_time = time1

    def update(self):
        print("Rainfall update")
        # rain.tips contains the rain sensor TOTAL count for as long as it has been powered.  We need to work
        # out if there has been an increment and do some things with that.
        increment_tips = self.rain_tips - self.old_rain_tips          # Calculate how many new tips have occurred
        print("Rain tips", self.rain_tips)
        print("Old rain tips", self.old_rain_tips)
        self.old_rain_mm = self.rain_mm
        self.rain_mm = self.rain_mm + increment_tips * self.mm_per_tip     # Calculate today's total rain

        increment_mm = self.rain_mm - self.old_rain_mm

        if increment_mm > 0:
            # Record time/date of rainfall event as last_rain
            now = datetime.datetime.now()
            fmt = "%Y/%m/%d %H:%M:%S"
            self.last_rain = now.strftime(fmt)

        # Check alarm levels
        if self.v_mcu < self.minimum_battery_voltage:
            self.battery_flat_voltage_alarm = 1     # Set alarm flag for flat battery
            print("Rain Sensor - Flat Battery alarm!", self.v_mcu)
        else:
            self.battery_flat_voltage_alarm = 0     # Clear alarm flag for flat battery
        if self.v_mcu < self.battery_warning_voltage:
            self.battery_low_voltage_alarm = 1     # Set alarm flag for low battery
            print("Rain Sensor - Low Battery alarm!", self.v_mcu)
        else:
            self.battery_low_voltage_alarm = 0     # Clear alarm flag for low battery
        if self.s_temp > self.maximum_sensor_temp:
            self.max_temp_alarm = 1     # Set max temp alarm
            print("Rain Sensor - Over temperature alarm!", self.s_temp)
        else:
            self.max_temp_alarm = 0     # Clear max temp alarm

        if self.s_temp < self.minimum_sensor_temp:
            self.min_temp_alarm = 1     # Set min temp alarm
            print("Rain Sensor - Under temperature alarm!", self.s_temp)
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
                print("Rain Sensor RX Timeout Alarm!", tdelta_secs)
                rx = 0
            print("New rain sensor message was ", tdelta, " ago.")

        if increment_mm > 0:
            self.month_rain_mm = self.month_rain_mm + increment_mm
            self.year_rain_mm = self.year_rain_mm + increment_mm
        self.calculate_rain_rate()
        self.calculate_hour_rain()
        self.check_max_min()

    # Calculates rainfall rate
    def calculate_rain_rate(self):
        # rain has increased by inc mm since last time.
        # This doesn't mean it has stopped raining since
        # the time between tips can be quite long when
        # the rain rate is low e.g 3mm per hour is 1mm per 20 minutes
        # or 0.33mm per 6.67 minutes.  We will set the rainfall rate
        # to zero only after 30 minutes of no new tips.
        timenow_ms = get_epochtime_ms()  # Time in milliseconds
        inc_tips = self.rain_tips - self.old_rain_tips
        inc_mm = inc_tips * self.mm_per_tip
        if inc_mm > 0:
            # New rain tip(s) occurred
            timediff = timenow_ms - self.old_rain_time_ms  # Time difference between tips in ms
            self.rain_rate = inc_mm / timediff * 3600000  # Rate in mm per hour
            self.old_rain_time_ms = timenow_ms
            self.old_rain_tips = self.rain_tips

        else:
            if (timenow_ms - self.old_rain_time_ms) > 1800000:
                # Time since last tip is over 30 minutes, reset rate to zero
                # This will also work for a first tip since old_time will be zero
                # This means the minimum rain rate is 0.66mm/hr
                self.rain_rate = 0

    """Calculates the rainfall for the past hour using rain_tips[] data"""
    def calculate_hour_rain(self):
        if len(self.rain_tips_data) > 60:
            rain_tips_hour_ago = self.rain_tips_data[-60]
            tips_in_last_hour = self.rain_tips - rain_tips_hour_ago
            if tips_in_last_hour < 0:
                tips_in_last_hour = 0
            self.hour_rain_mm = tips_in_last_hour * self.mm_per_tip
        elif len(self.rain_tips_data) > 1:
            tips_in_last_hour = self.rain_tips - self.rain_tips_data[-1]
            if tips_in_last_hour < 0:
                tips_in_last_hour = 0
            self.hour_rain_mm = tips_in_last_hour * self.mm_per_tip
        else:
            self.hour_rain_mm = 0

    def reset_max_min(self):
        now = datetime.datetime.now()
        fmt = "%H:%M:%S"
        time1 = now.strftime(fmt)
        self.max_rain_rate = self.rain_rate
        self.max_rain_rate_time = time1
        if self.rain_mm > 0:
            # It rained so days since it last rained = 0
            # days since last dry day + 1
            self.days_since_it_last_rained = 0
            self.days_since_last_dry_day = self.days_since_last_dry_day + 1
        else:
            # It did not rain so days since it last rained + 1
            self.days_since_it_last_rained = self.days_since_it_last_rained + 1
            self.days_since_last_dry_day = 0

        self.rain_mm = 0
        self.max_hour_rain = 0.0
        self.max_hour_rain_time = "00:00:00"

    def reset_month(self):
        self.month_rain_mm = 0.0

    def reset_year(self):
        self.year_rain_mm = 0.0

    # Adds current data to all the internal lists and adds the
    # current timestamp to the x_times list
    def add_data(self):
        # Remove oldest data if more than 24 hours worth
        if len(self.rain_mm_data) > 1440:
            self.rain_mm_data.pop(0)
            self.rain_rate_data.pop(0)
            self.rain_tips_data.pop(0)
            self.s_temp_data.pop(0)
            self.v_mcu_data.pop(0)
            self.rssi_data.pop(0)
            self.snr_data.pop(0)
            self.x_times.pop(0)
        # Add new data to end of lists
        self.rain_mm_data.append(self.rain_mm)
        self.rain_rate_data.append(self.rain_rate)
        self.rain_tips_data.append(self.rain_tips)
        self.s_temp_data.append(self.s_temp)
        self.v_mcu_data.append(self.v_mcu)
        self.rssi_data.append(self.rssi)
        self.snr_data.append(self.snr)
        self.x_times.append(datetime.datetime.now())
        # print("Rain data stored")

    def draw_24hr_rainfall_graph(self, plot_to_file=False, file_name=""):
        plt.plot(self.x_times, self.rain_mm_data)
        plt.gcf().autofmt_xdate()
        plt.xlabel("Time")
        plt.ylabel("Rainfall (mm)")
        fig = plt.gcf()
        fig.canvas.set_window_title("Rainfall 24-hour Graph")
        if plot_to_file == True:
            plt.savefig(file_name)
            plt.clf()
            plt.close(fig)
        else:
            plt.show()

    def draw_24hr_rainrate_graph(self, plot_to_file=False, file_name=""):
        plt.plot(self.x_times, self.rain_rate_data)
        plt.gcf().autofmt_xdate()
        plt.xlabel("Time")
        plt.ylabel("Rainfall Rate (mm/hr)")
        fig = plt.gcf()
        fig.canvas.set_window_title("Rainfall Rate 24-hour Graph")
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
        fig.canvas.set_window_title("Rainfall Sensor Temperature 24-hour Graph")
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
        fig.canvas.set_window_title("Rainfall Sensor MCU Voltage 24-hour Graph")
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
        fig.canvas.set_window_title("Rainfall Sensor RSSI 24-hour Graph")
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
        fig.canvas.set_window_title("Rainfall Sensor Sensor SNR 24-hour Graph")
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

    # Call this function with a message received for a rain sensor.
    def receive_message(self, data_list, s, r):
        print("Rain checking message")

        # Check for key match
        match = 1
        for i in range (0,8):
            if data_list[3+i] != self.key[i]:
                match = 0
        if match > 0:
            print("Rain key match")
            rx = 1
            self.snr = s
            self.rssi = r
            self.m_count = data_list[12]*16777216 + data_list[13]*65536 + data_list[14]*256 + data_list[15]
            mcu_supply_raw = data_list[16] * 256 + data_list[17]
            self.v_mcu = float(mcu_supply_raw/250.0)
            # print("VMCU: ", self.v_mcu)
            s_temp_raw = data_list[18] * 256 + data_list[19]
            self.s_temp = self.convert_adc_to_temp(s_temp_raw)
            # print("S Temp:", self.s_temp)
            self.rain_tips = data_list[24] * 16777216 + data_list[25] * 65536 + data_list[26] * 256 + data_list[27]
            print("Raw tips:", self.rain_tips)
            if self.first == 0:
                self.old_rain_tips = self.rain_tips  #Sets the initial rain tips offset
                self.first = 1
