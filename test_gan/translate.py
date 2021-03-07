import time
import asyncio
from bleak import BleakClient
import struct
import math
import numpy
import os
import sys
import collections


class aes128:
    def __init__(self, key):
        self.sbox = [99, 124, 119, 123, 242, 107, 111, 197, 48, 1, 103, 43, 254, 215, 171, 118, 202, 130, 201, 125, 250,
                     89, 71,
                     240, 173, 212, 162, 175, 156, 164, 114, 192, 183, 253, 147, 38, 54, 63, 247, 204, 52, 165, 229,
                     241, 113,
                     216, 49, 21, 4, 199, 35, 195, 24, 150, 5, 154, 7, 18, 128, 226, 235, 39, 178, 117, 9, 131, 44, 26,
                     27, 110,
                     90, 160, 82, 59, 214, 179, 41, 227, 47, 132, 83, 209, 0, 237, 32, 252, 177, 91, 106, 203, 190, 57,
                     74, 76,
                     88, 207, 208, 239, 170, 251, 67, 77, 51, 133, 69, 249, 2, 127, 80, 60, 159, 168, 81, 163, 64, 143,
                     146, 157,
                     56, 245, 188, 182, 218, 33, 16, 255, 243, 210, 205, 12, 19, 236, 95, 151, 68, 23, 196, 167, 126,
                     61, 100,
                     93, 25, 115, 96, 129, 79, 220, 34, 42, 144, 136, 70, 238, 184, 20, 222, 94, 11, 219, 224, 50, 58,
                     10, 73, 6,
                     36, 92, 194, 211, 172, 98, 145, 149, 228, 121, 231, 200, 55, 109, 141, 213, 78, 169, 108, 86, 244,
                     234, 101,
                     122, 174, 8, 186, 120, 37, 46, 28, 166, 180, 198, 232, 221, 116, 31, 75, 189, 139, 138, 112, 62,
                     181, 102,
                     72, 3, 246, 14, 97, 53, 87, 185, 134, 193, 29, 158, 225, 248, 152, 17, 105, 217, 142, 148, 155, 30,
                     135,
                     233, 206, 85, 40, 223, 140, 161, 137, 13, 191, 230, 66, 104, 65, 153, 45, 15, 176, 84, 187, 22]

        self.sboxI = [0] * 256
        self.shiftTabI = [0, 13, 10, 7, 4, 1, 14, 11, 8, 5, 2, 15, 12, 9, 6, 3]
        self.xtime = [0] * 256
        self.xtime_init = False
        self.init()
        self.initial_bool = False
        self.initial = None
        exKey = [0] * 176
        for i in range(len(key)):
            exKey[i] = key[i]
        Rcon = 1
        self.tmp = [0] * 200

        for i in range(16, 176, 4):
            try:
                self.tmp = exKey[i - 4: i]
                if (i % 16 == 0):
                    self.tmp = [self.sbox[self.tmp[1]] ^ Rcon, self.sbox[self.tmp[2]], self.sbox[self.tmp[3]],
                                self.sbox[self.tmp[0]]]
                    Rcon = self.xtime[Rcon]
                for j in range(4):
                    exKey[i + j] = exKey[i + j - 16] ^ self.tmp[j]
            except Exception as e:
                pass
        self.key = exKey

    def decrypt(self, block):
        rkey = self.key[160: 176]
        for i in range(16):
            block[i] ^= rkey[i]
        for i in range(144, 15, -16):
            block = self.shiftSubAdd(block, self.key[i: i + 16])
            for j in range(0, 16, 4):
                s0 = block[j + 0]
                s1 = block[j + 1]
                s2 = block[j + 2]
                s3 = block[j + 3]
                h = s0 ^ s1 ^ s2 ^ s3
                xh = self.xtime[h]
                h1 = self.xtime[self.xtime[xh ^ s0 ^ s2]] ^ h
                h2 = self.xtime[self.xtime[xh ^ s1 ^ s3]] ^ h
                block[j + 0] ^= h1 ^ self.xtime[s0 ^ s1]
                block[j + 1] ^= h2 ^ self.xtime[s1 ^ s2]
                block[j + 2] ^= h1 ^ self.xtime[s2 ^ s3]
                block[j + 3] ^= h2 ^ self.xtime[s3 ^ s0]
        block = self.shiftSubAdd(block, self.key[0:16])
        return block

    def shiftSubAdd(self, state, rkey):
        state0 = state[:]

        for i in range(16):
            state[i] = self.sboxI[state0[self.shiftTabI[i]]] ^ rkey[i]
        return state

    def init(self):
        if (self.xtime_init == True):
            return
        for i in range(256):
            self.sboxI[self.sbox[i]] = i
        for i in range(128):
            self.xtime[i] = i << 1
            self.xtime[128 + i] = (i << 1) ^ 0x1b
        self.xtime_init = True


