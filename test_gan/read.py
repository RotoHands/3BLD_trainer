import asyncio
from bleak import BleakClient
import binascii
addr = "F8:30:02:08:FB:FE"
MODEL_NBR_UUID = "00002a28-0000-1000-8000-00805f9b34fb"

async def run(address):
    client = BleakClient(address)
    try:

        print ("here 1")
        await client.connect()
        print("here 2")
        for i in range (1):

            model_number =  await client.read_gatt_char(MODEL_NBR_UUID)
            print("here 3")
            print((model_number))
    except Exception as e:
        print(e)
    finally:
        print("here 4")
        await client.disconnect()


loop = asyncio.get_event_loop()
loop.run_until_complete(run(addr))
