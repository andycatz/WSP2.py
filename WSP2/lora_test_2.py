from SX127x.LoRa import *
from SX127x.board_config import BOARD
import time

BOARD.setup()

lora = LoRa()
lora.set_mode(MODE.STDBY)
time.sleep(100)
lora.set_freq(866.5)

print (lora.get_version())
print (lora.get_freq())

BOARD.teardown()