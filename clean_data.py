# clean data
import pandas as pd
import numpy as np

try:
   import cPickle as pickle
except:
   import pickle
   

# read data
def clean_data():
	# load data. data is in the form of list of dicts.
	with open('./data/cocktail_data_raw', 'rb') as fp:
		data = pickle.load(fp)
	
	#----------------------
	# convert data to data frame
	basic_info = ['name', 'rating', 'vote_count', 'instruction',
			  'Calories', 'Energy', 'Fats', 'Carbohydrates', 'Protein',
			  'Fiber', 'Sugars', 'Cholesterol', 'Sodium', 'Alcohol'] 
	
	name_set = set() # initialize a set holding names

	for i,d in enumerate(data):
#		tmp_d = d[1]
		for k, v in d[1].iteritems():
			## try to delete the brands '\xae'
#			k_copy = k.encode('utf-8')
#			if k_copy.find('\xae') != -1:
#				k_tmp = k_copy[k_copy.find('\xae')+2:]
#				tmp_d[k_tmp] = tmp_d.pop(k) # change var name in data
#				k = k_tmp
				
			# add gredients name in name_set	 
			name_set.add(k)
				
	ingredients = sorted(list(name_set - set(basic_info)))

	#-----------------------
	# data frame
#	df = pd.DataFrame(index= range(0, len(data)), columns=basic_info + ingredients)
#	for i,d in enumerate(data):
#		for diction in d:
#			for k,v in diction.iteritems():
#				df.loc[i][k] = v

#	with open('./data/cocktail_df_raw', 'wb') as fp:
#		pickle.dump(df, fp, protocol=2)
	
	#-------------------------------
	# clean data frame data
	with open('./data/cocktail_df_raw', 'rb') as fp:
		df_raw = pickle.load(fp)
	print df_raw.loc[120]
	
	

#---------------------------------
clean_data()
