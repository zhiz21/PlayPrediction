import os
import math

LAMBDA = 0.1

'''---------------------- q1 ----------------------'''
class appearWord(object):

	def __init__(self,w,article):
		self.word = w
		self.article = [article]
		self.totalNum = 1

	def findOne(self, article):
		self.totalNum += 1
		if article not in self.article:
			self.article.append(article)


def getWords(articles, path, articleList):

	for article in articles:

		f = open(path + '/' + article)
		iter_f = iter(f)
		for line in iter_f:
			line = line.lower()
			lst = line.split(' ')
			for word in lst:
				if word == "\n" or word == '' or word == '\t':
					continue
				''' delete symbols from words'''
				word = word.replace('\n', '')
				word = word.replace('\t', '')
				word = word.replace('.', '')
				word = word.replace(':', '')
				word = word.replace(',', '')
				word = word.replace('!', '')
				word = word.replace(';', '')
				word = word.replace('?', '')

				if articleList.get(word) is None:
					articleList[word] = appearWord(word, article)
				else:
					articleList[word].findOne(article)


comediesPath = "shakespeare/comedies"
tragediesPath = "shakespeare/tragedies"
comedies = os.listdir(comediesPath)
tragedies = os.listdir(tragediesPath)
comedyList = []
alphabet = ['abcdefghijklmnopqrstuvwxyz']
comedyWordList = {}
tragedyWordList = {}

getWords(comedies, comediesPath, comedyWordList)    #Record words appear in comedies and tragedies.
getWords(tragedies, tragediesPath, tragedyWordList)


f = open("comedyVocabulary.txt", "a")
s = ''
f.writelines("Vocabulary for Comedies: \n")
for w, word in comedyWordList.items():
	'''delete word appears less than 5 times and less than 2 articles'''
	if len(word.article) > 1 and word.totalNum >= 5:
		s += (str(word.word) + ' '*(9 - len(word.word)) + ' ')
f.writelines(s)
f.close()

f = open("tragedyVocabulary.txt", "a")
s = ''
f.writelines("Vocabulary for Tragedies: \n")
for w, word in tragedyWordList.items():
	'''delete word appears less than 5 times and less than 2 articles'''
	if len(word.article) > 1 and word.totalNum >= 5:
		s += (str(word.word) + ' '*(9 - len(word.word)) + ' ')
f.writelines(s)
f.close()


'''--------------------------Q2-------------------------------'''
'''
P(R) = 0.5 | 0.5
P(R|w[1], w[2], w[3]..., w[n]) = P(w[1], w[2], w[3],..., w[n]|R) * P(R) / P(w[1], w[2], w[3],..., w[n])
log(P(w[1], w[2], w[3],..., w[n]|R)) = log(P(w[1]|R)) + log(P(w[2]|R)) + ... + log(P(w[n]|R))
log(P(w[1], w[2], w[3],..., w[n])) = log(P(w[1])) + log(P(w[2])) + ... + log(P(w[n]))
P(w[n]|R) = (c(w[n], R) + lambda) / (c(R) + lambda * V) ////     c(R) = total num of words, V = len(wordList)
P(w[n]) = (c(w[n]) + lambda) / (N + lambda * d)
'''

class Classifier(object):

	def __init__(self):
		self.word = {}
		self.total = 0


	def addWord(self, word):
		if self.word.get(word) is None:
			self.word[word] = 1
		else:
			self.word[word] += 1
		self.total += 1


	def getNum(self, word):
		return self.word[word]


	def getTotal(self):
		return self.total


	def train(self, articleList,articleType):
		for article in articleList:
			f = open(articleType + '/' + article)
			iter_f = iter(f)
			for line in iter_f:
				line = line.lower()
				lst = line.split(' ')
				for word in lst:
					if word == "\n" or word == '' or word == '\t':
						continue
					''' delete symbols from words'''
					word = word.replace('\n', '')
					word = word.replace('\t', '')
					word = word.replace('.', '')
					word = word.replace(':', '')
					word = word.replace(',', '')
					word = word.replace('!', '')
					word = word.replace(';', '')
					word = word.replace('?', '')
					self.addWord(word)


	def getPr(self,word):
		if self.word.get(word) is None:
			return (LAMBDA / (self.total + LAMBDA * len(self.word)))
		else:
			return (self.word[word] + LAMBDA)/(self.total + LAMBDA * len(self.word))


	def getPrDict(self):
		prDict = {}
		for word, n in self.word.items():
			prDict[word] = self.getPr(word)
		return prDict

	def getTotalPr(self, wordLst):
		totalPr = 0
		for word in wordLst:
			totalPr += math.log(self.getPr(word))

		return totalPr


rootPath = "shakespeare/all"
allArticleList = os.listdir(rootPath)
testResult = ""
'''-------------------------- train for all plays except one play ----------------------------'''
correctness = 0


