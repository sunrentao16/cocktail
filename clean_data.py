# clean data
try:
   import cPickle as pickle
except:
   import pickle
# read data
def clean_data():

	with open('./data/cocktail_data_raw', 'rb') as fp:
		data = pickle.load(fp)
	print(len(data))
	print(data[0])
	
	#----------------------
	basic_info = ['name', 'rating', 'vote_count', 'instruction',
			  'calories', 'energy', 'fats', 'carbohydrates', 'protein',
			  'fiber', 'sugars', 'cholesterol', 'sodium', 'alcohol'] 
	
	name_set = set() # initialize a set holding names
	for d in data:
		for diction in d:
			for k in diction:
				name_set.add(k.lower())
	print(len(name_set))
	print(len(name_set - set(basic_info)))

	#print(basic_info)
	
	
	
clean_data()
