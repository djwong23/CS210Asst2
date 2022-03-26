import re
import math

#PREPROCESSING

f = 'tfidf_docs.txt'
fileList = open(f)

stopWordsFile = open('stopwords.txt')
stopWords = set()
for word in stopWordsFile:
    stopWords.add(word.strip())
stopWordsFile.close()

for fileName in fileList:
    fileName = fileName.strip()
    currentFile = open(fileName)
    preProcessedText = ''
    for line in currentFile:
        goodwords = []
        words = line.split()
        for i in range(len(words)):
            lowerWord = words[i].lower().strip()
            
            if lowerWord.startswith('http://') or lowerWord.startswith('https://'):
                continue 
            lowerWord = ''.join(ch for ch in lowerWord if ch.isalnum() or ch == '_' or ch == ' ')

            if lowerWord in stopWords:
                continue

            if lowerWord.endswith('ing'):
                lowerWord = lowerWord[0:-3]
            elif lowerWord.endswith('ly'):
                lowerWord = lowerWord[0:-2]
            elif lowerWord.endswith('ment'):
                lowerWord = lowerWord[0:-4]
            goodwords.append(lowerWord)

        string = " ".join(goodwords)
        preProcessedText += string + " "

    f = open('preproc_' + fileName, "w")
    f.write(preProcessedText.strip())
    f.close()
    currentFile.close()

fileList.close()


# Calculating TF-IDF Scores


fileToTF = {}

fileList = open('tfidf_docs.txt')
for fileName in fileList:
    tf = {}
    fileName = 'preproc_' + fileName.strip()
    currentFile = open(fileName)
    counter = 0
    for line in currentFile:
        for word in line.split():
            if word not in tf:
                tf[word] = 0
            tf[word] += 1
            counter += 1
    

    for tempTuple in tf:
        tf[tempTuple] /= counter 

    fileToTF[fileName] = tf
    currentFile.close()

numDocs = len(fileToTF)

for documentName in fileToTF:
    currentTF = fileToTF[documentName]
    for currentWord in currentTF:
        numDocsFoundIn = 0
        for checkDoc in fileToTF:
            if currentWord in fileToTF[checkDoc]:
                numDocsFoundIn += 1
        currentTF[currentWord] *= (math.log(numDocs/numDocsFoundIn, math.e) + 1)

for documentName in fileToTF:
    array = [tuple((n,round(v,2))) for n,v in fileToTF[documentName].items()]
    array = sorted(array, key=lambda item: (-item[1], item[0]),)
    f = open('tfidf_' + documentName[8:], "w")
    f.write(str(array[:5]))
    f.close()

fileList.close()