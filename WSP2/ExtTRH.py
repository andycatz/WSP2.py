# Ext TRH Sensor

from datetime import datetime
from matplotlib import pyplot as plt
from os.path import exists
import csv
import math


# Convert Celsius to Farenheit
def get_temp_F(tc):
    return tc * 9 / 5 + 32


# Convert Farenheit to Celsius
def get_temp_C(tf):
    return (tf - 32) * 5 / 9

# Calculate the dewpoint from temperature in degrees Celsius and relative humidity (0 to 100%).
# This is only an estimate (the Magnus formula).
def calculate_dewpoint(tc, hum):
    b = 18.678
    c = 257.14
    gamma = math.log(hum/100) + b * tc/(c + tc)
    return c * gamma/(b - gamma)


class ExtTRH:
    temp_c = 0.0
    rh = 0.0
    dp = 0.0
    s_temp = 0.0
    v_mcu = 0.0
    v_supply = 0.0
    v_fan = 0.0
    rssi = 0
    snr = 0.0
    m_count = 0
    old_m_count = 0  # Sensor old message count
    rx = 1
    last_received_message_time = "00:00:00"  # Sensor time of last message received
    new_message = 0
    max_temp_c = 0.0
    min_temp_c = 0.0
    max_temp_time = "00:00:00"
    min_temp_time = "00:00:00"
    max_rh = 0.0
    min_rh = 0.0
    max_rh_time = "00:00:00"
    min_rh_time = "00:00:00"
    first = 0
    av_temp = 0.0  # Average temperature since midnight
    av_temp_sum = 0.0  # Used to keep track of sum of average temperature values
    av_temp_count = 0  # Used to keep track of how many values have been added to the average sum
    temperature_rate = 0.0  # Rate of change of temperature in °C/hr averaged over 1 hour
    max_dp = 0.0
    min_dp = 0.0
    max_dp_time = "00:00:00"
    min_dp_time = "00:00:00"
    key = [0x6C, 0x27, 0xDA, 0x88, 0x2F, 0xE4, 0x1A, 0xF0]  # The key that must match for this sensor

    # Alarm levels
    minimum_battery_voltage = 2.3   # VMCU voltage below this will cause battery flat alarm
    battery_warning_voltage = 2.5   # VMCU voltage below this will cause battery warning alarm
    rx_timeout_seconds = 120    # If sensor has not sent a new message for longer than this then rx_timeout_alarm will be set
    maximum_sensor_temp = 70    # Sensor temperature above this may be a problem! (battery may not work well)
    minimum_sensor_temp = -20   # Sensor temperature below this may be a problem! (battery may not work well)

    # Alarm flags
    battery_flat_voltage_alarm = 0       # Sensor VMCU (battery) flat voltage alarm
    battery_low_voltage_alarm = 0        # Sensor VMCU (battery) low voltage alarm
    rx_timeout_alarm = 0    # Receiver timeout alarm
    max_temp_alarm = 0      # Sensor over temperature alarm
    min_temp_alarm = 0      # Sensor under temperature alarm

    def update(self):
        # print("TRH Update")
        self.dp = calculate_dewpoint(self.temp_c, self.rh)
        self.check_max_min()
        self.temperature_rate = self.calculate_change_rate(self.temp_data)


        # Check alarm levels
        if self.v_mcu < self.minimum_battery_voltage:
            self.battery_flat_voltage_alarm = 1     # Set alarm flag for flat battery
            print("TRH Sensor - Very Low VMCU alarm!", self.v_mcu)
        else:
            self.battery_flat_voltage_alarm = 0     # Clear alarm flag for flat battery
        if self.v_mcu < self.battery_warning_voltage:
            self.battery_low_voltage_alarm = 1     # Set alarm flag for low battery
            print("TRH Sensor - Low VMCU alarm!", self.v_mcu)
        else:
            self.battery_low_voltage_alarm = 0     # Clear alarm flag for low battery
        if self.s_temp > self.maximum_sensor_temp:
            self.max_temp_alarm = 1     # Set max temp alarm
            print("TRH Sensor - Over temperature alarm!", self.s_temp)
        else:
            self.max_temp_alarm = 0     # Clear max temp alarm

        if self.s_temp < self.minimum_sensor_temp:
            self.min_temp_alarm = 1     # Set min temp alarm
            print("TRH Sensor - Under temperature alarm!", self.s_temp)
        else:
            self.min_temp_alarm = 0     # Clear min temp alarm

        # Check message reception
        if self.m_count != self.old_m_count:
            time_now = datetime.now()
            self.last_received_message_time = time_now     # Capture the time when a new message was received
            # We can use this last received time to determine if a sensor has stopped sending data
            self.old_m_count = self.m_count  # Remember message count
            self.rx_timeout_alarm = 0   # Turn off rx alarm as we received a message
        else:
            time_now = datetime.now()
            tdelta = time_now - self.last_received_message_time
            tdelta_secs = tdelta.total_seconds()
            if tdelta_secs > self.rx_timeout_seconds:
                self.rx_timeout_alarm = 1   # Set the alarm flag
                print("TRH Sensor RX Timeout Alarm!", tdelta_secs)
                rx = 0
            # print("New TRH message was ", tdelta, " ago.")


    def check_max_min(self):
        now = datetime.now()
        fmt = "%H:%M:%S"
        time1 = now.strftime(fmt)
        if self.first == 0:
            self.max_temp_c = self.temp_c
            self.min_temp_c = self.temp_c
            self.max_rh = self.rh
            self.min_rh = self.rh
            self.max_rh_time = time1
            self.min_rh_time = time1
            self.av_temp = self.temp_c
            self.av_temp_sum = self.temp_c
            self.av_temp_count = 1
            self.max_dp = self.dp
            self.min_dp = self.dp
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

            if self.dp > self.max_dp:
                self.max_dp = self.dp
                self.max_dp_time = time1

            if self.dp < self.min_dp:
                self.min_dp = self.dp
                self.min_dp_time = time1

                """
                # Test code
            self.max_rh = self.max_rh + 5
            self.min_rh = self.min_rh + 5
            if self.max_rh > 100:
                self.max_rh = 0
                self.min_rh = 0
                """
            self.av_temp_sum = self.av_temp_sum + self.temp_c
            self.av_temp_count = self.av_temp_count + 1
            self.av_temp = self.av_temp_sum / self.av_temp_count  # Calculates average temperature

    def reset_max_min(self):
        now = datetime.now()
        fmt = "%H:%M:%S"
        time1: str = now.strftime(fmt)
        self.max_temp_c = self.temp_c
        self.min_temp_c = self.temp_c
        self.max_temp_time = time1
        self.min_temp_time = time1
        self.av_temp = self.temp_c
        self.av_temp_count = 1
        self.av_temp_sum = self.temp_c
        self.max_dp = self.dp
        self.min_dp = self.dp
        self.max_dp_time = time1
        self.min_dp_time = time1

    def __init__(self):
        # 24 hour (1440 minutes) data lists
        self.temp_data = []
        self.rh_data = []
        self.x_times = []
        self.s_temp_data = []
        self.v_mcu_data = []
        self.v_supply_data = []
        self.v_fan_data = []
        self.rssi_data = []
        self.snr_data = []

    # Adds current data to all the internal lists and adds the
    # current timestamp to the x_times list
    def add_data(self):
        # Remove the oldest data if more than 24 hours worth
        if len(self.temp_data) > 1440:
            self.temp_data.pop(0)
            self.rh_data.pop(0)
            self.v_mcu_data.pop(0)
            self.v_supply_data.pop(0)
            self.v_fan_data.pop(0)
            self.rssi_data.pop(0)
            self.snr_data.pop(0)
            self.x_times.pop(0)
        # Add new data to end of lists
        self.temp_data.append(self.temp_c)
        self.rh_data.append(self.rh)
        self.s_temp_data.append(self.s_temp)
        self.v_mcu_data.append(self.v_mcu)
        self.v_supply_data.append(self.v_supply)
        self.v_fan_data.append(self.v_fan)
        self.rssi_data.append(self.rssi)
        self.snr_data.append(self.snr)
        self.x_times.append(datetime.now())
        # print("Ext TRH data stored")

    # Creates a plot of external temperature.  If plot_to_file is true
    # then it will save the plot to the supplied file_name and will
    # NOT plot to the screen.
    def draw_ext_temp_graph(self, plot_to_file=False, file_name=""):
        plt.plot(self.x_times, self.temp_data)
        plt.gcf().autofmt_xdate()
        plt.xlabel("Time")
        plt.ylabel("Temperature (\N{DEGREE SIGN} C)")
        fig = plt.gcf()
        fig.canvas.set_window_title("External Temperature 24-hour Graph")
        if plot_to_file==True:
            plt.savefig(file_name)
            plt.clf()
            plt.close(fig)
        else:
            plt.show()

    def draw_ext_rh_graph(self, plot_to_file=False, file_name=""):
        plt.plot(self.x_times, self.rh_data)
        plt.gcf().autofmt_xdate()
        plt.xlabel("Time")
        plt.ylabel("RH (%)")
        fig = plt.gcf()
        fig.canvas.set_window_title("External Relative Humidity 24-hour Graph")
        if plot_to_file==True:
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
        fig.canvas.set_window_title("External TRH Sensor Temperature 24-hour Graph")
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
        fig.canvas.set_window_title("External TRH Sensor MCU Voltage 24-hour Graph")
        if plot_to_file == True:
            plt.savefig(file_name)
            plt.clf()
            plt.close(fig)
        else:
            plt.show()

    def draw_v_supply_graph(self, plot_to_file=False, file_name=""):
        plt.plot(self.x_times, self.v_supply_data)
        plt.gcf().autofmt_xdate()
        plt.xlabel("Time")
        plt.ylabel("Voltage (V)")
        fig = plt.gcf()
        fig.canvas.set_window_title("External TRH Sensor Supply Voltage 24-hour Graph")
        if plot_to_file == True:
            plt.savefig(file_name)
            plt.clf()
            plt.close(fig)
        else:
            plt.show()

    def draw_v_fan_graph(self, plot_to_file=False, file_name=""):
        plt.plot(self.x_times, self.v_fan_data)
        plt.gcf().autofmt_xdate()
        plt.xlabel("Time")
        plt.ylabel("Voltage (V)")
        fig = plt.gcf()
        fig.canvas.set_window_title("External TRH Sensor Fan Voltage 24-hour Graph")
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
        fig.canvas.set_window_title("External TRH Sensor RSSI 24-hour Graph")
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
        fig.canvas.set_window_title("External TRH Sensor SNR 24-hour Graph")
        if plot_to_file == True:
            plt.savefig(file_name)
            plt.clf()
            plt.close(fig)
        else:
            plt.show()

    # The rate we require is temperature rate of change in °C per hour but over a 1-hour period.
    # td holds historical temperature data for up to the last 24 hours which must be one entry per minute.
    # When the program starts however, it will be empty and will slowly build up data.
    # Newest data is at the highest index, oldest data is at index 0
    def calculate_change_rate(self, td):
        # First determine whether there is any data and whether there is 1 hour or more of data
        return_value = 0  # The temperature rate value to be returned
        length = len(td)  # Length of temperature data - this will be in minutes
        if length > 0:
            # Some data available

            if len(td) > 60:
                # More than 1 hour of data available
                newest = td[-1]  # The newest value entered into the list
                one_hour_ago = td[-61]  # The value 1 hour ago
                return_value = newest - one_hour_ago
            else:
                oldest = td[0]  # The oldest recorded value
                newest = td[-1]  # The newest recorded value
                return_value = newest - oldest  # Temperature change
        # print("Temp rate of change ", return_value)
        return return_value  # Returns the temperature rate of change

    # Get current temperature in degrees Farenheit
    def get_temp_f(self):
        return (get_temp_F(self.temp_c))
    """
    # Restores data from data files on start up of program
    # Not working yet, numerous bugs!!!
    def restore_data(self):
        print("Ext TRH restoring data...")
        # If the date is 2nd or later, no need to look at last month's file
        time_now = datetime.now()   # Current time/date
        month_now = time_now.month
        date_now = time_now.date
        if date_now == 1:
            # Restoring data from previous month file
            print("Opening previous months data file ")
            # Work out the file name for the previous month's file.  This may be from last year also!
            old_year = time_now.year
            old_month = month_now - 1
            if month_now == 1:
                old_year = old_year - 1
                old_month = 12
            filename = "TRH"
            if old_month < 10:
                filename = filename + "0"
            filename = filename + str(old_month) + str(old_year) + ".txt"
            file_exists = exists(filename)
            if file_exists:
                # File exists, so load data from it
                with open(filename, newline='') as csvfile:
                    csvreader = csv.reader(csvfile, delimiter=",",quotechar='|')
                    for row in csvreader:
                        print(", ".join(row))
            else:
                print(filename, " does not exist.")

        print("Opening this month's data file for reading")
        filename = "TRH"
        if month_now < 10:
            filename = filename + "0"
        filename = filename + str(month_now) + str(time_now.year) + ".txt"
        file_exists = exists(filename)
        if file_exists:
            # File exists, so load data from it
            with open(filename, mode='r') as csvfile:
                csvreader = csv.DictReader(csvfile)
                line_count = 0
                for row in csvreader:
                    if line_count == 0:
                        print(f'Column names are {", ".join(row)}')
                        line_count += 1
                    print(f'\t{row["Date"]} {row["Time"]} {row["ExtTemp"]} {row["ExtRH"]} {row["ExtDP"]} {row["STemp"]} {row["VMCU"]} {row["VS"]} {row["VF"]} {row["RSSI"]} {row["SNR"]} {row["MC"]}')
                    line_count += 1
                    # We only want data from the last 24 hours
                    # Is the data from yesterday or today?
                    # If yesterday, is the time >= the same time right now?
                    # If today, any time is acceptable data
                    # Otherwise we don't need the data
                    # We also know only data from the current month is in this file so if the date is 1 don't look at yesterday

                    # Get date from first row entry
                    date_string = row["Date"]     # This should be of the format dd-mm-yyyy
                    print("Date string ", date_string[0:2])
                    day_string = date_string[0:2]   # This should just contain the date
                    day_value = int(day_string)     # This should be the date as a number
                    process_data = 0    # Flag to indicate if we are going to process this line of data (1) or not (0)
                    if date_now == day_value:
                        # All data from today's date should be processed
                        process_data = 1
                    else:
                        print("Data not from today.")
                    if date_now > 1 and day_value == date_now - 1:
                        # Data is from yesterday
                        # Now we need to know if the data is from a time after this time yesterday
                        time_string = {row["Time"]}     # This should be of the format hh:MM:ss
                        hour_string = time_string[0:2]  # This should just contain the hour
                        minute_string = time_string[3:5]    # This should just contain the minute
                        hour_value = int(hour_string)       # Convert to integer
                        minute_value = int(minute_string)   # Convert to integer
                        if hour_value > time_now.hour:
                            process_data = 1
                        if hour_value == time_now.hour and minute_value > time_now.minute:
                            process_data = 1
                    if process_data > 0:
                        # We are going to process this data into our data structures
                        extTempValue = float({row["ExtTemp"]})
                        extRHValue = float({row["ExtRH"]})
                        extDPValue = float({row["ExtDP"]})
                        sTempValue = float({row["STemp"]})
                        vMCUValue = float({row["VMCU"]})
                        vsValue = float({row["VS"]})
                        vfValue = float({row["VF"]})
                        rssiValue = float({row["RSSI"]})
                        snrValue = float({row["SNR"]})
                        self.temp_c = extTempValue
                        self.rh = extRHValue
                        self.dp = extDPValue
                        self.s_temp = sTempValue
                        self.v_mcu = vMCUValue
                        self.v_supply = vsValue
                        self.v_fan = vfValue
                        self.rssi = rssiValue
                        self.snr = snrValue
                        self.add_data()
                        self.check_max_min()
        else:
            print(filename, " does not exist.")
    """
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

    # Call this function with a message received for an ExtTRH sensor.
    def receive_message(self, data_list, s, r):
        # print("Ext TRH checking message")

        # Constants for calculating temperature
        RCALC = 0.1220703
        CONSTANT1 = 3.9083
        CONSTANT2 = 15.2725
        CONSTANT3 = 0.00231
        RTC0R = 1000.0
        CONSTANT4 = 0.001155
        RALPHA = 0.00385
        temp_offset = 1.2

        # Constants for calculating RH
        RHV_CONSTANT = 0.912611
        RHM1 = 48.23
        RHC1 = -23.82
        RHC2 = 1.0546
        RHM2 = 0.00216
        DIV_RATIO = 1.28455
        RH_SUPPLY_VOLTAGE = 3.32
        RH_CONSTANT1 = 0.1515
        RH_CONSTANT2 = 157.2327
        # Check for key match
        match = 1
        for i in range (0,8):
            if data_list[3+i] != self.key[i]:
                match = 0
        if match > 0:
            # print("Ext TRH key match")
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
            vs_raw = data_list[20] * 256 + data_list[21]
            self.v_supply = float(vs_raw/40.0)
            # print("V supply: ", self.v_supply)
            vf_raw = data_list[22] * 256 + data_list[23]
            self.v_fan = float(vf_raw/40.0)
            # print("V fan: ", self.v_fan)
            temp_raw = data_list[24] * 256 + data_list[25]
            rh_raw = data_list[26] * 256 + data_list[27]
            resistance = temp_raw * RCALC
            self.temp_c = ((-CONSTANT1 + math.sqrt(CONSTANT2 + CONSTANT3 * (RTC0R - resistance)))/-CONSTANT4) + temp_offset
            # print("Temp: ", self.temp_c)
            v_atod = rh_raw * 2.048/32768.0
            v_sensor = v_atod * DIV_RATIO
            rh_uncomp = (v_sensor/RH_SUPPLY_VOLTAGE - RH_CONSTANT1) * RH_CONSTANT2
            self.rh = rh_uncomp/(RHC2 - RHM2 * self.temp_c)
            if self.rh > 100:
                self.rh = 100
            if self.rh < 0:
                self.rh = 0
            # print("RH: ", self.rh)