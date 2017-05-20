# -*- coding: utf-8 -*-
import csv
import pandas as pd
import math

def PersonalRank(G, alpha, root, max_step):
    rank = dict()
    rank = {x:0 for x in G.key()}
    rank[root] = 1
    for k in range(max_step):
        tmp = {x:0 for x in G.keys()}
        for i, ri in G.items():
            for j, wij in ri.items():
                if j not in tmp:
                    tmp[j] = 0
                tmp[j] += alpha * rank[i] / (1.0 * len(ri))
                if j == root:
                    tmp[j] += 1 - alpha
        rank = tmp
    return rank