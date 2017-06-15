try:
   import cPickle as pickle
except:
   import pickle
import numpy as np
import pandas as pd

import networkx as nx
from itertools import combinations
import matplotlib.pyplot as plt
import matplotlib as mpl


#from visJS2jupyter import visJS_module
#import visJS2jupyter.visualizations
#import imp
#imp.reload(visJS_module)

import json
from networkx.readwrite import json_graph
import flask


# load data
with open('./data/cocktail_df_cleaned', 'rb') as fp:
    df_raw = pickle.load(fp)
    
# NetWorkX--------------------------
ingredient_names = df_raw.columns.values.tolist()[14:] 
df_ing = df_raw.loc[:, ingredient_names].copy() # ingredient dataframe
G = nx.Graph() # initialize the graph
G.add_nodes_from(ingredient_names) # add nodes
for n in G:
    G.node[n]['name'] = n # add name attr to nodes
# add edges
for r in range(df_ing.shape[0]):
    row = df_ing.loc[r] # current row
    ing_names = row[~row.isnull()].index.tolist() # ingredients in current row
    for c in combinations(range(len(ing_names)),2):
        if G.has_edge(ing_names[c[0]], ing_names[c[1]]):
            G[ing_names[c[0]]][ing_names[c[1]]]['weight'] += 1
        else:
            G.add_edge(ing_names[c[0]], ing_names[c[1]],{'weight':1})
            
            
#----------------------------------------------#

# write json formatted data
d = json_graph.node_link_data(G)
json.dump(d, open('force/force.json', 'w'))
print('Wrote node-link JSON data to force/force.json')

# Serve the file over http to allow for cross origin requests
app = flask.Flask(__name__, static_folder="force")

@app.route('/<path:path>')
def static_proxy(path):
  return app.send_static_file(path)
print('\nGo to http://localhost:8000/force.html to see the example\n')
app.run(port=8125)
