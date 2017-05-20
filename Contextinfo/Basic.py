import math
def addTodict(dict, key, value):
    dict[key] = value


def RecentPopularity(records, alpha, T):
    ret = dict()
    for u, i, tm in records:
        if tm >= T:
            continue
        addTodict(ret, i, 1 /(1.0 + alpha * (T - tm)))
    return ret

def ItemSimilarity(train, alpha):
    C = dict()
    N = dict()
    for u, items in train.items():
        for i, rui in items.items():
            N[i] += 1
            for j, ruj in items.items():
                if i == j:
                    continue
                C[i][j] += 1 / (1 + alpha * abs(rui - ruj))
    W = dict()
    for i, related_items in C.items():
        for j, cij in related_items.items():
            W[i][j] = cij / math.sqrt(N[i]*N[j])
    return W

def Recommendation(train, user_id, W, K, t0):
    rank = dict()
    ru = train[user_id]
    for i, pi in ru.items():
        for j, wj in sorted(W[i].items(), key=None, reverse=True)[0:K]:
            #if j, tuj  in ru.items():
                continue
        #    rank[j] += pi * wj / (1 + beta * (t0 - tuj))
    return rank


def UserSimilarity(train, alpha):
    item_users = dict()
    for u,items in train.items():
        for i, tui in items.items():
            if i not in items.items():
                item_users[i] = dict()
            item_users[i][u] = tui

    C = dict()
    N = dict()
    for i, users in item_users.items():
        for u, tui in users.items():
            N[u] += 1
            for v, tvi in users.items():
                if u == v:
                    continue
                C[u][v] += 1 /(1 + alpha* (tui - tvi))
    W = dict()
    for u, related_users in C.items():
        for v, cuv in related_users.items():
            W[u][v] = cuv / math.sqrt(N[u] * N[v])
    return W