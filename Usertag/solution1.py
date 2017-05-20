# -*- coding: utf-8 -*-
import math
import operator
import pandas as pd
import numpy as np

def addValueToMat(dict, A, B, cnt):
    if A not in dict:
        dict[A] = dict()
    if B not in dict[A]:
        dict[A][B] = 0
    dict[A][B] += 1

def InitStat(records):
    user_tags = dict()
    tag_items = dict()
    user_items = dict()
    for user, item, tag in records:
        addValueToMat(user_tags, user, tag, 1)
        addValueToMat(tag_items, tag, item, 1)
        addValueToMat(user_items, user, item, 1)

def Recommend(user, user_tags, tag_items, user_items):
    recommend_items = dict()
    #p(u,i) = \sum_b n_{u,b}n_{b,i}
    tagged_items = user_items[user]
    for tag, wut in user_tags[user].items():
        for item, wti in tag_items[tag].items():
            if item in tag_items:
                continue
            recommend_items[item] = recommend_items.get(item, 0) + (wut * wti)
    return recommend_items