class Synonym():
	def is_found(self, subtxt, subpat, synonym):
		for line in synonym:
			if subtxt in synonym and subpat in synonym:
				# print('text')
				# print(subtxt)
				# print('pattern')	
				# print(subpat)
				return True
		
		return False