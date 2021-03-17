import time
import asyncio
from bleak import BleakClient
from decode_gan import aes128
from decode_gan import get_moves
from decode_gan import decData
import time
from algClass import Alg
from algs_dict_init import load_algs_dict
from algs_dict_init import alg_detailed



class Trainer:
    def __init__(self):

        self.data_move_counter = None
        self.fail_times = 0
        self.success = False
        self.letter = ""
        self.new_moves = []
        self.moves = []
        self.recognize_time = None
        endTraining = False
        isFirstfirstAlg = True
        self.algStartTime = None
        self.algEndTime = None
        self.countTraining = 0
        self.start_practice_time = None
        self.training_time_per_alg = None
        self.current_alg = Alg("")
        self.action = ""
        self.algs_dict, self.lp_2_index_edges, self.lp_2_corners_dict = load_algs_dict()
        self.index_train = 0
        timesUp = False
        tryAgain = 0



    def reset_alg(self):
        self.current_alg.algString = self.algs_dict[self.index_train]
        self.current_alg.reset()
        self.current_alg.movesToExecute = self.current_alg.algString
        self.current_alg.executeAlg()
        self.current_alg.reverseSelf()
        self.moves = []
        self.algStartTime = time.time()

    def next_alg_action(self):
        self.index_train = (self.index_train + 1 )%len(self.algs_dict)
        self.reset_alg()
        self.fail_times = 0

    def last_alg_action(self):
        self.index_train = (self.index_train - 1) % len(self.algs_dict)
        self.reset_alg()
        self.fail_times = 0

    def failed_alg_action(self):
        self.reset_alg()
        self.fail_times += 1

    def train_add_action(self):
        self.algs_dict[self.index_train].train_alg = True
        self.reset_alg()

    def finish_training_action(self):
        pass

    def exec_alg_action(self):


    def exec_action(self):
        action = self.action
        if (action == "Last"):
            self.last_alg_action()
        if (action == "Next"):
            self.next_alg_action()
        if (action == "Exec"):
            self.new_moves

        if (action == "Fail"):
            self.failed_alg_action()

        if (action == "Train_add"):
            self.train_add_action()
        if (action == "Finish"):
            self.finish_training()

    def get_restult_alg_time(self):
        return (self.algEndTime - self.algStartTime)

    def check_next_action(self):

        if (len(self.moves) < 2):
            return False
        last_two_moves = self.moves[len(self.moves)-2:len(self.moves)]
        print(last_two_moves)
        if (('L' in last_two_moves) and ("L'" in last_two_moves)) :
            return "Fail"
        if (('F' in last_two_moves) and ("F'" in last_two_moves)) :
            return "Next"
        if (self.check_times_up() == True):
            return "Next"
        if (('B' in last_two_moves) and ("B'" in last_two_moves)) :
            return "Last"
        if (('R' in last_two_moves) and ("R'" in last_two_moves)) :
            return "Train_add"
        if (len(self.moves) >=4):
            last_four_moves = self.moves[len(self.moves) - 4 : len((self.moves))]
            if(last_four_moves.count("D'") == 4 or last_four_moves.count("D") == 4):
                return "Finish"
        return "Exec"

    def check_times_up (self):
        if(time.time() - self.start_practice_time > self.training_time_per_alg):
            self.startPracticeTime = time.time()
            return True
        return False


def get_new_moves(data, counter):
    moves = get_moves(data)
    new_counter = data[12]
    new_moves = []
    for i in range (new_counter-counter):
        new_moves.append(moves[5-i])
    return new_moves





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
    ff5 = decData(await server.read_gatt_char(CHRCT_UUID_F5), decoder)
    trainer = Trainer()
    trainer.data_move_counter= ff5[12]
    while (True):
        start = time.time()
        ff5 = decData(await server.read_gatt_char(CHRCT_UUID_F5), decoder)
        trainer.new_moves = get_new_moves(ff5, trainer.data_move_counter)
        trainer.moves += trainer.new_moves
        trainer.data_move_counter = ff5[12]
        print(trainer.check_next_action())

loop = asyncio.get_event_loop()
loop.run_until_complete(connect())