decoder = None


def decode(value, decoder):
    if (decoder == None):
        return value
    decoded = [0] * len(value)
    for i in range(len(value)):
        decoded[i] = value[i]

    if (len(decoded) > 16):
        decoded = decoded[0:len(decoded) - 16] + decoder.decrypt(decoded[len(decoded) - 16:])
    decoded = decoder.decrypt(decoded)
    return decoded


def toEuler(w, x, y, z):
    sp = 2 * (w * y - z * x)
    eu = {
        "x": math.atan2(2 * (w * x + y * z), 1 - 2 * (x * x + y * y)),
        "y": math.asin(sp) if abs(sp) < 1 else numpy.sign(sp) * math.pi / 2,
        "z": math.atan2(2 * (w * z + x * y), 1 - 2 * (y * y + z * z))}

    return eu


def faceRotation(r):
    if (r < -3 * math.pi / 4):
        return 0
    if (r < -math.pi / 4):
        return 1
    if (r > 3 * math.pi / 4):
        return 0
    if (r > math.pi / 4):
        return 3
    return 2


def get_battery(value, decoder):
    value = decoder.decrypt(value)
    return value[7]


def timesOff(f6val, decoder):
    f6val = decoder.decrypt(f6val)
    timeOffs = collections.deque()
    for i in range(9):
        off = f6val[i * 2 + 1] | f6val[i * 2 + 2] << 8
        timeOffs.appendleft((math.floor(off / 0.95)))
    return timeOffs


