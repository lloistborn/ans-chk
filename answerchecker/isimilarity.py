class ISimilarity:
	# for serial algorithm
	def sim_measure(self, txt, pat):
		raise NotImplementedError()

	# for parallel algorithm
	def sim_measure(self, index_start, index_end, pat, txt, R,):
		raise NotImplementedError()