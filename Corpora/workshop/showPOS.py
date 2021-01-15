
import nltk
import sys	
		
wordList=[]	#list of all the words in a haiku
posiList=[]	#list of the positions of each word in the haiku. corresponds to wordList
boo=False
with open(sys.argv[1]) as file:
	for line in file:
		if line=="\n":
			tagList=nltk.pos_tag(wordList)
			for i in range(1, len(posiList)):
				if posiList[i] == 'START':
					print(tagList[i-1],end='')
					print(" ",end='')
					print(tagList[i],end='')
					print()
				
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
				if i==len(line.split())-1:
					posiList.append("END")
				elif i==0:
					posiList.append("START")
				else:
					posiList.append("MID")



