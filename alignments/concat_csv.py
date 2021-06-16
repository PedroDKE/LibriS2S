# -*- coding: utf-8 -*-
# this file takes all the De EN mapping and concatenates those
import glob
import pandas as pd

folders = glob.glob('*/')
total = 0
dataframes = []
for fol in folders:
    result = glob.glob(fol+'/*.csv')
    for f in result:
        df = pd.read_csv(f, index_col=0)
        df.insert(0, 'book_id', df['book'][0].split('.')[0])
        dataframes.append(df)

all_df = pd.concat(dataframes, ignore_index=True)
all_df.to_csv('all_de_en_alligned.csv',index=False)
