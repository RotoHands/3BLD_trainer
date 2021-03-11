import time
import asyncio
from bleak import BleakClient
from .decode_gan import aes128
from .decode_gan import get_moves
from .decode_gan import decData
class Trainer:
    def __init__(self):
        self.moves = []
        self.counter = 0
        self.new_moves = []

def new_moves(data, counter):
    moves = get_moves(data)
    new_counter = data[12]
    
    for i in range (new_counter-counter):
        trainer.new_moves.append(moves[5-i])







async def connect():
    UUID_SUFFIX = '-0000-1000-8000-00805f9b34fb'
    CHRCT_UUID_F3 = '0000fff3' + UUID_SUFFIX  # // prev moves
    CHRCT_UUID_F5 = '0000fff5' + UUID_SUFFIX  # // gyro state, move counter, premoves
    CHRCT_UUID_F7 = '0000fff7' + UUID_SUFFIX

    addr = "F8:30:02:08:FB:FE"
    server = BleakClient(addr)
    await server.connect()
    key = [59, 18, 93, 222, 120, 218, 120, 216, 7, 96, 163, 218, 130, 60, 1, 241]
    decoder = aes128(key)
    batt = await server.read_gatt_char(CHRCT_UUID_F7)

    while (True):
        start = time.time()
        ff5 = decode(await server.read_gatt_char(CHRCT_UUID_F5), decoder)

        #f6val = await server.read_gatt_char(CHRCT_UUID_F6)
        #f2 = await server.read_gatt_char(CHRCT_UUID_F2)

loop = asyncio.get_event_loop()
loop.run_until_complete(connect())