s = ''
'''below value to get the tragedy most like comedy and comedy most like tragedy'''
minRatio = float('Inf')
minPlay = ''
maxRatio = float('-Inf')
maxPlay = ''

'''choose every play as test data'''
for i, testPlay in enumerate(allArticleList):

	trainingPlays = []
	comedyPlays = []
	tragedyPlays = []

	'''remove test play from training set'''
	for play in allArticleList:
		if play != testPlay and play != ".DS_Store":
			trainingPlays.append(play)
	for play in comedies:
		if play != testPlay and play != ".DS_Store":
			comedyPlays.append(play)
	for play in tragedies:
		if play != testPlay and play != ".DS_Store":
			tragedyPlays.append(play)


	#--------train for all plays--------
	allClassifier = Classifier()
	allClassifier.train(trainingPlays, rootPath)
	#--------train for all comedies--------''''''
	comedyClassifier = Classifier()
	comedyClassifier.train(comedyPlays, comediesPath)
	#--------train for all tragedies--------''''''
	tragedyClassifier = Classifier()
	tragedyClassifier.train(tragedyPlays, tragediesPath)




	'''--------testing part--------'''
	testWords = []
	totalNumOfTestWords = 0
	comedyPr = 0
	tragedyPr = 0
	'''--------------- read test play -----------------'''
	f = open('shakespeare/all/' + testPlay)
	iter_f = iter(f)
	for line in iter_f:
		line = line.lower()
		lst = line.split(' ')
		for word in lst:
			if word == "\n" or word == '' or word == '\t':
				continue
			'''delete symbols from words'''
			word = word.replace('\n', '')
			word = word.replace('\t', '')
			word = word.replace('.', '')
			word = word.replace(':', '')
			word = word.replace(',', '')
			word = word.replace('!', '')
			word = word.replace(';', '')
			word = word.replace('?', '')

			testWords.append(word)
			totalNumOfTestWords += 1

	allPr = allClassifier.getTotalPr(testWords)


	c = comedyClassifier.getTotalPr(testWords) - allPr
	t = tragedyClassifier.getTotalPr(testWords) - allPr
	likelihood = str(c - t)
	if c > t:
		ty = "comedy"

	else:
		ty = "tragedy"



	if testPlay in comedies:
		if minRatio > (c-t):
			minRatio = c - t
			minPlay = testPlay
		if ty == "comedy":
			result = "True"
			correctness += 1
		else:
			result = "False"

		s += "(" + str(i) + ") " + testPlay + (10 - len(testPlay))*" " +  "\t comedy \t\t" + ty +"\t\t"+ likelihood + "\n"
	else:
		if maxRatio < (c-t):
			maxRatio =  c - t
			maxPlay = testPlay
		if ty == "comedy":
			result = "False"
		else:
			result = "True"
			correctness += 1

		s += "(" + str(i) + ") " + testPlay + (10 - len(testPlay))*" " + "\t tragedy \t\t" + ty +"\t\t"+ likelihood + "\n"



f = open("prediction.txt", "a")
f.writelines("     NAME \t TRUE GENRE \t PREDICTED GENRE \t LOG RATIO \n")
f.writelines(s)
f.writelines("Correctness : " + str(correctness) + "/22 \n")
f.writelines("Comedy most like tragedy: " + minPlay +"\n")
f.writelines("Tragedy most like comedy: " + maxPlay + "\n")
print "Correctness : " + str(correctness) + "/22"
f.close()

'''----------------------- q3 ----------------------'''

fullComedyClassifier = Classifier()
fullComedyClassifier.train(comedies,comediesPath)
fullTragedyClassifier = Classifier()
fullTragedyClassifier.train(tragedies, tragediesPath)
wordRatio = {}
for word in fullComedyClassifier.word:
	if fullTragedyClassifier.word.get(word) is None:
		continue
	else:
		wordRatio[word] = math.log(fullComedyClassifier.getPr(word)/fullTragedyClassifier.getPr(word))

print wordRatio
wordRatio = sorted(wordRatio.items(), key = lambda x : x[1])
'''get the first 20 elements in the sorted list'''
mostTragicList = wordRatio[:20]

'''get the last 20 elements in the sorted list'''
mostComicList = wordRatio[len(wordRatio) - 20:]
'''reverse the list'''
mostComicList = mostComicList[::-1]


'''file output'''
f = open("comicWordList.txt", "a")
for word, ratio in enumerate(mostComicList):
	f.writelines(str(ratio) + "  " + str(word) + "\t \n" )
f.close()

f = open("tragicWordList.txt", "a")
for word, ratio in enumerate(mostTragicList):
	f.writelines(str(ratio) + "  " + str(word) + "\t \n" )



