# -*- coding: utf-8 -*-
import math
import operator
import pandas as pd
import numpy as np



def readdatafromdf(df):
    train = dict()
    for index, row in df.iterrows():
        if row[0] not in train:
            train[row[0]] = dict()
        train[row[0]][row[1]] = 1
    return train

def ItemSimilarity(train):
    #calc co-rated users between items
    C = dict()
    N = dict()
    for u, items in train.items():
        for i in items:
            N[i] = N.get(i,0) + 1
            for j in items:
                if i == j:continue
                if i not in C:
                    C[i] = dict()
                if j not in C[i]:
                    C[i][j] = 1
                C[i][j] += 1
    W = dict()
    for i, related_items in C.items():
        for j,cij in related_items.items():
            if i not in W:
                W[i] = dict()
            W[i][j] = cij / math.sqrt(N[i] * N[j])
    return W

def ItemSimilarityImproved(train):
    #calc co-rated users between items
    C = dict()
    N = dict()
    for u, items in train.items():
        for i in items:
            N[i] = N.get(i,0) + 1
            for j in items:
                if i == j:continue
                if i not in C:
                    C[i] = dict()
                if j not in C[i]:
                    C[i][j] = 1
                C[i][j] += 1 / math.log(1 + len(items) * 1.0)
    W = dict()
    for i, related_items in C.items():
        for j,cij in related_items.items():
            if i not in W:
                W[i] = dict()
            W[i][j] = cij / math.sqrt(N[i] * N[j])
    return W


def Recommendation(train, user_id, W, K):
    rank = dict()
    ru = train[user_id]
    for i,pi in ru.items():
        for j, wj in sorted(W[i].items(), key=operator.itemgetter(1), reverse=True)[0:K]:
            if j in ru:
                continue
            rank[j] = rank.get(j,0) + pi * wj
    return rank


if __name__=="__main__":
    df = pd.read_csv('movielen/u.data', sep='\t', names=['user_id', 'movie_id', 'rating', 'unix_timestamp'],
                     encoding='latin-1')
    df.drop(['rating', 'unix_timestamp'], axis=1, inplace=True)
    msk = np.random.rand(len(df)) < 0.9
    train = readdatafromdf(df[msk])
    test = readdatafromdf(df[~msk])
    W = ItemSimilarity(train)
    rank = Recommendation(train, 1, W, 5)
    print rank