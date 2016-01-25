from __future__ import division

from .shingle import Shingle
from .isimilarity import ISimilarity

class RabinKarpParallel(ISimilarity):
	q = 1079
	# d = 26
	s = Shingle()

	def sub_search(self, x, y, subpat, txt):
		pattern = subpat.split()
		# print '\npattern'
		# print pattern

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

			if i < txtlen - patlen:				
				hashtxt = ((hashtxt - hash(txt[i])) + hash(txt[i+patlen])) % self.q		

		return 0

	def full_search(self, x, y, pat, txt):
		# print 'TEXT = %s ' %txt

		found = 0
		pattern = pat
		
		for i in range(x, y - 4):
			# print 'index[%d] %s ' %(i, pattern[i])

			if self.sub_search(x, y, pattern[i], txt):
				found += 1

		# print "\n"

		return found

	def sim_measure(self, x, y, pat, txt, R,):
		# l.acquire()

		# print "%d" %len(txt)

		intersect = 0
		similarity = 0
		
		txtlen = len(self.s.wordshingling(txt))

		intersect = self.full_search(x, y, pat, txt)
		# print intersect

		similarity = 1 - ((txtlen - intersect) / txtlen)
		# print similarity

		R.put(similarity)

		# l.release()