class Synonym():
	def is_found(self, txt, pat, synonym):
		pattern = pat.split()

		patlen = len(pattern)
		txtlen = len(txt)

		for i in range(0, txtlen - patlen + 1):
			for j in range (patlen):
				if txt[i + j] != pattern[j] or not self.check_synonym(txt[i+j], pattern[j], synonym):
					break
				if j == patlen - 1:
					return 1
		return 0

	def check_synonym(self, subtxt, subpat, synonym):
		for line in synonym:
			if subtxt in synonym and subpat in synonym:
				# print('text')
				# print(subtxt)
				# print('pattern')	
				# print(subpat)
				return True
		
		return False