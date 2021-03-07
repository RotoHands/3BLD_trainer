from openpyxl import load_workbook
def getEdgesToTrainIndex():
    lettersEdgesTrain = ['א', 'ב', 'ד', 'ה', 'ו', 'ז', 'ח', 'י', 'כ', 'ל', 'מ', 'נ', 'ס', 'ע', 'פ', 'צ', 'ק', 'ר', 'ש',
                         'ת','1', '2']
    letterTrainEd = open(r"C:\Users\rotem\PycharmProjects\pythonProject\BLD\algTrainingList\trainingSetEdges.txt", "r", encoding="utf8")
    EdTrain = []
    for line in letterTrainEd:
        print(line)
        print([lettersEdgesTrain.index(line[1])+2, lettersEdgesTrain.index(line[0])+2])
        EdTrain.append([lettersEdgesTrain.index(line[1])+2, lettersEdgesTrain.index(line[0])+2])
    return EdTrain

def getCorToTrainIndex():
    lettersCornersTrain = ['א', 'ב', 'ד', 'ה', 'ו', 'ז', 'ח', 'ט', 'כ', 'ל', 'נ', 'ס', 'ע', 'פ', 'צ', 'ק', 'ר', 'ש',
                           'ת','1', '2']
    letterTrainCor = open(r"C:\Users\rotem\PycharmProjects\pythonProject\BLD\algTrainingList\trainingSetCorners.txt", "r", encoding="utf8")
    CorTrain = []
    for line in letterTrainCor:

        CorTrain.append([lettersCornersTrain.index(line[1])+2, lettersCornersTrain.index(line[0])+2])
    print(CorTrain)
    return CorTrain
def init():
    global wb
    global corD
    global edD
    global edAlgs
    global corAlgs
    global lettersCorners
    global lettersEdges
    global letters
    global sheet
    global quizlet
    global CorTrain
    global EdTrain
    global numlineE
    global numlineC




    wb = load_workbook('ROTO 3bld Algs.xlsx', data_only=True)
    edAlgs = wb["edges"]
    corAlgs = wb["corners"]
    corD = wb["corners - drill"]
    edD = wb["edges - drill"]
    lettersCorners = ['א', 'ב', 'ד', 'ה', 'ו', 'ז', 'ח', 'ט', 'כ', 'ל', 'נ', 'ס', 'ע', 'פ', 'צ', 'ק', 'ר', 'ש', 'ת',
                      'צ\'', 'ג\'']
    lettersEdges = ['א', 'ב', 'ד', 'ה', 'ו', 'ז', 'ח', 'י', 'כ', 'ל', 'מ', 'נ', 'ס', 'ע', 'פ', 'צ', 'ק', 'ר', 'ש', 'ת',
                    'צ\'', 'ג\'']


    letters = ['א', 'ב', 'ג', 'ד', 'ה', 'ו', 'ז', 'ח', 'ט', 'י', 'כ', 'ל', 'מ', 'נ', 'ס', 'ע', 'פ', 'צ', 'ק', 'ר', 'ש',
               'ת', '1', '2']
    EdTrain = getEdgesToTrainIndex()
    CorTrain = getCorToTrainIndex()
    w = open(r"C:\Users\rotem\PycharmProjects\pythonProject\BLD\algTrainingList\trainingSetCorners.txt", "r",
             encoding="utf-8")
    numlineC =0
    numlineE = 0
    for l in w:
        numlineC += 1
    w2 = open(r"C:\Users\rotem\PycharmProjects\pythonProject\BLD\algTrainingList\trainingSetEdges.txt", "r",
             encoding="utf-8")
    for l in w2:
        numlineE+= 1



init()