# -*- coding: utf-8 -*-
import csv
import pandas as pd
import math
import numpy as np


df = pd.DataFrame(np.random.randn(100, 2))
print df
msk = np.random.rand(len(df)) < 0.8
print msk
train = df[msk]
test = df[~msk]

print train,test