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
	nutrition = soup.findAll(class_ = 'l1a')[2:]
	print(len(nutrition))
	print(nutrition,'\n')
	#print(name)
	for key, v in recipe.items():
		print(key, ':', v)

#url = 'https://www.bigoven.com/recipe/pomegranate-key-lime-vodka-cocktails/641724'
#url = 'https://www.bigoven.com/recipe/the-old-fashioned-cocktail/124600'

url = 'http://www.drinksmixer.com/'
url = 'http://www.drinksmixer.com/drink5056.html'
url = 'http://www.drinksmixer.com/drink2961.html'
url = 'http://www.drinksmixer.com/drink3954.html'
get_recipe(url)







