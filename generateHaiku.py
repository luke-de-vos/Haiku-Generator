#Luke De Vos
#Haiku Generator


import random
import re

'''
further fit the training set

'''

#return word without surrounding punctuation
def strip(word):
	x = re.search("[A-Za-z0-9\'\- ]+", word)
	if x == None:
		return word
	else:
		return x.group(0)

#get sum of second field in passed list
def getSum(passedL):	#(list of [ngram, count] lists)
	total=0
	for entry in passedL:
		total += entry[1]
	return total

#compose list of all ngrams that could follow the passed gram
def getMatchList(passGram):	#(string)
	global gramL
	newList=[]
	for entry in gramL:
		if passGram.split()[-gramLen+1:] == entry[0].split()[0:-1]:	#[-gramLen+1] so that it handles two-word startGrams correctly
			newList.append(entry)
	return newList

#return number of sylls in passed word
def getSylls(string):
	if re.fullmatch("[\.\-]+", string) != None: #floating hyphens and periods treated as 0 syllable words
		return 0
	totSylls=0
	for word in string.split():
		if strip(word).upper() in phDict:
			totSylls += phDict[strip(word).upper()]
		else:
			return 10000
	return totSylls

#find starting gram
def getFirstGram(syllsLeft, endIdea):
	global startGramD
	global totalStartGrams
	found=False	#set to true when suitable gram is found
	cumu=0.0
	while not found:
		r = random.random()
		for key, value in startGramD.items():
			cumu += value / totalStartGrams
			if r < cumu:
				if key[0][-1] == '~':
					if endIdea:
						if getSylls(key[0]) == syllsLeft:
							found = True
				else:
					if getSylls(key) < syllsLeft:
						found = True
					elif getSylls(key) == syllsLeft and not endIdea:
						found = True
				break
	return key #trim leading '+'

#find subsequent words
#make a screenL, etc
def getNextWord(syllsLeft, outputL, endIdea):
	global gramD

	key = " ".join(outputL[-(gramLen-1):])
	if key[0] == '+':
		key = key[1:]

	if key not in gramD:
		return False

	#screen contents of gramD[key]
	screenL=[]
	for word, value in gramD[key].items():
		if word[-1] == '~':
			if endIdea:
				if getSylls(word) == syllsLeft:
					screenL.append([word, value])
		else:
			if getSylls(word) < syllsLeft:
				screenL.append([word, value])
			elif getSylls(word) == syllsLeft and not endIdea:
				screenL.append([word, value])

	if not screenL:
		return False

	totalGrams=0
	for entry in screenL:
		totalGrams += entry[1]

	chance=0.0
	r=random.random()
	cumu=0
	for entry in screenL:
		cumu += entry[1] / totalGrams
		if r < cumu:
			return entry[0]


#print list of generated haiku words in correct format
def haikuPrint(outputL, lineSylls):
	print('...')
	i=0
	for entry in lineSylls:
		syllsLeft=entry
		while syllsLeft > 0:
			print(outputL[i] + " ", end='')
			syllsLeft -= getSylls(outputL[i])
			i += 1
			if i < len(outputL) and outputL[i] == '-':
				print(outputL[i] + " ", end='')
				i += 1
		print()
	print('...')







'''
MAIN ======================================
'''

filePath="Corpora/fitHaiku.txt"
#filePath="test.txt"
gramLen=3
lineSylls=[5,7,5]
maxSylls=0
phDict={}
wordL=[]
startGramD={} #for ngrams that start ideas
gramD={} #for the rest
totalStartGrams=0

for entry in lineSylls:
	maxSylls += entry

#syllable count dict
EMPHNOS=['0','1','2']

#populate phDict
with open("Corpora/phonetic.txt") as file:
	for line in file:
		sylls=0
		for textGroup in line.split():
			if textGroup[-1] in EMPHNOS:
				sylls += 1
		phDict[line.split()[0]] = sylls

#write each word of training set to list "wordL"
#all lowercase
with open(filePath) as file:
	for line in file:
		for word in line.split():
			wordL.append(word.lower())

#populate gramD and startGramD
for i in range(len(wordL) - gramLen + 1):
	try:
		key=" ".join(wordL[i:i+gramLen-1])
		valWord=wordL[i+gramLen-1]
		if ('+' in key+valWord and '~' in key+valWord):
			if key[0] != '+' or valWord[-1] != '~':
				continue
		if key[0] == '+':
			totalStartGrams += 1
			if key in startGramD:
				startGramD[key] += 1
			else:
				startGramD[key] = 1
			key=key[1:]
		if key in gramD:
			if valWord in gramD[key]:
				gramD[key][valWord] += 1
			else:
				gramD[key][valWord] = 1
		else:
			gramD[key] = {}
			gramD[key][valWord] = 1
		
	except:
		print(key)


wordL.clear() #cleanup



#GENERATION LOOP
print("Hit ENTER to generate a haiku.")
print("Enter any other key to quit.")
while True:
	if input()!='':
		break

	#POETRY GENERATION
	outputL=[]
	deadEndL=[]
	totSylls=0
	nextWord=""
	while totSylls< maxSylls:
		#line 1
		if totSylls < lineSylls[0]:
			if totSylls == 0:
				firstGram = getFirstGram(lineSylls[0], endIdea=True)
				for word in firstGram.split():
					outputL.append(word)
					totSylls += getSylls(word)
			else:
				nextWord = getNextWord(lineSylls[0]-totSylls, outputL, endIdea=True)
				if nextWord != False:
					outputL.append(nextWord)
					totSylls += getSylls(nextWord) 
				
		#line 2
		elif totSylls < lineSylls[0] + lineSylls[1]:
			if totSylls == lineSylls[0]:
				while True:
					nextFirstGram = getFirstGram(lineSylls[1], endIdea=False)
					if nextFirstGram != firstGram: break
				for word in nextFirstGram.split():
					outputL.append(word)
					totSylls+=getSylls(word)
			else:
				nextWord = getNextWord(lineSylls[0]+lineSylls[1]-totSylls, outputL, endIdea=False)
				if nextWord!=False:
					outputL.append(nextWord)
					totSylls+=getSylls(nextWord)
					
		#line 3
		else:	
			nextWord = getNextWord(maxSylls-totSylls, outputL, endIdea=True)
			if nextWord!=False:
				outputL.append(nextWord)
				totSylls+=getSylls(nextWord)

		#dead end loop detection
		if nextWord == False:
			deadEndL.append(outputL.copy())
			for i in range(deadEndL.count(outputL)):
				if outputL:
					totSylls-=getSylls(outputL.pop())
			nextWord=True

		#print in-progress generation, line by line
		#print(outputL)

	#print outputL
	haikuPrint(outputL, lineSylls)









