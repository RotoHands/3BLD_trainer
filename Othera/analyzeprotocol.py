
def findInLine(word,line):
    for i in range (len(line)-1):
        if (line[i:i+2] == word):
            return True
    return False
def countApperenceStreak(word,lines):
    count = 0
    for line in lines:
        if (findInLine(word,line) == True):
            count+=1
        else:
           return count

    return count
def countApperenceStreak2(word,lines):
    count = 0
    for line in lines:
        if (findInLine(word,line) == True):
            count+=1

    return count

def func():
    allPack = open("a.txt","r")
    listPack = allPack.readlines()
    newList = []
    for x in listPack:
        newList.append(x[:len(x)-1])
    allPack.close()
    print(newList)
    countList = []
    i=0
    c = 0
    for pack in newList:
        for i in range(len(pack)-1):
            current = pack[i:i+2]
            currentCount = countApperenceStreak2(current,newList)
            countList.append([currentCount,current])
            i+=2
        c+=1
    countList.sort(reverse= True)
    print(*countList, sep = "\n")
func()