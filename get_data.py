# get data using python3
# ge html from website
from bs4 import BeautifulSoup as BS
import urllib.request  as urllib2 
import re # regular expression



#-------------------------------------------
# get all recipes links on one pages
def get_links(url, key_words):

	html = urllib2.urlopen(url)
	soup = BS(html, "html5lib")
	tags_a = soup.findAll('a')
	ret = [None]*len(tags_a)

	for index, link in enumerate(tags_a):
		if re.search(key_words,link.get('href')):
			ret[index] = link.get('href')
	
	ret = list(set(ret)) # unique
	ret = [x for x in ret if x is not None] # delete None
	for l in ret:
		print(l)
	return ret

#
#url = 'https://www.bigoven.com/recipes/cocktail/best'
#key_words = 'www.bigoven.com/recipe/'

#url = 'http://www.drinksmixer.com/'
#get_links(url, key_words)

#-----------------------------------------------
# get recipe given a url
def get_recipe(url):
	
	html = urllib2.urlopen(url)
	soup = BS(html, "html5lib")
	
	# initialize the recipe dict
	recipe = dict(
	name = soup.findAll(class_ = 'recipe_title')[0].text, 
	instruction = soup.findAll(class_ = 'instructions')[0].text
	)
	
	# ingredient	
	ingredient = soup.findAll(class_ = 'name')
	# amount
	amount = soup.findAll(class_ = 'amount')
	for index, ing in enumerate(ingredient):
		recipe[ing.text] = amount[index].text
	
	# slice rating text to rating & vote count
	rating_vote = soup.findAll(class_ = 'rating')[0].text.split()[0] 
	recipe['rating'] = rating_vote[6:9]
	recipe['vote_count'] = rating_vote.split('.')[-1][1:]
	#print(rating_vote, '\n')
	
	# nutrition
	nutrition = soup.findAll(class_ = 'l1a')[2:] # get table
	nutri_dict = {} # initialize
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
	
	for key, v in nutri_dict.items():
		print(key, ':', v)
	#print(cl2)
	for key, v in recipe.items():
		print(key, ':', v)
		
	return(recipe, nutri_dict)
	
#	
#url = 'http://www.drinksmixer.com/'
#url = 'http://www.drinksmixer.com/drink5056.html'
#url = 'http://www.drinksmixer.com/drink2961.html'
#url = 'http://www.drinksmixer.com/drink3954.html'
#get_recipe(url)







