# get data using python3
# ge html from website
from bs4 import BeautifulSoup as BS
import urllib.request  as urllib2 
import re # regular expression
import pickle # write & read data


#-------------------------------------------
# get all recipes links on one pages
def get_links(url, key_words = None):
	
	html = urllib2.urlopen(url)
	soup = BS(html, "html5lib")
	tags_a = soup.findAll('a')
	ret = [None]*len(tags_a)
	
	if key_words == None:
		key_words = '/drink'
	
	for index, link in enumerate(tags_a):
		if re.search(key_words,link.get('href')):
			ret[index] = 'http://www.drinksmixer.com' + link.get('href')
	
	ret = list(set(ret)) # unique
	ret = [x for x in ret if x is not None] # delete None
	for l in ret:
		print(l)
	return ret


#url = 'http://www.drinksmixer.com/cat/1/'
#key_words = '/drink'
#get_links(url, key_words)

#-----------------------------------------------
# get recipe given a url
def get_recipe(url):
	
	html = urllib2.urlopen(url)
	soup = BS(html, "html5lib")
	
	# initialize the recipe dict
	basic = dict(
	name = soup.findAll(class_ = 'recipe_title')[0].text, 
	instruction = soup.findAll(class_ = 'instructions')[0].text
	)
	
	# slice rating text to rating & vote count
	rating_vote = soup.findAll(class_ = 'rating')[0].text.split()[0] 
	basic['rating'] = rating_vote[6:9]
	basic['vote_count'] = rating_vote.split('.')[-1][1:]
	#print(rating_vote, '\n')	
	
	recipe = dict()
	# ingredient	
	ingredient = soup.findAll(class_ = 'name')
	# amount
	amount = soup.findAll(class_ = 'amount')
	for index, ing in enumerate(ingredient):
		recipe[ing.text] = amount[index].text
	
	# nutrition
	nutrition = soup.findAll(class_ = 'l1a')[2:] # get table
	nutri_dict = {} # initialize
	if nutrition: # some page may NOT have nutrition table
	
		## column 1
		cl1 = [x for x in nutrition[0].text.split() if '(' not in x]
		print(cl1)
	
		## column 2
		cl2_raw =  [None]*4# 2nd row is missing
		for index, x in enumerate(nutrition[1].findAll('span')):
			cl2_raw[index]= x.text
		### find 2nd row
		tmp_str = nutrition[1].text
		row_2 = tmp_str[len(cl2_raw[0]):tmp_str.find(cl2_raw[1])]
		cl2_raw.insert(1,row_2)
	
		## column 3
		cl3 = nutrition[2].text.split()
		print(cl3)
	
		## column 4
		cl4_raw =  [None]*4# 5nd row is missing
		for index, x in enumerate(nutrition[3].findAll('span')):
			cl4_raw[index]= x.text
		### find 5nd row
		tmp_str = nutrition[3].text.strip()
		row_5 = tmp_str[tmp_str.find(cl4_raw[3])+len(cl4_raw[3]):]
		cl4_raw.append(row_5)
	
		for index, x in enumerate(cl1):
			nutri_dict[x] = cl2_raw[index]
		for index, x in enumerate(cl3):
			nutri_dict[x] = cl4_raw[index]
	
#		for key, v in nutri_dict.items():
#			print(key, ':', v)

#	
#	for k, v in basic.items():
#		print(k, ':', v)
#	
#	for key, v in recipe.items():
#		print(key, ':', v)
	
	print([basic, recipe, nutri_dict])
	return([basic, recipe, nutri_dict])
	
#	
#url = 'http://www.drinksmixer.com/'
#url = 'http://www.drinksmixer.com/drink5056.html'
#url = 'http://www.drinksmixer.com/drink2961.html'
#url = 'http://www.drinksmixer.com/drink3954.html'
#url = 'http://www.drinksmixer.com/drink10001.html'
#get_recipe(url)

def save_data(url):
	
	urls = get_links(url)
	data = [None] * len(urls)
	for i, u in enumerate(urls):
		data[i] = get_recipe(u)
	# write data by pickle
	with open('./data/cocktail_data', 'wb') as fp:
		pickle.dump(data, fp)

url = 'http://www.drinksmixer.com/cat/1/'
save_data(url)


