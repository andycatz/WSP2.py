from SX127x.LoRa import *
from SX127x.LoRaArgumentParser import LoRaArgumentParser
from SX127x.board_config import BOARD
from LoRaRcvCont import *

class LoRaRcvCont(LoRa):
    payload = []    # Will contain received bytes
    new_data = 0    # Set to 1 when new data is received.  Set back to 0 when data has been read.
    snr = 0
    rssi = 0

    def __init__(self, verbose=False):
        super(LoRaRcvCont, self).__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([0] * 6)

    def on_rx_done(self):
        BOARD.led_on()
        # print("\nRxDone")
        self.clear_irq_flags(RxDone=1)
        self.payload = self.read_payload(nocheck=True)
        # print(payload)
        # print([hex(x) for x in payload])
        # print(bytes(payload).decode("utf-8",'ignore'))
        self.set_mode(MODE.SLEEP)
        self.reset_ptr_rx()
        BOARD.led_off()
        self.set_mode(MODE.RXCONT)
        self.new_data = 1

    def get_data(self):
        self.new_data = 0
        return self.payload

    def on_tx_done(self):
        print("\nTxDone")
        print(self.get_irq_flags())

    def on_cad_done(self):
        print("\non_CadDone")
        print(self.get_irq_flags())

    def on_rx_timeout(self):
        print("\non_RxTimeout")
        print(self.get_irq_flags())

    def on_valid_header(self):
        print("\non_ValidHeader")
        print(self.get_irq_flags())

    def on_payload_crc_error(self):
        print("\non_PayloadCrcError")
        print(self.get_irq_flags())

    def on_fhss_change_channel(self):
        print("\non_FhssChangeChannel")
        print(self.get_irq_flags())

    def start(self):
        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT)
        """
        while True:
            sleep(.5)
            rssi_value = self.get_rssi_value()
            status = self.get_modem_status()
            # sys.stdout.flush()
            # sys.stdout.write("\r%d %d %d" % (rssi_value, status['rx_ongoing'], status['modem_clear']))
        """

    def get_rssi(self):
        return self.get_pkt_rssi_value()

    def get_snr(self):
        return self.get_pkt_snr_value()

    def get_status(self):
        return self.get_modem_status()