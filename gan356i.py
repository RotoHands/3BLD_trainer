
import asyncio
import time
from drill import genAlg
from drill import saveResults
from algClass import Alg
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import keyboard
import setting
import pyautogui



class Trainer:
    def __init__(self):
        self.data_move_counter = None
        self.fail = False
        self.nextAlg = True
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
        timesUp = False
        tryAgain = 0

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
        if (len(self.moves) >=4):
            last_four_moves = self.moves[len(self.moves) - 4 : len((self.moves))]
            if(last_four_moves.count("D'") == 4 or last_four_moves.count("D") == 4):
                return "Finish"
        return "Continue"
    def check_times_up (self):
        if(time.time() - self.start_practice_time > self.training_time_per_alg):
            self.startPracticeTime = time.time()
            return True
        return False

    def action_next(self):
        pass


def init_alg_list():




def execAlg(alg, withPair, timesUp, algTrainedFinish):
    a = checkNextAlg(alg.moves)
    b = checkLastAlg(alg.moves)
    if ((withPair == True and((a==True or b==True) or timesUp == True) )or algTrainedFinish == True):
        print("")
        print(alg.letter)
        st = alg.letter
        file = open(r"C:\Users\rotem\PycharmProjects\pythonProject\BLD\currentLetterPair.txt", "w", encoding='utf8')
        if (len(st) == 3):
            if(st[2] == "'"):
                st = "'" + st[0:2]
        file.write(st)
    alg.currentAlg.reset()
    alg.currentAlg.movesToExecute = alg.currentAlg.algString
    alg.currentAlg.executeAlg()
    alg.currentAlg.reverseSelf()

    alg.moves = []  #reset moves

def Gan356i(piece, timePerLetter,algNumStart,alg, withPair, autoTransitionPerAlg,tryAgainTimes):

    def algorithm(move):
        alg.moves.append(move)
        alg.timesUp = checkTimesUp(autoTransitionPerAlg, alg)

        if (checkNextAlg(alg.moves) == True or alg.isFirstfirstAlg == True or alg.timesUp == True):
            alg.tryAgain=0
            open(r"C:\Users\rotem\PycharmProjects\pythonProject\BLD\algString.txt", "w", encoding='utf8').close()

            alg.countTraining = 0
            alg.algNumber += 1
            alg.isFirstfirstAlg = False
            generatedAlg = genAlg(alg.algNumber, piece)
            alg.currentAlg.algString = generatedAlg[1]
            alg.index = generatedAlg [0]
            alg.letter = generatedAlg[2]

            execAlg(alg, withPair, alg.timesUp, False)
            if (alg.timesUp == True):
                alg.timesUp = False
                print(alg.results)
                saveResults(alg.results, piece)
                alg.results = []
                print("finished entering")
                f = open(r"C:\Users\rotem\PycharmProjects\pythonProject\BLD\‏‏currentLetterPairResults.txt", "a")
                f.write("f ")
                f.close()
            alg.startPracticeTime = time.time()
            alg.moves = []

        elif (checkLastAlg(alg.moves) == True):  # move to last alg

            alg.countTraining = 0
            alg.algNumber -= 1
            alg.tryAgain=0
            open(r"C:\Users\rotem\PycharmProjects\pythonProject\BLD\algString.txt", "w", encoding='utf8').close()
            generatedAlg = genAlg(alg.algNumber, piece)
            alg.letter = generatedAlg[2]
            alg.currentAlg.algString = generatedAlg[1]
            alg.index = generatedAlg[0]
            execAlg(alg, withPair, alg.timesUp, False)
            alg.moves = []

        elif (checkFail(alg.moves) == True):  # do the algorithm again

            print(", ", end = "", flush=True)
            f = open(r"C:\Users\rotem\PycharmProjects\pythonProject\BLD\‏‏currentLetterPairResults.txt", "a")
            f.write(", ")
            f.close()
            alg.tryAgain+=1
            if(alg.tryAgain >tryAgainTimes):
                f = open(r"C:\Users\rotem\PycharmProjects\pythonProject\BLD\algString.txt", "w", encoding='utf8')
                f.write(alg.currentAlg.algString)
                f.close()
            alg.currentAlg.reset()
            alg.currentAlg.movesToExecute = alg.currentAlg.algString
            alg.currentAlg.executeAlg()
            alg.currentAlg.reverseSelf()
            alg.moves = []  # reset moves
        elif (checkEndTraining(alg.moves) == True):  # finish training session
            print("finished")
            saveResults(alg.results, piece)
            alg.results = []
            alg.startPracticeTime = time.time()
            print("finished entering")
            f = open(r"C:\Python\PythonWork\BLD\RotoBLD\‏‏currentLetterPairResults.txt", "a")
            f.write("f ")
            f.close()

        else:# execute the current move
            if (len(alg.moves)  == 1):
                alg.algStartTime = time.time()
            currentMoves = alg.moves[len(alg.moves) - 1]
            alg.currentAlg.movesToExecute = currentMoves
            alg.currentAlg.executeAlg()

            if(alg.currentAlg.isSolved == True):
                alg.currentAlg.isSolved = False
                alg.algEndTime = time.time()
                alg.algFinalTime = alg.algEndTime - alg.algStartTime
                print("%.1f, " % alg.algFinalTime,end = "", flush=True )
                f = open(r"C:\Users\rotem\PycharmProjects\pythonProject\BLD\‏‏currentLetterPairResults.txt", "w")
                f.write("%.2f" % alg.algFinalTime)
                f.close()
                alg.tryAgain=0
                open(r"C:\Users\rotem\PycharmProjects\pythonProject\BLD\algString.txt", "w", encoding='utf8').close()
                if(piece == "corners"):
                    file = open('timesCor.txt','a')
                else:
                    file = open('timesEd.txt','a')
                strApp = str(alg.index[0]) + "," + str(alg.index[1]) + "," + str(round(alg.algFinalTime,2))+";"
                file.write(strApp)
                file.close()
                alg.countTraining += 1
                alg.results.append([alg.index, alg.algFinalTime])
                alg.currentAlg.reset()
                alg.currentAlg.movesToExecute = alg.currentAlg.algString
                alg.currentAlg.executeAlg()
                alg.currentAlg.reverseSelf()
                alg.moves = []  # reset moves
                alg.algStartTime = time.time()

                if (alg.countTraining == timePerLetter):
                    alg.tryAgain = 0
                    open(r"C:\Users\rotem\PycharmProjects\pythonProject\BLD\algString.txt", "w", encoding='utf8').close()

                    alg.countTraining = 0
                    alg.algNumber += 1
                    alg.isFirstfirstAlg = False
                    generatedAlg = genAlg(alg.algNumber, piece)
                    alg.currentAlg.algString = generatedAlg[1]
                    alg.index = generatedAlg[0]
                    alg.letter = generatedAlg[2]
                    execAlg(alg, withPair, alg.timesUp, True)
                    alg.startPracticeTime = time.time()
                    alg.moves = []
    movesList = ["U", "U2", "U'", "R", "R2", "R'", "F", "F2", "F'", "D", "D2", "D'", "L", "L2", "L'", "B", "B2", "B'"]
    moves = []
    alg.algNumber = algNumStart
    alg.startPracticeTime = time.time()
    flag = True
    lastMoves = []
    script = "return temp1"
    browser.execute_script("window.open('http://localhost/3bldweb.php');")
    while(True):
        try:
            moves = browser.execute_script(script)
            newMoves = findNewMoves(lastMoves, moves)
            lastMoves = moves
            for move in newMoves:
                algorithm(movesList[move])
        except:
            a = input("press enter when finish to reconnect")