def pollCharacteristic(value, decoder):
    try:

        value = decode(value, decoder)
        # pose
        # value = [68, -1, 124, 1, 2, 56, 4, 4, 4, 251, 252, 4, 54, 3, 3, 3, 3, 3, 3]

        for i in range(6):
            if (value[i] > 127):
                value[i] = value[i] - 256
        # print (value[:6])

        xr = value[1] << 8 | value[0]
        yr = value[3] << 8 | value[2]
        zr = value[5] << 8 | value[4]
        htm = ""
        htm += "<b>Raw:</b><br />x: " + str(round(xr)) + "<br />y: " + str(round(yr)) + "<br />z: " + str(
            round(zr)) + "<br />"

        # convert angles
        x = xr / 16384  # //* Math.PI;
        y = yr / 16384  # // * Math.PI;
        z = zr / 16384  # //* Math.PI;
        ww = 1 - (x * x + y * y + z * z)
        w = math.sqrt(ww) if ww > 0 else 0

        htm += "<b>Quaternion:</b><br />x: " + str(x) + "<br />y: " + str(y) + "<br />z: " + str(z) + "<br />w: " + str(
            w) + "<br />"
        current = {"w": w, "x": x, "y": y, "z": z}
        if (decoder.initial_bool == False):
            n = current["w"] * current["w"] + current["x"] * current["x"] + current["y"] * current["y"] + current["z"] * \
                current["z"]
            if (n == 0):
                initial = {"w": 1, "x": 0, "y": 0, "z": 0}
            else:
                n = 1 / n
                decoder.initial = {"w": current["w"] * n, "x": -current["x"] * n, "y": -current["y"] * n,
                                   "z": -current["z"] * n}
            decoder.initial_bool = True

        diff = {"w": decoder.initial["w"] * current["w"] - decoder.initial["x"] * current["x"] - decoder.initial["y"] *
                     current["y"] - decoder.initial["z"] * current["z"],
                "x": decoder.initial["w"] * current["x"] + decoder.initial["x"] * current["w"] + decoder.initial["y"] *
                     current["z"] - decoder.initial["z"] * current["y"],
                "y": decoder.initial["w"] * current["y"] + decoder.initial["y"] * current["w"] + decoder.initial["z"] *
                     current["x"] - decoder.initial["x"] * current["z"],
                "z": decoder.initial["w"] * current["z"] + decoder.initial["z"] * current["w"] + decoder.initial["x"] *
                     current["y"] - decoder.initial["y"] * current["x"]}
        d = toEuler(diff["w"], diff["x"], diff["y"], diff["z"])
        htm += "<b>Euler:</b><br />x: " + str(d["x"]) + "<br />y: " + str(d["y"]) + "<br />z: " + str(d["z"]) + "<br />"

        rx = faceRotation(d["x"])
        ry = faceRotation(d["y"])
        rz = faceRotation(d["z"])
        colors = [[
            ["?? 00", "?? 01", "?? 02", "?? 03"],
            ["RG 04", "RW 05", "RB 06", "RY 07"],
            ["YG 08", "YR 09", "YB 10", "YO 11"],
            ["OG 12", "OY 13", "OB 14", "OW 15"]
        ],
            [
                ["?? 16", "?? 17", "?? 18", "?? 19"],
                ["RW 20", "RB 21", "RY 22", "RG 23"],
                ["GW 24", "GR 25", "GY 26", "GO 27"],
                ["OG 28", "OG 29", "OY 30", "OB 31"]
            ],
            [
                ["?? 32", "?? 33", "?? 34", "?? 35"],
                ["RB 36", "RY 37", "RG 38", "RW 39"],
                ["WB 40", "WR 41", "WG 42", "WO 43"],
                ["OB 44", "OW 45", "OG 46", "OY 47"]
            ],
            [
                ["?? 48", "?? 49", "?? 50", "?? 51"],
                ["RY 52", "RG 53", "G3 54", "RB 55"],
                ["BY 56", "BR 57", "BW 58", "BO 59"],
                ["OY 60", "OB 61", "OW 62", "OG 63"]
            ]
        ]
        uc = colors[rx][ry][rz]

        htm = uc[0] + "/" + uc[1]
        print(htm)

        # document.getElementById("pose").innerHTML = htm;

        # encoders
        sides = "URFDLB"
        htm1 = ""
        for i in range(6):
            htm1 += "{}: {}\n".format(sides[i], value[i + 6])

        # document.getElementById("encoders").innerHTML = htm;

        # // twists
        twists = ["U", "?", "U'", "R", "?", "R'", "F", "?", "F'", "D", "?", "D'", "L", "?", "L'", "B", "?", "B'"]
        htm += "Count: {}\n".format(value[12])
        for i in range(13, 19):
            htm += "{} ".format(twists[value[i]])
        # htm+="\n"
        # document.getElementById("twists").innerHTML = htm;

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)


