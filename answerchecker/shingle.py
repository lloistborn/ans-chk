class Shingle():
	def wordshingling(self, word):
		shingle = []

		for i in range(0, len(word) - 4):
			shingle.append(word[i] + " " + word[i + 1] + " " + word[i + 2] + " " + word[i + 3] + " " + word[i + 4])
		
		return shingle