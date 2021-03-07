
import asyncio
import time
from drill import genAlg
from drill import saveResults
from algClass import Alg
from LocalTrainer import printLetterPair2
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import keyboard
import setting
import pyautogui



class AlgorithmLocals:
    uuid = "0000aadc-0000-1000-8000-00805f9b34fb" #Giiker
    address = "EA:1B:FE:2D:9A:DA" #Giiker
    #address = "4C:24:98:6A:7A:65"#gan
    #uuid = "0000fff5-0000-1000-8000-00805f9b34fb"
    fail = False
    nextAlg = True
    success = False
    letter = ""
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
    tryAgain = 0

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
    if (moves[size - 1] == "L" and moves[size - 2] == "L'"):
        return  True  # the alg faild, try another time
    if (moves[size - 1] == "L'" and moves[size - 2] == "L"):
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
    if (moves[size - 1] == "F" and moves[size - 2] == "F'"):
        return  True  # move to next alg
    if (moves[size - 1] == "F'" and moves[size - 2] == "F"):
        return  True  # move to next alg
    return False

def checkLastAlg(moves):
    if (len(moves) < 2):
        return False
    size = len(moves)
    if (moves[size - 1] == "B" and moves[size - 2] == "B'"):
        return  True  # move to next alg
    if (moves[size - 1] == "B'" and moves[size - 2] == "B"):
        return  True  # move to next alg
    return False
def checkEndTraining(moves):
    if (len(moves) < 4):
        return False
    size = len(moves)
    if (moves[size - 1] == "D'" and moves[size - 2] == "D'" and moves[size - 3] == "D'" and moves[size - 4] == "D'"):
        return  True  # move to next alg
    return False
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
    def pyauto():
        pyautogui.click(42, 160)  # options
        time.sleep(1)
        pyautogui.click(313, 400)  # timer
        time.sleep(1)
        pyautogui.click(436, 413)  # timer
        time.sleep(1)
        pyautogui.click(443, 511)  # giiker
        time.sleep(3)
        pyautogui.click(588, 146)  # GAN
        time.sleep(1)
        pyautogui.click(616, 487)  # OK
        time.sleep(12)
        pyautogui.click(431, 189)  # accecpt
        time.sleep(3)
        pyautogui.rightClick(431, 189)
        time.sleep(1)
        pyautogui.click(369, 420)
        time.sleep(2)
        pyautogui.click(664, 141)  # console
        time.sleep(2)
        pyautogui.click(539, 681)  # console
        pyautogui.write('console.clear()')
        time.sleep(0.5)
        pyautogui.press('enter')
        time.sleep(0.5)
        pyautogui.write("giikerutil")
        time.sleep(0.5)
        pyautogui.press('enter')
        time.sleep(0.5)
        pyautogui.click(526, 265)
        time.sleep(0.5)
        pyautogui.click(540, 367)
        time.sleep(0.5)
        pyautogui.click(551, 496)
        time.sleep(0.5)
        pyautogui.click(560, 510)
        time.sleep(0.5)
        pyautogui.scroll(-500)
        time.sleep(0.5)
        pyautogui.rightClick(589, 584)
        time.sleep(0.5)
        pyautogui.click(500, 658)
        time.sleep(0.5)
        pyautogui.click(39, 113)
        time.sleep(0.5)
    def findNewMoves(lastMoves, currentMoves):
        lastLen = len(lastMoves)
        if (lastLen != len(currentMoves)):
            return currentMoves[lastLen:]
        return []


    browser = webdriver.Chrome(ChromeDriverManager().install())
    browser.get("https://cstimer.net/new")
    #pyauto()
    a=input("press enter when finished")
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


