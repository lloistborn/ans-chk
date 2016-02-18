class Shingle():
	def wordshingling(self, word):
		shingle = []

		for i in range(0, len(word) - 2):
			shingle.append(word[i] + " " + word[i + 1] + " " + word[i + 2])
		
		return shingle