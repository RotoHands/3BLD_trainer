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
import pickle
from datetime import datetime
import shutil

class Trainer:
    def __init__(self):
        self.data = None
        self.data_move_counter = None
        self.fail_times = 0
        self.success = False
        self.letter = ""
        self.new_moves = []
        self.moves = []
        self.use_recognize = True
        self.recognize_time_finished = False
        self.recognize_time = None
        endTraining = False
        self.algStartTime = 0
        self.algEndTime = None
        self.countTraining = 0
        self.start_practice_time = time.time()
        self.training_time_per_alg = 10
        self.action = ""
        self.index_train = 500
        self.save_timer_diff = 300
        self.save_timer = time.time()
        self.pkl_path = "dicts.pkl"
        self.pkl_path_backup = "dicts_backup.pkl"
        self.algs_dict, self.lp_2_index_edges, self.lp_2_corners_dict = load_algs_dict(self.pkl_path)

        self.current_alg = Alg(self.algs_dict[self.index_train].alg_string)
        self.reset_alg() # initialize alg

        self.ble_server = None
        self.addr = "F8:30:02:08:FB:FE"
        self.timesUp = False
        self.finish_training = False
        self.try_again_before_string = 3



    def reset_alg(self):

        if (self.use_recognize):
            self.recognize_time = time.time()
            self.recognize_time_finished = False
        self.startPracticeTime = time.time()
        self.current_alg.algString = self.algs_dict[self.index_train].alg_string
        self.current_alg.reset()
        self.current_alg.movesToExecute = self.current_alg.algString
        self.current_alg.executeAlg()
        self.current_alg.reverseSelf()
        self.moves = []
        self.algStartTime = 0
        print(self.algs_dict[self.index_train])

    def next_alg_action(self):
        self.index_train = (self.index_train + 1 )%len(self.algs_dict)
        self.reset_alg()
        self.fail_times = 0
        self.start_practice_time = time.time()


    def last_alg_action(self):
        self.index_train = (self.index_train - 1) % len(self.algs_dict)
        self.reset_alg()
        self.fail_times = 0
        self.start_practice_time = time.time()

    def failed_alg_action(self):
        self.reset_alg()
        self.fail_times += 1

    def train_add_action(self):
        self.algs_dict[self.index_train].train_alg = True
        self.reset_alg()

    def finish_training_action(self):
        self.finish_training = True
        self.save_solves()
        shutil.copy(self.pkl_path, self.pkl_path_backup)


    def add_solve_to_dict(self):
        solve_time = float("%.2f"%(time.time() - self.algStartTime))
        if (self.use_recognize):
            self.recognize_time = time.time()
            self.algs_dict[self.index_train].solves_times.append(((solve_time, self.recognize_time),datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        else:
            self.algs_dict[self.index_train].solves_times.append(((solve_time),datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        print(solve_time)
    def exec_alg_action(self):

        if(len(self.moves) > 0 and self.algStartTime == 0):
            self.algStartTime = time.time()

        if (self.use_recognize and len(self.moves) > 0 and not self.recognize_time_finished):
            self.recognize_time = time.time() - self.recognize_time
            self.recognize_time_finished = True
        self.new_moves.reverse()
        for move in self.new_moves:
            self.current_alg.movesToExecute = move
            self.current_alg.executeAlg()

        if self.current_alg.isSolved:
            self.add_solve_to_dict()
            self.next_alg_action()

    def exec_action(self):

        self.action = self.check_next_action()
        action = self.action

        if (action == "Last"):
            self.last_alg_action()
        if (action == "Next"):
            self.next_alg_action()
        if (action == "Exec"):
            self.exec_alg_action()
        if (action == "Fail"):
            self.failed_alg_action()
        if (action == "Train_add"):
            self.train_add_action()
        if (action == "Finish"):
            self.finish_training_action()

    def get_restult_alg_time(self):
        return (self.algEndTime - self.algStartTime)

    def check_next_action(self):
        if (len(self.moves) < 2):
            return "Exec"
        last_two_moves = self.moves[len(self.moves)-2:len(self.moves)]
        if (('L' in last_two_moves) and ("L'" in last_two_moves)) :
            return "Fail"
        if (('F' in last_two_moves) and ("F'" in last_two_moves)) :
            return "Next"
        if (self.check_times_up() == True):
            return "Next"
        if (('B' in last_two_moves) and ("B'" in last_two_moves)) :
            return "Last"
        #if (('R' in last_two_moves) and ("R'" in last_two_moves)) :
            #return "Train_add"
        if (len(self.moves) >=4):
            last_four_moves = self.moves[len(self.moves) - 4 : len((self.moves))]
            if(last_four_moves.count("D'") == 4 or last_four_moves.count("D") == 4):
                return "Finish"
        return "Exec"

    def save_solves(self):
        if((time.time() - self.save_timer > self.save_timer_diff) or self.finish_training):
            with open (self.pkl_path, "wb") as f:
                pickle.dump((self.algs_dict, self.lp_2_index_edges, self.lp_2_corners_dict), f)
                print("saved!")
            self.save_timer = time.time()

    def check_times_up (self):
        if(time.time() - self.start_practice_time > self.training_time_per_alg):
            return True
        return False

    def print_solves(self, index):
        for solve in self.algs_dict[index].solves_times:
            print (solve)

def get_new_moves(data, counter):
    moves = get_moves(data)
    new_counter = data[12]
    new_moves = []

    for i in range ((new_counter-counter)%256):
        new_moves.append(moves[5-i])
    return new_moves


async def connect():
    UUID_SUFFIX = '-0000-1000-8000-00805f9b34fb'
    CHRCT_UUID_F3 = '0000fff3' + UUID_SUFFIX  # // prev moves
    CHRCT_UUID_F5 = '0000fff5' + UUID_SUFFIX  # // gyro state, move counter, premoves
    CHRCT_UUID_F7 = '0000fff7' + UUID_SUFFIX

    trainer = Trainer()
    trainer.ble_server = BleakClient(trainer.addr)
    await trainer.ble_server.connect()
    key = [59, 18, 93, 222, 120, 218, 120, 216, 7, 96, 163, 218, 130, 60, 1, 241]
    decoder = aes128(key)
    batt = await trainer.ble_server.read_gatt_char(CHRCT_UUID_F7)
    print(batt[7])
    trainer.data = decData(await trainer.ble_server.read_gatt_char(CHRCT_UUID_F5), decoder)
    trainer.data_move_counter= trainer.data[12]
    while (not trainer.finish_training):

        trainer.save_solves()
        trainer.data = decData(await trainer.ble_server.read_gatt_char(CHRCT_UUID_F5), decoder)
        trainer.new_moves = get_new_moves(trainer.data, trainer.data_move_counter)
        trainer.moves += trainer.new_moves
        trainer.data_move_counter = trainer.data[12]
        trainer.exec_action()

    await trainer.ble_server.disconnect()

    for i in range (500, 503):
        print(trainer.algs_dict[i])
        trainer.print_solves(i)

loop = asyncio.get_event_loop()
loop.run_until_complete(connect())


