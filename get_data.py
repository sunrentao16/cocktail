# get data using python3
# ge html from website
from bs4 import BeautifulSoup as BS
import urllib.request  as urllib2 
import re # regular expression

# website = 'http://www.drinksmixer.com/'

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
	ret = [x for x in ret if x is not None]
	for l in ret:
		print(l)
	return ret

#
#url = 'https://www.bigoven.com/recipes/cocktail/best'
#key_words = 'www.bigoven.com/recipe/'
#get_links(url, key_words)

#-----------------------------------------------
# get recipe given a url
def get_recipe(url):
	
	html = urllib2.urlopen(url)
	soup = BS(html, "html5lib")
	
	# initialize the recipe dict
	recipe = dict(
	# name
	name = soup.findAll(class_ = 'fn')[0].text, 
	# review number
	review_count = soup.findAll(class_ = 'count')[0].text, 
	# rating
	rating = soup.findAll(class_ = 'recipe-detail-star-rating')[0].text, 
	# duration
	duration = soup.findAll(class_ = 'duration')[0].text 
	)
	
	# ingredient	
	ingredient = soup.findAll(class_ = 'name')
	# amount
	amount = soup.findAll(class_ = 'amount')
	
	
	for index, ing in enumerate(ingredient):
		recipe[ing.text] = amount[index].text
	#print(name)
	for key, v in recipe.items():
		print(key, ':', v)
		

url = 'https://www.bigoven.com/recipe/pomegranate-key-lime-vodka-cocktails/641724'
url = 'https://www.bigoven.com/recipe/the-old-fashioned-cocktail/124600'
get_recipe(url)
