import datetime
from matplotlib import pyplot as plt
import math


class UV_Light:
    visible = 0.0
    uva = 0.0
    uvb = 0.0
    uvi = 0.0
    uv_index = 0.0
    s_temp = 0.0
    v_mcu = 0.0
    rssi = 0
    snr = 0.0
    m_count = 0
    new_message = 0
    rx = 0
    max_visible = 0.0
    max_visible_time = "00:00:00"
    min_visible = 0.0
    min_visible_time = "00:00:00"
    max_uv_index = 0
    max_uv_index_time = "00:00:00"
    max_uva = 0.0
    max_uva_time = "00:00:00"
    max_uvb = 0.0
    max_uvb_time = "00:00:00"
    max_uvi = 0.0
    max_uvi_time = "00:00:00"
    first = 0

    # Temporary holding registers until data is validated
    temp_visible = 0.0
    temp_uva = 0.0
    temp_uvb = 0.0
    temp_uvi = 0.0
    temp_uv_index = 0.0
    temp_s_temp = 0.0
    temp_v_mcu = 0.0
    temp_rssi = 0
    temp_snr = 0.0
    temp_m_count = 0

    key = [0x6E, 0xDA, 0x82, 0x33, 0x33, 0x66, 0xF5, 0xE6]  # The key that must match for this sensor

    def __init__(self):
        # 24 hour (1440 minutes) data lists
        self.visible_data = []
        self.uva_data = []
        self.uvb_data = []
        self.uvi_data = []
        self.uv_index_data = []
        self.x_times = []
        self.s_temp_data = []
        self.v_mcu_data = []
        self.rssi_data = []
        self.snr_data = []

    def update(self):
        # print("UVL Sensor update")
        pass

    # Adds current data to all the internal lists and adds the
    # current timestamp to the x_times list
    def add_data(self):
        # Remove oldest data if more than 24 hours worth
        if len(self.visible_data) > 1440:
            self.visible_data.pop(0)
            self.uva_data.pop(0)
            self.uvb_data.pop(0)
            self.uvi_data.pop(0)
            self.s_temp_data.pop(0)
            self.uv_index_data.pop(0)
            self.v_mcu_data.pop(0)
            self.rssi_data.pop(0)
            self.snr_data.pop(0)
            self.x_times.pop(0)
        # Add new data to end of lists
        self.visible_data.append(self.visible)
        self.uva_data.append(self.uva)
        self.uvb_data.append(self.uvb)
        self.uvi_data.append(self.uvi)
        self.uv_index_data.append(self.uv_index)
        self.s_temp_data.append(self.s_temp)
        self.v_mcu_data.append(self.v_mcu)
        self.rssi_data.append(self.rssi)
        self.snr_data.append(self.snr)
        self.x_times.append(datetime.datetime.now())
        # print("Light data stored")

    def check_max_min(self):
        now = datetime.datetime.now()
        fmt = "%H:%M:%S"
        time1 = now.strftime(fmt)
        if self.first == 0:
            self.max_visible = self.visible
            self.min_visible = self.visible
            self.max_visible_time = time1
            self.min_visible_time = time1
            self.max_uv_index = self.uv_index
            self.max_uv_index_time = time1
            self.max_uva = self.uva
            self.max_uvb = self.uvb
            self.max_uvi = self.uvi
            self.max_uva_time = time1
            self.max_uvb_time = time1
            self.max_uvi_time = time1

            self.first = 1
        else:
            if self.visible > self.max_visible:
                self.max_visible = self.visible
                self.max_visible_time = time1
            if self.visible < self.min_visible:
                self.min_visible = self.visible
                self.min_visible_time = time1

            if self.uv_index > self.max_uv_index:
                self.max_uv_index = self.uv_index
                self.max_uv_index_time = time1

            if self.uva > self.max_uva:
                self.max_uva = self.uva
                self.max_uva_time = time1

            if self.uvb > self.max_uvb:
                self.max_uvb = self.uvb
                self.max_uvb_time = time1

            if self.uvi > self.max_uvi:
                self.max_uvi = self.uvi
                self.max_uvi_time = time1


    def draw_vis_graph(self, plot_to_file=False, file_name=""):
        plt.plot(self.x_times, self.visible_data)
        plt.gcf().autofmt_xdate()
        plt.xlabel("Time")
        plt.ylabel("Light Intensity (lux)")
        fig = plt.gcf()
        fig.canvas.set_window_title("UVL Sensor Visible Light 24-hour Graph")
        if plot_to_file == True:
            plt.savefig(file_name)
            plt.clf()
            plt.close(fig)
        else:
            plt.show()

    def draw_uv_graph(self, plot_to_file=False, file_name=""):
        plt.plot(self.x_times, self.uvi_data, "-b", label="UVI")
        plt.plot(self.x_times, self.uva_data, "-r", label="UVA")
        plt.plot(self.x_times, self.uvb_data, "-g", label="UVB")
        plt.legend(loc="upper left")
        plt.gcf().autofmt_xdate()
        plt.xlabel("Time")
        plt.ylabel("UV (W/m2)")
        fig = plt.gcf()
        fig.canvas.set_window_title("UVL Sensor Ultraviolet Light Intensity 24-hour Graph")
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
        fig.canvas.set_window_title("External UVL Sensor Temperature 24-hour Graph")
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
        fig.canvas.set_window_title("External UVL Sensor MCU Voltage 24-hour Graph")
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
        fig.canvas.set_window_title("External UVL Sensor RSSI 24-hour Graph")
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
        fig.canvas.set_window_title("External UVL Sensor SNR 24-hour Graph")
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

    def calculate_uva(self, uvar, c1_raw, c2_raw):
        uv_alpha = 1.0
        uv_delta = 1.0
        uv_gamma = 1.0
        uvAco = 1.986
        uvBco = 0.514
        uva_resp = 0.023765
        uva_calc = float(uvar) - (uvAco * uv_alpha * float(c1_raw)/uv_gamma - (uvBco * uv_alpha * float(c2_raw))/uv_delta)
        uva_result = uva_calc * (1.0/uv_alpha) * uva_resp
        return uva_result

    def calculate_uvb(self, uvbr, c1_raw, c2_raw):
        uvCco = 2.91
        uv_beta = 1.0
        uv_gamma = 1.0
        uv_delta = 1.0
        uvDco = 0.681
        uvb_resp = 0.02804
        uvb_calc = float(uvbr) - (uvCco * uv_beta * float(c1_raw)/uv_gamma - (uvDco * uv_beta * float(c2_raw))/uv_delta)
        uvb_result = uvb_calc * (1.0/uv_beta) * uvb_resp
        return uvb_result

    # Call this function with a message received for an UVL sensor.
    def receive_message(self, data_list, s, r):
        # print("UVL checking message")

        # Check for key match
        match = 1
        for i in range (0,8):
            if data_list[3+i] != self.key[i]:
                match = 0
        if match > 0:
            # print("UVL key match")
            self.snr = s
            self.rssi = r
            self.m_count = data_list[12]*16777216 + data_list[13]*65536 + data_list[14]*256 + data_list[15]
            mcu_supply_raw = data_list[16] * 256 + data_list[17]
            self.v_mcu = float(mcu_supply_raw/250.0)
            # print("VMCU: ", self.v_mcu)
            s_temp_raw = data_list[18] * 256 + data_list[19]
            self.s_temp = self.convert_adc_to_temp(s_temp_raw)
            # print("S Temp:", self.s_temp)
            uva_raw = data_list[24] * 256 + data_list[25]
            uvb_raw = data_list[26] * 256 + data_list[27]
            comp1_raw = data_list[28] * 256 + data_list[29]
            comp2_raw = data_list[30] * 256 + data_list[31]
            vis_raw = data_list[32] * 256 + data_list[33]
            self.uva = self.calculate_uva(uva_raw, comp1_raw, comp2_raw)
            self.uvb = self.calculate_uvb(uvb_raw, comp1_raw, comp2_raw)
            vis_light_scale = 1.468
            self.uvi = (self.uva + self.uvb)/2.0
            self.uv_index = self.uvi/25.0
            self.visible = vis_raw * vis_light_scale