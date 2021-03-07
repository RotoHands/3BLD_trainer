import time
from algClass import Alg
from LocalTrainer import printLetterPair2

class AlgorithmLocals:
    uuid = "0000aadc-0000-1000-8000-00805f9b34fb" #Giiker
    address = "EA:1B:FE:2D:9A:DA" #Giiker
    #address = "4C:24:98:6A:7A:65"#gan
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
def faceConversion (faceIndex, amount):
    faces = ["", "B", "D", "L", "U", "R", "F"]
    if(amount == 1):
        return (faces[faceIndex])
    elif(amount == 3):
        return(faces[faceIndex] + '\'')
    elif (amount == 9):
        return (faces[faceIndex] + '2')
    else:
        print("here 1 with amount:" , amount)
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
        printLetterPair2(alg.index[3])
    alg.currentAlg.reset()
    alg.currentAlg.movesToExecute = alg.currentAlg.algString
    alg.currentAlg.executeAlg()
    alg.currentAlg.reverseSelf()
    alg.currentAlg.printAlg()
    alg.moves = []  # reset moves


"""""
async def GiikerNew(address, loop, piece, letterDrill,algNumStart, isRandom, trainingTime,alg, withPair, autoTransitionPerAlg):

    async with BleakClient(address, loop=loop) as client:

        alg.algNumber = algNumStart
        alg.startPracticeTime = time.time()
        def algorithm(sender, data):
            value = bytes(data)
            alg.moves.append(faceConversion(value[16] // 16, value[16] % 16))
            alg.timesUp = checkTimesUp(autoTransitionPerAlg, alg)

            if (checkNextAlg(alg.moves) == True or alg.isFirstfirstAlg == True or alg.timesUp == True):  # move to next alg


                alg.algNumber += 1
                alg.isFirstfirstAlg = False
                generatedAlg = genAlg(letterDrill, isRandom, alg.algNumber, piece)
                #alg.algNumber = generatedAlg[2]
                alg.currentAlg.algString = generatedAlg [1]
                alg.index = generatedAlg [0] # gen new alg
                checkAlgNumber(alg)# prevent out of bound
                execAlg(alg, withPair, alg.timesUp)
                if (alg.timesUp == True):
                    alg.timesUp = False
                    print(alg.results)
                    saveResults(alg.results, piece)
                    alg.results = []
                    print("finished entering")
                alg.startPracticeTime = time.time()
                alg.moves = []

            elif (checkLastAlg(alg.moves) == True):  # move to last alg

                alg.algNumber -= 1
                checkAlgNumber(alg)# prevent out of bound
                generatedAlg = genAlg(letterDrill, isRandom,alg.algNumber, piece)
                #alg.algNumber = generatedAlg[2]
                alg.currentAlg.algString = generatedAlg[1]
                alg.index = generatedAlg[0]  # gen new alg
                execAlg(alg, withPair, alg.timesUp)
                alg.moves = []

            elif (checkFail(alg.moves) == True):  # do the algorithm again

                print(", ", end = "", flush=True)
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

            else:# execute the current move
                if (len(alg.moves) == 1):
                    alg.algStartTime = time.time()
                currentMoves = alg.moves[len(alg.moves) - 1]
                alg.currentAlg.movesToExecute = currentMoves
                alg.currentAlg.executeAlg()

                if(alg.currentAlg.isSolved == True):
                    alg.currentAlg.isSolved = False
                    alg.algEndTime = time.time()
                    alg.algFinalTime = alg.algEndTime - alg.algStartTime
                    print("%.1f, " % alg.algFinalTime,end = "", flush=True )
                    alg.countTraining += 1
                    alg.results.append([alg.index, alg.algFinalTime])
                    alg.currentAlg.reset()
                    alg.currentAlg.movesToExecute = alg.currentAlg.algString
                    alg.currentAlg.executeAlg()
                    alg.currentAlg.reverseSelf()
                    alg.moves = []  # reset moves
                    alg.algStartTime = time.time()


        await client.start_notify("0000aadc-0000-1000-8000-00805f9b34fb", algorithm)
        await asyncio.sleep(trainingTime, loop=loop)
"""