

import random
import math
import csv

def readdata(path):
    csv_reader = csv.reader(open(path))
    train = dict()
    firstline = True
    for row in csv_reader:
        if firstline:
            firstline = False
            continue
        if row[0] not in train:
            train[row[0]] = dict()
        if row[1] not in train[row[0]]:
            train[row[0]][row[1]] = float(row[2])
    return train

train = readdata('ml-latest-small\\ratings.csv')


def GlobalAverage(train):
    sum = 0
    cnt = 0
    for u, item in train.items():
        for i, rui in train[u].items():
            sum += rui
            cnt += 1
    return 1.0 * sum / cnt

def UserAverage(train, user):
    sum = 0
    cnt = 0
    for u, item in train.items():
        if u != user:
            continue
        for i, rui in train[u].items():
            sum += rui
            cnt += 1
    return 1.0 * sum / cnt

def itemAverage(train, item):
    sum = 0
    cnt = 0
    for u, item in train.items():
        for i, rui in train[u].items():
            if i != item:
                continue
            sum += rui
            cnt += 1
    return 1.0 * sum / cnt

def PredictAll(records, user_cluster, item_cluster):
    total = dict()
    count = dict()
    for r in records:
        if r.test != 0:
            continue
        gu = user_cluster.GetGroup(r.user)
        gi = item_cluster.GetGroup(r.item)
        AddToMat(total, gu, gi, r.vote)
        AddToMat(count, gu, gi, 1)

    for r in records:
        gu = user_cluster.GetGroup(r.user)
        gi = item_cluster.GetGroup(r.item)
        average = total[gu][gi] / (1.0 * count[gu][gi] + 1.0)
        r.predict = average

def UserSimilarity(records):
    item_users = dict()
    ave_vote = dict()
    activity = dict()

