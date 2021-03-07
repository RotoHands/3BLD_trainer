#-*- coding: utf-8 -*-
from testMove1 import AlgorithmLocals
from gan356i import Gan356i
import setting

if __name__ == "__main__":
    print("get ready!")
    setting.init()

    #address = "4C:24:98:6A:7A:65" # GAN
    address = "EA:1B:FE:2D:9A:DA"
    alg = AlgorithmLocals()
    alg.algNumber = 0
    c = "corners"

    e = "edges"


    piece = e
    letter = "צ"
    timePerLetter = 3
    tryAgainTimes = -1
    withPair = True
    isRandom = False
    autoTransitionPerAlg = 3000.0
    f = open(r"C:\Users\rotem\PycharmProjects\pythonProject\BLD\‏‏currentLetterPairResults.txt", "w")
    f.write("1.2")
    f.close()
    Gan356i(piece, int(timePerLetter), alg.algNumber, alg, withPair, autoTransitionPerAlg,tryAgainTimes)

