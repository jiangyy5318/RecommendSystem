
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
       #if row[0] not in train:
       #    train[row[0]] = dict()
       #if row[1] not in train[row[0]]:
       #    train[row[0]][row[1]] = row[2]
    #print train.items()
    return train



def InitLFM(train, F):
    P = dict()
    Q = dict()
    for u,i,rui in train:
        if u not in P:
            P[u] = [random.random()/math.sqrt(F) for x in range(F)]
        if i not in Q:
            Q[i] = [random.random()/math.sqrt(F) for x in range(F)]

    return P,Q

def Predict(u,i,P,Q,F):
    return sum(P[u][f]*Q[i][f] for f in range(F))

def LearningLFM(train, F, n, alpha, Lambda):
    P,Q = InitLFM(train, F)
    for step in range(n):
        for u,i, rui in train:
            pui = Predict(u,i,P,Q,F)
            eui = rui - pui
            for f in range(F):
                P[u][f] += alpha * (Q[i][f] * eui - Lambda * P[u][f])
                Q[i][f] += alpha * (P[u][f] * eui - Lambda * Q[i][f])
            alpha *= 0.9
    return P,Q

train = readdata('ml-latest-small\\ratings.csv')
P,Q = LearningLFM(train, 1, 10, 0.8, 0.001)
print P,Q
