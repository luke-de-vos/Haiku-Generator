#Markov approach
#improvements:
#curate output to add commas before determiners and pronouns if previous word is not a verb or smth
#get more haiku to train on
#add data with brown corpus topic stuff, a link talks about it in last session bookmarks
#rather than only having final line's final word be appropriate ending, select an entire trigram to link to
#only let lines end with words that ended lines in sources?

import random
import re

gramLen=3
numGrams=10
startIndex=0
startChance=5
chance=25
lineSylls=[5,7,5]
thisLineSylls=0

#syllable count dict
EMPHNOS=['0','1','2']
phDict={}
with open("Corpora/phonetic.txt") as file:
	for line in file:
		sylls=0
		for textGroup in line.split():
			if textGroup[-1] in EMPHNOS:
				sylls+=1
		phDict[line.split()[0]] = sylls

#FUNCTION
#return word without surrounding punctuation
def strip(word):
	x = re.search("[A-Za-z0-9\'\-]+", word)
	if x==None:
		return word
	else:
		return x.group(0)

#convert files to list
wl=[]
with open("Corpora/haiku1.txt") as file:
#with open("Corpora/test.txt") as file:
	for line in file:
		for word in line.split():
			wl.append(word)
with open("Corpora/haiku2.txt") as file:
	for line in file:
		for word in line.split():
			wl.append(word)

#make dict of words with following n-1grams and number of occurrences
wd={} 
for i in range(len(wl)-gramLen+1):
	#skip grams that combine poems
	symFound=0
	ngram=" "
	ngram = ngram.join(wl[i:i+gramLen])
	if '+' in ngram and '=' in ngram:
		continue
	#build wd
	if ngram not in wd:
		wd[ngram] = 1
	else:
		wd[ngram] = wd[ngram]+1

#sort from stack overflow
wd={k: v for k, v in sorted(wd.items(), key=lambda item: item[1], reverse=True)}

#FUNCTION
#
def gramMatch(key, passGram):
	if key.split()[0:-1] == passGram.split()[1:gramLen]:
		return True
	return False

#FUNCTION
#return number of sylls in passed word
def getSylls(string):
	if re.fullmatch("[\.\-]+", string) != None:
		return 0
	totSylls=0
	for word in string.split():
		if strip(word).upper() in phDict:
			totSylls += phDict[strip(word).upper()]
		else:
			return 10000
	return totSylls

#FUNCTION
#checks to see if passed string has few enough syllables
def shortEnough(string, syllsLeft):
	if getSylls(string) <= syllsLeft:
		return True
	return False

#FUNCTION
#passed a gram, returns true if passed gram has a potential next gram
def hasNextGram(passGram, syllsLeft):
	for key in wd:
		if gramMatch(key, passGram):
			for key2 in wd:
				if gramMatch(key2, key):
					return True
	return False

#FUNCTION
#finds gram that begins with '+'
def findFirstGram(syllsLeft):
	for key in wd:
		if key[0]=='+':
			z=random.random()*100
			if z < startChance:
				if shortEnough(key, syllsLeft):
					return key
				#if any slice of the key fits the syllable restriction, return it
				#will handle printing it on two lines later
				for i in range(1, gramLen):
					if getSylls(" ".join(key.split()[0:i]))==syllsLeft:
						return key
	return findFirstGram(syllsLeft)

#FUNCTION
#passed a gram, returns next gram
def getNextGram(passGram, chance, syllsLeft):
	if passGram==None:
		return None
	backupGram=""
	for key in wd:
		if gramMatch(key, passGram):
			#print("2",end='')
			if shortEnough(key.split()[-1], syllsLeft):
				#print("3",end='')
				if hasNextGram(key, syllsLeft):
					#print("4",end='')
					backupGram=key
					if random.random()*100 < chance:
						return key
			elif getSylls(key.split()[-1])==syllsLeft and key[-1]=='=':
				return key
	if len(backupGram)>0:
		return backupGram
	#print("syllsLeft:"+str(syllsLeft))
	#print("SHOULDN'T BE HERE")


#FUNCTION
#finds final line grams
def getFinalGrams(passGram, chance, syllsLeft):
	if syllsLeft < 3:
		for key in wd:
			if gramMatch(key, passGram):
				if getSylls(key.split()[-1]) == syllsLeft and key[-1]=='=':
					return key
	backupGram=""
	if syllsLeft >= 1:
		for key in wd:
			if gramMatch(key, passGram):
				if shortEnough(key.split()[-1], syllsLeft) and hasNextGram(key, syllsLeft):
					backupGram=key
					if random.random()*100 < chance:
						return key
	return backupGram


#POETRY GENERATION
gram = None
overList=[]
#for each line except last line
for i in range(len(lineSylls)-1):
	syllsLeft=lineSylls[i]
	while syllsLeft > 0:
		#flush potential overflow from last line
		for word in overList:
			print(word+" ", end='')
			syllsLeft-=getSylls(word)
		overList.clear()
		#gram getting
		gram = getNextGram(gram, chance, syllsLeft)
		if gram != None:
			print(gram.split()[-1]+" ",end='')
			syllsLeft -= getSylls(gram.split()[-1])	
		else:
			gram = findFirstGram(syllsLeft)
			#gram may have more syllables than line allows
			#note- findFirstGram won't pick a gram with a word that breaks the syllCount
			for gr in gram.split():
				if syllsLeft == 0 and gr!='-':
					overList.append(gr)
				else:
					print(gr+" ",end='')
					syllsLeft -= getSylls(gr)
	print()
#last line
syllsLeft=lineSylls[-1]
while syllsLeft > 0:
	#flush potential overflow from last line
	for word in overList:
		print(word+" ", end='')
		syllsLeft-=getSylls(word)
	overList.clear()
	#get rest of last line
	gram = getFinalGrams(gram, chance, syllsLeft) #error- passed gram is not None, but this func returns None
	print(gram.split()[-1]+" ",end='')
	syllsLeft -= getSylls(gram.split()[-1])
print()









