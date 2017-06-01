# clean data
import pickle

# read data
def clean_data():

	with open('./data/cocktail_data_124', 'rb') as fp:
		data = pickle.load(fp)
	
	with open('./data/cocktail_data_raw', 'rb') as fp:
		data_2 = pickle.load(fp)
	
	
	print(len(data))
	print(len(data_2))
	
clean_data()
