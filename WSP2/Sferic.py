import datetime
from matplotlib import pyplot as plt
import math


def get_epochtime_ms():
    return round(datetime.datetime.utcnow().timestamp() * 1000)

class Sferic:

    count1 = 0.0
    count2 = 0.0
    s_temp = 0.0
    v_mcu = 0.0
    rssi = 0
    snr = 0.0
    m_count = 0
    new_message = 0
    rx = 0
    today_count1=0 #Count for today only
    today_count2=0 #Count for today only
    today_start_count1=0 #Count at start of today
    today_start_count2=0 #Count at start of today
    first=0
    rate1 = 0   # Rate of strikes per hour for counter 1
    rate2 = 0   # Rate of strikes per hour for counter 2
    old_count1 = 0
    old_count2 = 0
    old_sf_time1_ms = 0
    old_sf_time2_ms = 0

    key = [0xCD, 0xEA, 0xCB, 0x09, 0x33, 0x6B, 0x39, 0x5A]  # The key that must match for this sensor

    def update(self):
        # print("Sferic update")
        if(self.first==0):
            self.today_start_count1=self.count1
            self.today_start_count2=self.count2
            self.first=1
        else:
            self.today_count1=self.count1-self.today_start_count1
            self.today_count2=self.count2-self.today_start_count2
        self.calculate_sferic_rates()


    def reset_today_counts(self):
        self.today_start_count1=self.count1
        self.today_start_count2=self.count2
        self.today_count1=0
        self.today_count2=0



    def __init__(self):
        #24 hour (1440 minutes) data lists
        self.today_count1_data = []
        self.today_count2_data = []
        self.x_times = []
        self.s_temp_data = []
        self.v_mcu_data = []
        self.rssi_data = []
        self.snr_data = []


    #Adds current data to all the internal lists and adds the
    #current timestamp to the x_times list
    def add_data(self):
        #Remove oldest data if more than 24 hours worth
        if(len(self.today_count1_data)>1440):
            self.today_count1_data.pop(0)
            self.today_count2_data.pop(0)
            self.v_mcu_data.pop(0)
            self.rssi_data.pop(0)
            self.snr_data.pop(0)
            self.x_times.pop(0)
        #Add new data to end of lists
        self.today_count1_data.append(self.today_count1)
        self.today_count2_data.append(self.today_count2)
        self.s_temp_data.append(self.s_temp)
        self.v_mcu_data.append(self.v_mcu)
        self.rssi_data.append(self.rssi)
        self.snr_data.append(self.snr)
        self.x_times.append(datetime.datetime.now())
        #print("Sferic data stored")

    #Draw 24-hr sferic graph
    def draw_sf_graph(self):
        plt.plot(self.x_times,self.today_count1_data, "-b", label="Count1")
        plt.plot(self.x_times,self.today_count2_data, "-r", label="Count2")
        plt.legend(loc="upper left")
        plt.gcf().autofmt_xdate()
        plt.xlabel("Time")
        plt.ylabel("Sferic Count")
        fig = plt.gcf()
        fig.canvas.set_window_title("Sferic 24-hour Graph")
        plt.show()

    def draw_sensor_temp_graph(self):
        plt.plot(self.x_times,self.s_temp_data)
        plt.gcf().autofmt_xdate()
        plt.xlabel("Time")
        plt.ylabel("Temperature (\N{DEGREE SIGN} C)")
        fig = plt.gcf()
        fig.canvas.set_window_title("Sferic Sensor Temperature 24-hour Graph")
        plt.show()

    def draw_v_mcu_graph(self):
        plt.plot(self.x_times,self.v_mcu_data)
        plt.gcf().autofmt_xdate()
        plt.xlabel("Time")
        plt.ylabel("Voltage (V)")
        fig = plt.gcf()
        fig.canvas.set_window_title("Sferic Sensor MCU Voltage 24-hour Graph")
        plt.show()

    def draw_rssi_graph(self):
        plt.plot(self.x_times,self.rssi_data)
        plt.gcf().autofmt_xdate()
        plt.xlabel("Time")
        plt.ylabel("RSSI (dB)")
        fig = plt.gcf()
        fig.canvas.set_window_title("Sferic Sensor RSSI 24-hour Graph")
        plt.show()

    def draw_snr_graph(self):
        plt.plot(self.x_times,self.snr_data)
        plt.gcf().autofmt_xdate()
        plt.xlabel("Time")
        plt.ylabel("SNR (dB)")
        fig = plt.gcf()
        fig.canvas.set_window_title("Sferic Sensor SNR 24-hour Graph")
        plt.show()

    # Returns the average sferic count
    def get_average_count(self):
        return (self.today_count1 + self.today_count2)/2

    # Returns the average sferic rate
    def get_average_rate(self):
        return (self.rate1 + self.rate2)/2

    # Calculates sferic rates
    def calculate_sferic_rates(self):
        # sferic count has increased by inc since last time.
        # This doesn't mean it has stopped lightning since
        # the time between sferics can be quite long when
        # the sferic rate is low e.g 1 str per hour.  We will set the sferic rate
        # to zero only after 60 minutes of no new sferics.
        timenow_ms = get_epochtime_ms()  # Time in milliseconds
        inc1 = self.count1 - self.old_count1
        inc2 = self.count2 - self.old_count2

        if inc1 > 0:
            # New sferic(s) occurred on counter 1
            timediff = timenow_ms - self.old_sf_time1_ms  # Time difference between sferic occurrences in ms
            self.rate1 = inc1 / timediff * 3600000  # Rate in sferics per hour
            self.old_sf_time1_ms = timenow_ms
            self.old_count1 = self.count1

        else:
            if (self.old_sf_time1_ms - timenow_ms) > 3600000:
                # Time since last sferic is over 60 minutes, reset rate to zero
                # This will also work for a first sferic since old_time will be zero
                # This means the minimum sferic rate is 1/hr
                self.rate1 = 0

        if inc2 > 0:
            # New sferic(s) occurred on counter 2
            timediff = timenow_ms - self.old_sf_time2_ms  # Time difference between sferic occurrences in ms
            self.rate2 = inc2 / timediff * 3600000  # Rate in sferics per hour
            self.old_sf_time2_ms = timenow_ms
            self.old_count2 = self.count2

        else:
            if (self.old_sf_time2_ms - timenow_ms) > 3600000:
                # Time since last sferic is over 60 minutes, reset rate to zero
                # This will also work for a first sferic since old_time will be zero
                # This means the minimum sferic rate is 1/hr
                self.rate2 = 0

        if self.rate1<1:
            self.rate1 = 0

        if self.rate2<1:
            self.rate2 = 0

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

    # Call this function with a message received for a sferic sensor.
    def receive_message(self, data_list, s, r):
        # print("Sferic checking message")

        # Check for key match
        match = 1
        for i in range (0,8):
            if data_list[3+i] != self.key[i]:
                match = 0
        if match > 0:
            # print("SF key match")
            self.snr = s
            self.rssi = r
            rx = 1
            self.m_count = data_list[12]*16777216 + data_list[13]*65536 + data_list[14]*256 + data_list[15]
            mcu_supply_raw = data_list[16] * 256 + data_list[17]
            self.v_mcu = float(mcu_supply_raw/250.0)
            # print("VMCU: ", self.v_mcu)
            s_temp_raw = data_list[18] * 256 + data_list[19]
            self.s_temp = self.convert_adc_to_temp(s_temp_raw)
            # print("S Temp:", self.s_temp)
            self.count1 = data_list[24] * 16777216 + data_list[25] * 65536 + data_list[26] * 256 + data_list[27]
            self.count2 = data_list[28] * 16777216 + data_list[29] * 65536 + data_list[30] * 256 + data_list[31]
            # print("Count 1:", self.count1)
            # print("Count 2:", self.count2)
            if self.first == 0:
                self.reset_today_counts()
                self.first = 1