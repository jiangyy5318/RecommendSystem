# -*- coding: utf-8 -*-
import csv
import pandas as pd
import math


df  = pd.read_csv('movielen/u.data', sep='\t', names=['user_id', 'movie_id', 'rating', 'unix_timestamp'],
                      encoding='latin-1')
df.drop(['rating', 'unix_timestamp'], axis=1, inplace=True)

def readdatafromdf(df):
    train = dict()
    for index, row in df.iterrows():
        if row[0] not in train:
            train[row[0]] = dict()
        train[row[0]][row[1]] = 1
    return train

train = readdatafromdf(df)

def UserSimilarity(train, type = 'Jaccard'):
    #build reverse table for item_users
    item_users = dict()
    for u,items in train.items():
        for i in items.keys():
            if i not in item_users:
                item_users[i] = set()
            item_users[i].add(u)
    N = dict()
    C = dict()
    for i,users in item_users.items():
        for u in users:
            N[u] = N.get(u,0) + 1
            if u not in C:
                C[u] = dict()
            for v in users:
                if u == v:continue
                if v not in C[u]:
                    C[u][v] = 0
                C[u][v] += 1
    W = dict()
    for u, related_users in C.items():
        for v, cuv in related_users.items():
            W[u][v] = cuv / math.sqrt(N[u]*N[v])
    return W


def UserSimilarityImproved(train):
    #build reverse table for item_users
    item_users = dict()
    for u,items in train.items():
        for i in items.keys():
            if i not in item_users:
                item_users[i] = set()
            item_users[i].add(u)
    N = dict()
    C = dict()
    NI = dict()
    for i,users in item_users.items():
        for u in users:
            N[u] = N.get(u,0) + 1
            if u not in C:
                C[u] = dict()
            for v in users:
                if u == v:continue
                if v not in C[u]:
                    C[u][v] = 0
                C[u][v] += 1/math.log(1+len(users))
    W = dict()
    for u, related_users in C.items():
        for v, cuv in related_users.items():
            W[u][v] = cuv / math.sqrt(N[u]*N[v])
    return W



def Recommend(train, user, W):
    rank = dict()
    interacted_items = train[user]
    #for v, wuv in sorted(W[user].items, reverse=True):
        #for


def Recall(train, test, N):
    hit = 0
    all = 0
    for user in train.keys():
        tu = test[user]
        rank = GetRecommendation(user,N)
        for item, pui in rank:
            if item in tu:
                hit += 1
        all += len(tu)
    return hit / (all * 1.0)


