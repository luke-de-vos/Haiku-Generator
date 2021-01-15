#POS and sentence position based haiku marking
#pass file to be fit as command line argument
#meant to be run on poetry already with markings for beginnings/ends of haiku

import nltk
import sys


NOUNS = ['NN','NNS','NNP','NNPS']
ADJ = ['JJ','JJR','JJS']
PRP = ['PRP','PRP$']
DT = ['DT']


def showPOS(i):
	print(tagList[i-1],end='')
	print(" ",end='')
	print(tagList[i],end='')
	print()

def fix(i):
	global wordList
	if '~' not in wordList[i-1]:
		wordList[i-1] = wordList[i-1] + '~'
	if '+' not in wordList[i]:
		wordList[i] = '+' + wordList[i]

#if passed parts of speech suggest an idea split
#where the magic happens
def isPattern(pos1, pos2):
	if pos1 in NOUNS or pos1 in ADJ:
		if pos2 in DT or pos2 in PRP:
			return True
		if pos2 in NOUNS or pos2 in ADJ:
			return True
			
wordList=[]	#list of all the words in a haiku
posiList=[]	#list of the positions of each word in the haiku. corresponds to wordList

with open(sys.argv[1]) as file:
	for line in file:
		if line=="\n":
			tagList=nltk.pos_tag(wordList)
			for i in range(1, len(posiList)):
				if posiList[i] == 'START':
					if isPattern(tagList[i-1][1], tagList[i][1]):
						#showPOS(i)
						fix(i)
			#output
			for i in range(len(wordList)):
				if posiList[i]!=('END'):
					print(wordList[i]+" ",end='')
				else:
					print(wordList[i])
			print()
			#cleanup
			wordList.clear()
			posiList.clear()

		else:
			for i in range(len(line.split())):
				wordList.append(line.split()[i])
				if i == len(line.split())-1:
					posiList.append("END")
				elif i==0:
					posiList.append("START")
				else:
					posiList.append("MID")