def facelet(value, decoder):
    value = decoder.decrypt(value)
    print(len(value))
    state = []
    for i in range(0, len(value) - 2, 3):
        face = value[i ^ 1] << 16 | value[i + 1 ^ 1] << 8 | value[i + 2 ^ 1]
        for j in range(21, -1, -3):
            print("here 1")
            print(face >> j & 0x7)
            state.append("URFDLB"[(face >> j & 0x7)])
            if (j == 12):
                print("here 2")
                state.append("URFDLB"[i // 3])
    print(state)
    return state


async def connect():
    UUID_SUFFIX = '-0000-1000-8000-00805f9b34fb'
    SERVICE_UUID_META = '0000180a' + UUID_SUFFIX
    CHRCT_UUID_VERSION = '00002a28' + UUID_SUFFIX
    CHRCT_UUID_HARDWARE = '00002a23' + UUID_SUFFIX
    SERVICE_UUID_DATA = '0000fff0' + UUID_SUFFIX
    CHRCT_UUID_F2 = '0000fff2' + UUID_SUFFIX  # cube state, (54 - 6) facelets, 3 bit per facelet var
    CHRCT_UUID_F3 = '0000fff3' + UUID_SUFFIX  # // prev moves
    CHRCT_UUID_F5 = '0000fff5' + UUID_SUFFIX  # // gyro state, move counter, premoves
    CHRCT_UUID_F6 = '0000fff6' + UUID_SUFFIX  # // movecounter, timeoffsets between premoves
    CHRCT_UUID_F7 = '0000fff7' + UUID_SUFFIX;

    try:
        addr = "F8:30:02:08:FB:FE"
        server = BleakClient(addr)
        await server.connect()
        GAN_ENCRYPTION_KEYS = [
            "NoRgnAHANATADDWJYwMxQOxiiEcfYgSK6Hpr4TYCs0IG1OEAbDszALpA",
            "NoNg7ANATFIQnARmogLBRUCs0oAYN8U5J45EQBmFADg0oJAOSlUQF0g"]  # second key
        GAN_SERVICE_UUID = "0000fff0-0000-1000-8000-00805f9b34fb"
        GAN_CHARACTERISTIC_UUID = "0000fff5-0000-1000-8000-00805f9b34fb"
        GAN_SERVICE_UUID_META = "0000180a-0000-1000-8000-00805f9b34fb"
        GAN_CHARACTERISTIC_VERSION = "00002a28-0000-1000-8000-00805f9b34fb"
        GAN_CHARACTERISTIC_UUID_HARDWARE = "00002a23-0000-1000-8000-00805f9b34fb"

        decoder = None
        versionValue = await server.read_gatt_char(GAN_CHARACTERISTIC_VERSION)
        version = versionValue[0] << 16 | versionValue[1] << 8 | versionValue[2]

        if (version > 0x010007 and (version & 0xfffe00) == 0x010000):
            hardwareValue = await server.read_gatt_char(GAN_CHARACTERISTIC_UUID_HARDWARE)
            key = GAN_ENCRYPTION_KEYS[version >> 8 & 0xff]

        # key = JSON.parse(LZString.decompressFromEncodedURIComponent(key))
        key_1 = [198, 202, 21, 223, 79, 110, 19, 182, 119, 13, 230, 89, 58, 175, 186, 162]
        # with open("hard.txt", "rb") as f:
        #   hardwareValue = f.read()
        # f.close()
        key = [67, 226, 91, 214, 125, 220, 120, 216, 7, 96, 163, 218, 130, 60, 1, 241]
        for i in range(6):
            key[i] = (key[i] + hardwareValue[5 - i]) & 0xff
        decoder = aes128(key)
        batt = await server.read_gatt_char(CHRCT_UUID_F7)

        #print(int(get_battery(batt, decoder)), 16)
        # with open ("bin.txt", "rb") as f:
        #   characteristic = f.read()
        # f.close()

        while (True):
            start = time.time()
            ff5 = await server.read_gatt_char(GAN_CHARACTERISTIC_UUID)
            #f6val = await server.read_gatt_char(CHRCT_UUID_F6)
            #f2 = await server.read_gatt_char(CHRCT_UUID_F2)
            #rint("{}".format(facelet(f2,decoder)))
            #time0 = timesOff(f6val, decoder)

            end = time.time()
            pollCharacteristic(ff5, decoder)

    except Exception as ex:
        print(ex)


loop = asyncio.get_event_loop()
loop.run_until_complete(connect())
# key = [59, 18, 93, 222, 120, 218, 120, 216, 7, 96, 163, 218, 130, 60, 1, 241]

