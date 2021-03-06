from __future__ import division

from .shingle import Shingle
from .isimilarity import ISimilarity
from .synonym import Synonym

class RabinKarpParallel(ISimilarity):
	q = 1079
	# d = 26
	s = Shingle()

	def sub_search(self, subpat, txt, s, synonym):
		pattern = subpat.split()
		# print '\npattern'
		print(pattern)

		patlen = len(pattern)
		txtlen = len(txt)

		hashpat = 0
		hashtxt = 0

		# hash for pattern
		for i in range(0, patlen):
			hashpat = (hashpat + hash(pattern[i])) % self.q
			# print pattern[i]
			hashtxt = (hashtxt + hash(txt[i])) % self.q

		# hash for txt
		# print '[%d][%d]' %(x, y-patlen)
		# for i in range(0, patlen):
		# 	hashtxt = (hashtxt + hash(txt[i])) % self.q
						
		# for i in range(x, y - patlen):
		# 	if hashpat == hashtxt:
		# 		for j in range(patlen):
		# 			if txt[i + j] != pattern[j]:
		# 				break
		# 			if j == patlen - 1:
		# 				return 1
		# 	# print 'if %d < %d stop' %(i, (y-patlen))  
		# 	if i < y - patlen:				
		# 		hashtxt = ((hashtxt - hash(txt[i])) + hash(txt[i+patlen])) % self.q
		
		# for i in range(0, txtlen - patlen + 1):
		# 	for j in range(patlen):
		# 		print txt[i+j]

		for i in range(0, txtlen - patlen + 1):
			if hashpat == hashtxt:
				for j in range (patlen):
					if txt[i + j] != pattern[j]:
						break
					if j == patlen - 1:
						return 1
			else: # synonym checker
				for j in range (patlen):
					if txt[i + j] != pattern[j] or not s.is_found(txt[i+j], pattern[j], synonym):
						break
					if j == patlen - 1:
						return 1

			if i < txtlen - patlen:				
				hashtxt = ((hashtxt - hash(txt[i])) + hash(txt[i+patlen])) % self.q		

		return 0

	def full_search(self, x, y, pat, txt):
		# print('TEXT = %s ' %txt)

		found = 0
		pattern = pat
		s = Synonym()

		with open('answerchecker/media/tbipb1.dict', encoding='utf-8') as a_file:
			content = a_file.read()
		synonym = content.splitlines()
		
		for i in range(x, y - 2):
			print ('index[%d] %s ' %(i, pattern[i]))

			if self.sub_search(pattern[i], txt, s, synonym):
				print(pattern[i])
				found += 1
		# print "\n"

		return found

	def sim_measure(self, x, y, pat, txt, R, l,):
		l.acquire()

		# print "%d" %len(txt)
		print("first")

		intersect = 0
		similarity = 0
		
		txtlen = len(self.s.wordshingling(txt))

		intersect = self.full_search(x, y, pat, txt)
		# print intersect

		similarity = 1 - ((txtlen - intersect) / txtlen)
		# print("%f = 1 - ((%d - %d) / %d)" %(similarity, txtlen, intersect, txtlen))
		# print("sim_measure %f" % similarity)

		R.put(similarity)

		l.release()