
import random
import math
import csv

def readdata(path):
    csv_reader = csv.reader(open(path))
    train = list()
    firstline = True
    for row in csv_reader:
        if firstline:
            firstline = False
            continue
        train.append((row[0],row[1],float(row[2])))
    return train

def InitLFM(train, F):
    P = dict()
    Q = dict()
    bu = dict()
    bi = dict()
    mu = 0
    for u,i,rui in train:
        bu[u] = 0
        bi[i] = 0
        if u not in P:
            P[u] = [random.random()/math.sqrt(F) for x in range(F)]
        if i not in Q:
            Q[i] = [random.random()/math.sqrt(F) for x in range(F)]

    return P,Q,bu,bi,mu

def Predict(u,i,P,Q,F, bu, bi , mu):
    return mu + bu[u] + bi[i] + sum(P[u][f]*Q[i][f] for f in range(F))

def LearningLFM(train, F, n, alpha, Lambda):
    P,Q,bu,bi,mu = InitLFM(train, F)
    #
    for step in range(n):
        for u,i, rui in train:
            pui = Predict(u,i,P,Q,F, bu, bi , mu)
            eui = rui - pui
            bu[u] += alpha * (eui - Lambda * bu[u])
            bi[i] += alpha * (eui - Lambda * bi[i])
            for f in range(F):
                P[u][f] += alpha * (Q[i][f] * eui - Lambda * P[u][f])
                Q[i][f] += alpha * (P[u][f] * eui - Lambda * Q[i][f])
            alpha *= 0.9
    return P,Q,bu,bi,mu

train = readdata('ml-latest-small\\ratings.csv')
P,Q,bu,bi,mu = LearningLFM(train, 1, 10, 0.8, 0.001)
print P,Q,bu,bi,mu
