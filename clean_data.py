# clean data
import pandas as pd
import numpy as np
import re
try:
   import cPickle as pickle
except:
   import pickle
   
#------------------------------------------------------------#
def clean_data():
    # load data. data is in the form of list of dicts.
    with open('./data/cocktail_data_raw', 'rb') as fp:
        data = pickle.load(fp)
    #------------------------------------------------
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
    
    # data frame
    df = pd.DataFrame(index= range(0, len(data)), columns=basic_info + ingredients)
    for i,d in enumerate(data):
        for diction in d:
            for k,v in diction.iteritems():
                df.loc[i][k] = v
    #save cocktail_df_raw
    with open('./data/cocktail_df_raw', 'wb') as fp:
        pickle.dump(df, fp, protocol=2)

    #------------------------------------------------------------------
    # clean data frame data
    with open('./data/cocktail_df_raw', 'rb') as fp:
        df_raw = pickle.load(fp)

    df = df_raw.copy() # copy the data frame
    column_names = df.columns.values.tolist()

    # convert string values to numbers in dataframe
    for col in range(4, len(column_names)):
        #print column_names[col]
        x = df[column_names[col]]
        #print x[~x.isnull()]
        df[column_names[col]][~x.isnull()] = convert_to_num(x[~x.isnull()].tolist())

    # modify gredient(columns after 14) values; replace extreme values by median
    for col in range(14,len(column_names)):
        x = df[column_names[col]]
        tmp = x[(~x.isnull()) & (x >= 0)] # well defined values
        med = tmp.median(skipna=True) # find median
        # replace ill-defined value by median
        df[column_names[col]][(~x.isnull()) & ((x < 0)|(x > 10*med))] = med

    # rating
    x = df[column_names[1]]
    x[x==''] = np.nan # replace null by np.nan
    df.loc[:, column_names[1]] = [float(s) for s in x] #convert to numeric

    # number of votes
    x = df[column_names[2]]
    x[x=='ote!'] = np.nan
    df.loc[:, column_names[2]] = [float(s) for s in x]

    # nutrition
    for col in range(4, 14):
        x = df[column_names[col]]
        df.loc[(x.isnull()) | (x == -999), column_names[col]] = np.nan

    #----------------------------------------
    # save cleaned data frame
    with open('./data/cocktail_df_cleaned', 'wb') as fp:
        pickle.dump(df, fp, protocol=2)
        

        
#------------------------------------------------------------------#          
# convert fraction string to float
def convert_to_float(frac_str):
    try:
        return float(frac_str)
    except ValueError:
        try:
            num, denom = frac_str.split('/')
        except ValueError:
            return None
        try:
            leading, num = num.split(' ')
        except ValueError:
            return float(num) / float(denom)        
        if float(leading) < 0:
            sign_mult = -1
        else:
            sign_mult = 1
        return float(leading) + sign_mult * (float(num) / float(denom))

#------------------------------------------------------------------#     
# convert string to numerical data for each column of df
def convert_to_num(l):
    num_l = [np.nan]*len(l)
    for i in range(len(l)):
        # get part contains only number
        tmp = [x for x in l[i].split() if re.search('^\d+/?\d*$',x)]
        # convert to numeric and compute sum
        if tmp:
            num_l[i] = sum([convert_to_float(x) for x in tmp])
        else:
            num_l[i] = -999 # for non numerical value
    return num_l
        

#---------------------------------
clean_data()
