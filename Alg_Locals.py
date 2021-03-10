import time
from .algClass import Alg

class AlgorithmLocals:
    uuid = "0000aadc-0000-1000-8000-00805f9b34fb" #Giiker
    address = "EA:1B:FE:2D:9A:DA" #Giiker
    #address = ""F8:30:02:08:FB:FE""#gan
    #uuid = "0000fff5-0000-1000-8000-00805f9b34fb"
    fail = False
    nextAlg = True
    success = False
    moves = []
    index = []
    results = []  # the results of all the session
    endTraining = False
    isFirstfirstAlg = True
    algStartTime = time.time()
    algEndTime = time.time()
    algFinalTime = algEndTime - algStartTime
    countTraining = 0
    algNumber = 0
    timesUp = False
    startPracticeTime = time.time()
    currentAlg = Alg("")

def checkFail(moves):
    if (len(moves) < 2):
        return False
    size = len(moves)
    if (moves[size - 1] == "U'" and moves[size - 2] == "U"):
        return  True  # the alg faild, try another time
    if (moves[size - 1] == "U" and moves[size - 2] == "U'"):
        return True
    return False
def checkTimesUp (auto, alg):
    if(time.time() - alg.startPracticeTime > auto):
        print("times up",time.time() - alg.startPracticeTime )
        alg.startPracticeTime = time.time()
        return True
    return False

def checkNextAlg(moves):
    if (len(moves) < 2):
        return False
    size = len(moves)
    if (moves[size - 1] == "R" and moves[size - 2] == "R'"):
        return  True  # move to next alg
    if (moves[size - 1] == "R'" and moves[size - 2] == "R"):
        return  True  # move to next alg
    return False

def checkLastAlg(moves):
    if (len(moves) < 2):
        return False
    size = len(moves)
    if (moves[size - 1] == "L" and moves[size - 2] == "L'"):
        return  True  # move to next alg
    if (moves[size - 1] == "L'" and moves[size - 2] == "L"):
        return  True  # move to next alg
    return False

def checkAlgNumber(alg):
    if(alg.algNumber > 21):
        alg.algNumber = 0
    if(alg.algNumber < 0):
        alg.algNumber = 20

def checkEndTraining(moves):
    if (len(moves) < 4):
        return False
    size = len(moves)
    if (moves[size - 1] == "D'" and moves[size - 2] == "D'" and moves[size - 3] == "D'" and moves[size - 4] == "D'"):
        return  True  # move to next alg
    return False
def execAlg(alg, withPair, timesUp):
    a = checkNextAlg(alg.moves)
    b = checkLastAlg(alg.moves) == True
    if (withPair == True and((a==True or b==True) or timesUp == True)):
        print("")
        print(alg.index[3])
    alg.currentAlg.reset()
    alg.currentAlg.movesToExecute = alg.currentAlg.algString
    alg.currentAlg.executeAlg()
    alg.currentAlg.reverseSelf()
    alg.currentAlg.printAlg()
    alg.moves = []  # reset moves
