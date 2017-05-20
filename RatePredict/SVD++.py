

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

def InitSVDPP(train, F):
    P = dict()
    Q = dict()
    bu = dict()
    bi = dict()
    Y = dict()
    mu = 0
    for u, ui_item in train.items():
        bu[u] = 0
        #bi[i] = 0
        if u not in P:
            P[u] = [random.random()/math.sqrt(F) for x in range(F)]
        for i, rui in train[u].items():
            bi[i] = 0
            if i not in Q:
                Q[i] = [random.random()/math.sqrt(F) for x in range(F)]
            if i not in Y:
                Y[i] = [random.random() / math.sqrt(F) for x in range(F)]
    return P,Q,bu,bi,mu,Y

def Predict(u,i,P,Q,F, bu, bi , mu):
    ###modify
    return mu + bu[u] + bi[i] + sum(P[u][f]*Q[i][f] for f in range(F))

def LearningSVDPP(train, F, n, alpha, Lambda):
    P,Q,bu,bi,mu,Y = InitSVDPP(train, F)
    #
    Z = dict()
    for step in range(n):
        for u,u_items in train.items():
            Z[u] = P[u]
            ru = 1/ math.sqrt(1.0/len(u_items))
            for i, rui in u_items.items():
                for f in range(F):
                    Z[u][f] += Y[i][f] * ru
                sum = [0 for i in range(F)]
            for i, rui in u_items.items():
                pui = Predict(u, i, P, Q, F, bu, bi, mu, Y)
                eui = pui
                bu[u] += alpha * (eui - Lambda * bu[u])
                bi[i] += alpha * (eui - Lambda * bi[i])
                for f in range(F):
                    sum[f] += Q[i][f] * eui * ru
                    P[u][f] += alpha * (Q[i][f] * eui - Lambda * P[u][f])
                    Q[i][f] += alpha * ((Z[u][f] + P[u][f]) * eui - Lambda * Q[i][f])

            for i,rui in u_items.items():
                for f in range(F):
                    Y[i][f] += alpha * (sum(f) - Lambda * Y[i][f])
            alpha *= 0.9
    return P,Q,bu,bi,mu

train = readdata('ml-latest-small\\ratings.csv')
P,Q,bu,bi,mu = LearningSVDPP(train, 1, 10, 0.8, 0.001)
print P,Q,bu,bi,mu
