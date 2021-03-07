lettersCorners = ['א', 'ב', 'ד', 'ה', 'ו', 'ז', 'ח', 'ט', 'כ', 'ל', 'נ', 'ס', 'ע', 'פ', 'צ', 'ק', 'ר', 'ש', 'ת',
                  'צ\'', 'ג\'']
lettersEdges = ['א', 'ב', 'ד', 'ה', 'ו', 'ז', 'ח', 'י', 'כ', 'ל', 'מ', 'נ', 'ס', 'ע', 'פ', 'צ', 'ק', 'ר', 'ש', 'ת',
                'צ\'', 'ג\'']
letters = ['א', 'ב', 'ג', 'ד', 'ה', 'ו', 'ז', 'ח', 'ט', 'י', 'כ', 'ל', 'מ', 'נ', 'ס', 'ע', 'פ', 'צ', 'ק', 'ר', 'ש',
           'ת', '1', '2']




def getEdgesToTrainIndex():
    lettersEdgesTrain = ['א', 'ב', 'ד', 'ה', 'ו', 'ז', 'ח', 'י','כ', 'ל','מ', 'נ', 'ס', 'ע', 'פ', 'צ', 'ק', 'ר', 'ש',
                           'ת', '1', '2']

    letterTrainEd = open(r"C:\Users\rotem\PycharmProjects\pythonProject\BLD\algTrainingList\trainingSetEdges.txt", "r", encoding="utf8")
    EdTrain = []
    for line in letterTrainEd:
        EdTrain.append([lettersEdgesTrain.index(line[1])+1, lettersEdgesTrain.index(line[0])+1])
    return EdTrain

def getCorToTrainIndex():
    lettersCornersTrain = ['א', 'ב', 'ד', 'ה', 'ו', 'ז', 'ח', 'ט', 'כ', 'ל', 'נ', 'ס', 'ע', 'פ', 'צ', 'ק', 'ר', 'ש',
                           'ת', '1', '2']
    letterTrainCor = open(r"C:\Users\rotem\PycharmProjects\pythonProject\BLD\algTrainingList\trainingSetCorners.txt", "r", encoding="utf8")
    CorTrain = []
    for line in letterTrainCor:
        CorTrain.append([lettersCornersTrain.index(line[1])+1, lettersCornersTrain.index(line[0])+1])
    return CorTrain
