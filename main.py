#-*- coding: utf-8 -*-
from Alg_Locals import AlgorithmLocals
from gan356i import Gan356i
from  setting import  init

if __name__ == "__main__":
    print("get ready!")
    init()

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
    Gan356i(piece, int(timePerLetter), alg.algNumber, alg, withPair, autoTransitionPerAlg,tryAgainTimes)

