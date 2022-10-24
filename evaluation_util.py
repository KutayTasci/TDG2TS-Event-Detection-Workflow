import numpy as np
import pandas as pd
import matplotlib
import datetime

def hour_rounder(t):
    # Rounds to nearest hour by adding a timedelta hour if minute >= 30
    return (t.replace(second=0, microsecond=0, minute=0, hour=t.hour)
               +datetime.timedelta(hours=t.minute//30))

def readFiles(path, granularity="days"):
    f = open(path, "r")
    ls = f.read().split("\n")
    if granularity == "days":
        for i in range(len(ls)):
            ls[i] = datetime.datetime.strptime(ls[i], '%m/%d/%Y') #%m/%d/%Y %H:%M:%S
            #ls[i] = hour_rounder(ls[i])
    elif granularity == "hours":
        for i in range(len(ls)):
            ls[i] = datetime.datetime.strptime(ls[i], '%m/%d/%Y %H:%M:%S') #%m/%d/%Y %H:%M:%S
            ls[i] = hour_rounder(ls[i])
    return ls


def get_top_anomalies(df_temp, ascending=True, top=5):
    print("Anomaly Threshold: ")
    print(df_temp.sort_values("anom_score", ascending=ascending).iloc[top])
    top -= 1
    if ascending:
        df_temp = (df_temp.sort_values("anom_score", ascending=ascending) <= df_temp.sort_values("anom_score", ascending=ascending)
                   .iloc[top]["anom_score"]).sort_index()
    else:
        df_temp = (df_temp.sort_values("anom_score", ascending=ascending) >=
                   df_temp.sort_values("anom_score", ascending=ascending)
                   .iloc[top]["anom_score"]).sort_index()

    df_temp[df_temp == True] = 1
    df_temp[df_temp == False] = 0

    return df_temp

def generate_metadata(df_metadata, time_stamps, ls):
    for i in time_stamps:
        df_metadata.loc[i]["trainval"] = True
        if i in ls:
            df_metadata.loc[i]["anomaly"] = 1
        else:
            df_metadata.loc[i]["anomaly"] = 0
    return df_metadata

def get_precision(pred, labels, delay=0, top=0):
    tp = 0
    fp = 0
    for i in range(len(pred)):
        hit = 0
        if pred.iloc[i]["anom_score"] == 1:
            for j in range(-1*delay, delay+1):
                if labels[min(max(i+j, 0), len(labels)-1)][1][0] == 1:
                    tp += 1
                    hit = 1
                    break
            if hit == 0:
                fp += 1

    return tp / (tp + fp)

def get_recall(pred, labels, delay=0, top=0):
    tp = 0
    fn = 0
    for i in range(len(labels)):
        hit = 0
        if labels[i][1][0] == 1:
            for j in range(-1*delay, delay+1):
                if pred.iloc[min(max(i+j, 0), len(labels)-1)]["anom_score"] == 1:
                    tp +=1
                    hit = 1
                    break
            if hit == 0:
                fn += 1

    return tp / (tp + fn)

def get_accuracy(pred, labels):
    tp = 0
    tn = 0
    for i in range(len(pred)):
        if pred.iloc[i]["anom_score"] == 1:
            if labels[i][1][0] == 1:
                tp += 1
        else:
            if labels[i][1][0] == 0:
                tn += 1
    return (tp + tn) / len(pred)