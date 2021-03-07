from bleak import BleakClient
import asyncio
import keyboard
import time
import setting
from drill import genEdge
from drill import genCor
from drill import saveResults
from algClass import Alg

def checkSlice(value):

    moves =[]
    x = faceConversion(value[16]//16, value[16]%16)
    y = faceConversion(value[17] // 16, value[17] % 16)
    flag = False

    if(x == "R" and y == "L'"):
        #moves.append("x'")
        moves.append(y)
        #print("here 1")
    elif(x == "R'" and y == "L"):
        #moves.append("x")
        moves.append(y)
    elif (x == "U'" and y == "D'"):
    # moves.append("x")
        moves.append(y)
    elif (x == "U" and y == "D"):
        # moves.append("x")
        moves.append(y)
    elif (y == "U'" and x == "D'"):
        # moves.append("x")
        moves.append(y)
    elif (y == "U" and x == "D"):
        # moves.append("x")
        moves.append(y)

        #print("here 2")
    elif(x == "F" and y == "B'"):
        #moves.append("z'")
        moves.append(y)
        #print("here 3")
    elif(x == "F'" and y == "B"):
        #moves.append("z")
        moves.append(y)
        #print("here 4")
    elif(x == "U" and y == "D'"):
        #moves.append("y'")
        moves.append(y)
        #print("here 5")
    elif (x == "U'" and y == "D"):
        #moves.append("y")
        moves.append(y)
        #print("here 6")
    elif (y == "R" and x == "L'"):
        #moves.append("x'")
        moves.append(y)
        #print("here 7")
    elif (y == "R'" and x == "L"):
        #moves.append("x")
        moves.append(y)
        #print("here 8")
    elif (y == "F" and x == "B'"):
        #moves.append("z'")
        moves.append(y)
        #print("here 9")
    elif (y == "F'" and x == "B"):
        #moves.append("z")
        moves.append(y)
        #print("here 10")
    elif (y == "U" and x == "D'"):
        #moves.append("y'")
        moves.append(y)
        #print("here 11")
    elif (y == "U'" and x == "D"):
        #moves.append("y")
        moves.append(y)
        #print("here 12")

    else:
        moves.append(x)
        flag = True
        #print("here 13")


    if (flag == False):
        #print("here 14")
        moves.append(x)
        moves.append("x")
        moves.append("x'")
    return moves
def printMoves(value):
    moves=[]
    for i in range (16,20):
        moves.append(faceConversion(value[i] // 16, value[i] % 16))

    #moves = [move1,move2, move3, move4]
    print (*moves ,sep=" ")

def algMoves(value,moves):#moves has 2 attributes :time and move
    move1 = faceConversion(value[16] // 16, value[16] % 16)
    move2 = faceConversion(value[17] // 16, value[17] % 16)
    move3 = faceConversion(value[18] // 16, value[18] % 16)
    move4 = faceConversion(value[19] // 16, value[19] % 16)
    currentMoves =[move1, move2,move3,move4]

def faceConversion (faceIndex, amount):
    faces = ["", "B", "D", "L", "U", "R", "F"]
    if(amount == 1):
        return faces[faceIndex]
    elif(amount == 3):
        return faces[faceIndex] + '\''
    elif (amount == 9):
        return faces[faceIndex] + '2'
    else:
        print("here 1 with amount:" , amount)

def checkFail(moves):
    if (len(moves) < 2):
        return False
    size = len(moves)
    if (moves[size - 1] == "U'" and moves[size - 2] == "U"):
        return  True  # the alg faild, try another time
    return False

def checkOperation(moves):
    if (len(moves) < 2):
        return False
    size = len(moves)
    if (moves[size - 1] == "R" and moves[size - 2] == "R'"):
        return  True  # move to next alg
    return False

def checkEndTraining(moves):
    if (len(moves) < 4):
        return False
    size = len(moves)
    if (moves[size - 1] == "D'" and moves[size - 2] == "D'" and moves[size - 3] == "D'" and moves[size - 4] == "D'"):
        return  True  # move to next alg
    return False
def genAlg(index, piece):
    if (piece == "corners"):
        algString = setting.corAlgs.cell(index[0], index[1]).value
    elif(piece == "edges"):
        algString = setting.edAlgs.cell(index[0], index[1]).value
    else:
        print("error 1")

    return algString

async def Giiker(address, loop, piece, letterDrill, isRandom, nextAlgCount):
    modelNum = "00002a29-0000-1000-8000-00805f9b34fb"
    service = "0000aadb-0000-1000-8000-00805f9b34fb"
    uuid = "0000aadc-0000-1000-8000-00805f9b34fb"
    address = "EA:1B:FE:2D:9A:DA"
    current = ""
    fail = False
    nextAlg = True
    success = False
    moves = []
    results = []# the results of all the session
    i =0
    endTraining = False

    async with BleakClient(address, loop=loop) as client:


        while(endTraining == False):
            if (nextAlg == True):# if diddn't fail then generate a new random alg
                if (piece == "corners"):
                    index = genCor(letterDrill, isRandom, nextAlgCount)
                elif(piece == "edges"):
                    index = genEdge(letterDrill, isRandom, nextAlgCount)
                    nextAlgCount  = index[2]
                else:
                    print("error 2")
                nextAlgCount+=1
                moves = []
                nextAlg = False
            #otherwise the current alg will trained agian
            currentAlg = Alg(genAlg(index, piece))
            currentAlg.executeAlg()
            currentAlg.reverseSelf()
            currentAlg.printAlg()
            # alg.printState()

            #starts the timer of the alg execution
            algStart = time.time()
            while (success == False):  # only one alg executed

                nextAlg = checkOperation(moves)
                fail = checkFail(moves)
                endTraining = checkEndTraining(moves)
                if(fail == True or nextAlg == True or endTraining == True):
                    moves = []
                    break

                value =bytes(await client.read_gatt_char(uuid))
                last = current
                current = value

                if ((current != last and last != "")):
                    lastMoves = checkSlice(value)
                    for x in lastMoves:
                        currentAlg.move(x)
                        moves.append(x)
                        currentAlg.executeAlg()

                    #print("moves applied", *moves, sep = " ")
                    #printMoves(value)
                    #currentAlg.printState()
                success = currentAlg.isSolved

            if (success == True): #complited the alg successfully
                moves = []
                algEnd = time.time()
                algTime  = algEnd - algStart
                results.append([index, algTime])
                success = False
                i+=1
                print(i, ". Success! time is %.2f" % algTime )
        print("finished")
        print("results are :", *results, sep = " ")
        saveResults(results, piece)
