import pandas as pd
import sys
from tqdm import tqdm
import numpy as np
from tdGraphEmbed.tdGraphEmbed.temporal_graph import TemporalGraph
import pickle

def dataset_convert(dataset='enron',granularity = 'months',min_degree_val=10):

    if dataset == "Tw-WorldCup":
        df = pd.read_table(r"Datasets/Twitter_WorldCup/Twitter_WorldCup_2014_resolved.txt", sep=' ', header=None)
        df.columns = ['time', 'source', 'target']
        df['time'] = pd.to_datetime(df['time'], format='%m:%d:%Y:%H:%M:%S')
        df['time'] = df['time'].values.astype(np.int64) // 10 ** 9
        temporal_g = TemporalGraph(data=df, time_granularity=granularity)
        graphs = temporal_g.get_temporal_graphs(min_degree=min_degree_val)

    elif dataset == "Tw-Terror-Security":
        df = pd.read_table(r"Datasets/Twitter_Security/Twitter_May_Aug_2014_TerrorSecurity_resolved.txt", sep=' ', header=None)
        df.columns = ['time', 'source', 'target']
        df['time'] = pd.to_datetime(df['time'], format='%m:%d:%Y:%H:%M:%S')
        df['time'] = df['time'].values.astype(np.int64) // 10 ** 9
        temporal_g = TemporalGraph(data=df, time_granularity=granularity)
        graphs = temporal_g.get_temporal_graphs(min_degree=min_degree_val)
    elif dataset == "gameofthrones":
        with open('Datasets/gameofthrones/gameofthrones_2017_graphs_dynamic.pkl', 'rb') as f:
            graphs = pickle.load(f)

    elif dataset == "formula":
        with open('Datasets/formula/formula_2019_graphs_dynamic.pkl', 'rb') as f:
            graphs = pickle.load(f)





    return graphs
