# Freddy @Blair House, Waterloo, ON, Canada
# Nov 13, 2017

import numpy as np
import pandas as pd
import csv
import time
from datetime import datetime
import sys
import os
from tqdm import *
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.finance import candlestick_ohlc
from data_gen import data_plot
from utils import one_hot


def main():
    #data = get_data(sys.argv[1], sys.argv[2], sys.argv[3])
    #print(data.head())
    data = pd.read_csv(sys.argv[1], parse_dates=True, dayfirst=True)# argv[1]: stock_symbol.txt
    # some preprocessing
    data[['Open','High','Low','Close']] = data[['Open','High','Low','Close']].astype('float32')     
    data["Date"] = data["Date"].apply(mdates.datestr2num)
    data_len = len(data)
    stock_symbol = sys.argv[1].split('/')[-1][:-4] # remove .txt
    counter = 0
    #tqdm
    for _ in tqdm(range(0,int(data_len/13)+1)):
        if(counter + 13 >= data_len): break
        data_cur = data[counter:counter+13]
        data_close = data_cur['Close']
        labels = []
        for i in range(0,13):
            # draw day [0,1,...,9], predict day [10,11,12] 
            # positive label 1, negative label -1
            last_4 = data_close[9:13].values
            labels_raw = last_4[1:4] - last_4[0]
            labels = list(map(one_hot,labels_raw))
        counter = counter + 13
        
        # plot
        fig = data_plot(data_cur[0:10]) # only plot the first 10 days
        #fig.set_size_inches(8,8);
        #fig.show()
        file_name = stock_symbol+'_'+str(counter)+'.png'
        fig.savefig('./data/imgs/' + file_name, dpi=40)
        # save label
        #label_table = pd.read_csv('./data/label_table.csv',header = None, delim_whitespace=False)
        new_data = [[file_name, labels[0],labels[1],labels[2]]]
        df = pd.DataFrame(new_data, columns=['file_name', 'pred_1', 'pred_2', 'pred_3'])
        #label_table.append(df)
        df.to_csv('./data/label_table.csv', mode='a', header=False)
        #label_table.to_csv('./data/label_table.csv')


if __name__ == '__main__':
    main()


