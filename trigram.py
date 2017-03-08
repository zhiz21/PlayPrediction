#!/usr/bin/python
# import sys
import StringIO
import math

class trigram(object):

	def __init__(self, f, s, c):
		self.first = f
		self.second = s
		self.total = 1
		self.cur = {c:1}
		'''use dictionary to store third letter and num'''
		self.pr = {c:(float(self.cur[c]+ 0.1) / float( self.total + 0.1*37**3)) }

	def addCh(self, c):
		self.total += 1
		if self.cur.get(c) is None:
			'''if given letter doesnt exist, create a new one'''
			self.cur[c] = 1
		else:
			'''if given letter exist, num add one'''
			self.cur[c] += 1
		self.pr[c] = float(self.cur[c]+ 0.1) / float( self.total + 0.1*37**3)
		'''update probability'''

	def getPr(self, c):
		if self.cur.get(c) is None:
			return float(0.1 / (self.total + 0.1*37**3))
		else:
			return self.pr.get(c)


	def show(self):
		f = open("out.txt", "a")
		s = []
		for (i, c) in self.pr.items():
			s.append("P('%c'|'%c','%c')=%s \n" %(i, self.first, self.second, str(c)))
		
		f.writelines(s)
		f.close()



f = open('nlp.txt')
context = f.read()
context = context.lower()

fmt = 'abcdefghijklmnopqrstuvwxyz0123456789     '
for s in context:
	if s not in fmt:
		context = context.replace(s, '')

trigramList = {}
for i in xrange(2, len(context)):
	temp = context[i-2] + context[i-1]
	'''use i-2 and i-1 letter as index'''
	if trigramList.get(temp) is None :
		trigramList[temp] = trigram(context[i - 2], context[i - 1], context[i])
	else:
		trigramList[temp].addCh(context[i])
for (i, t) in trigramList.items():
	t.show()

input1 = "he somehow made this analogy sound exciting instead of hopeless"
input2 = "no living humans had skeletal features remotely like these"
input3 = "frequent internet and social media users do not have higher stress levels"
input4 = "the sand the two women were sweeping into their dustpans was transferred into plastic bags"

inputList = [input1, input2, input3, input4]

for index, input in enumerate(inputList):
	entropy = 0
	for i in xrange(2, len(input)):
		'''calculate the entropy : entropy = -sum(p(x)*log(p(x)))'''
		temp = input[i-2] + input[i-1]
		pro = trigramList[temp].getPr(input[i])
		entropy -= math.log(pro) * pro
	f = open("CrossEntropy.txt", "a")
	f.writelines("Cross entropy of ("+ str(index+1)+") : " + str(entropy) + "\n")
	f.close()




