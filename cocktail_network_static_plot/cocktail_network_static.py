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


# Serve the file over http to allow for cross origin requests
app = flask.Flask(__name__, static_folder="force")

@app.route('/<path:path>')
def static_proxy(path):
  return app.send_static_file(path)
print('\nGo to http://127.0.0.1:8229/index.html \n')
app.run(port=8236)
