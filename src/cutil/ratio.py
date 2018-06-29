
def get_score_opm(ratio):
	score = 0
	if ratio > 20 :
		# excellent
		score = 4
	elif ratio > 15 and ratio <= 20:
		# good
		score = 3
	elif ratio > 10 and ratio <= 15:
		# average
		score = 2
	elif ratio > 5 and ratio <= 10:
		# good 
		score = 1
	elif ratio < 5:
		# very poor
		score = 0 
	return score

def get_score_dp(ratio):
	score = 0
	if ratio > 20 :
		# excellent
		score = 4
	elif ratio > 15 and ratio <= 20:
		# good
		score = 3
	elif ratio > 10 and ratio <= 15:
		# average
		score = 2
	elif ratio > 5 and ratio <= 10:
		# good 
		score = 1
	elif ratio < 5:
		# very poor
		score = 0 
	return score

def get_score_pe(ratio):
	if ratio <= 12:
		# excellent : under-valued : steal 
		score = 4
	elif ratio > 12 and ratio <= 15:
		# good :   looks ok
		score = 3
	elif ratio > 15 and ratio <= 20:
		# average
		score = 2
	elif ratio > 20 and ratio <= 25:
		# poor : slightly over-valued 
		score = 1
	elif ratio > 25:
		# very poor : over-valued
		score = 0 
	return score

def get_score_ic(ratio):
	if ratio >= 3:
		score = 3
	elif ratio >= 2:
		score = 2
	elif ratio >= 1:
		score = 1
	elif ratio < 1:
		score = 0 
	return score

def get_score_peg(ratio):
	if ratio <= 1:
		# less than fair price
		score = 1
	elif ratio > 1:
		# expansive
		score = 0 
	return score

