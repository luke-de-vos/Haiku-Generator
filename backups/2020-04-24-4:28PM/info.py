gramLen=3

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


for key in wd:
	print(key)
