import re
from collections import Counter

f = 'tfidf_docs.txt'
fileList = open(f)

stopWordsFile = open('stopwords.txt')

stopWords = set()
for word in stopWordsFile:
    stopWords.add(word.strip())

#print(stopWords)

for fileName in fileList:
    fileName = fileName.strip()
    currentFile = open(fileName)
    preProcessedText = ''
    for line in currentFile:
        goodwords = []
        words = line.split()
        for i in range(len(words)):
            lowerWord = words[i].lower().strip()
            
            #print(lowerWord)
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
            #print('appended')
            goodwords.append(lowerWord)

        string = " ".join(goodwords)
        preProcessedText += string + " "

    #print(preProcessedText)
    f = open('preproc_' + fileName, "w")
    f.write(preProcessedText.strip())
    f.close()



