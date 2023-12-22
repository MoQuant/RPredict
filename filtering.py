import numpy as np
import pandas as pd



dataset = pd.read_csv('Dataset.csv')

del dataset['Unnamed: 0']

cols = dataset.columns.values.tolist()

Y = dataset['Bitcoin'].values
del dataset['Bitcoin']

X = dataset.values.tolist()

X = np.array([[1] + i for i in X])


XTX = X.T.dot(X)
IXTX = np.linalg.inv(XTX)
XTY = X.T.dot(Y)

beta = IXTX.dot(XTY)

m = len(X)
n = len(X[0]) - 1

e = (Y - X.dot(beta))

rss = e.T.dot(e)

factor = rss / (m - n - 1)

A = factor*IXTX

sd = np.sqrt(np.diag(A))

test_stat = beta / sd

cols = ['Intercept'] + cols[:-1]

significant_cols = []
significant_vars = []

test_statistic = 1.96

for i, j in zip(cols[1:], test_stat[1:]):
    if abs(j) >= test_statistic:
        significant_cols.append(i)
        significant_vars.append(dataset[i])

significant_cols.append('Bitcoin')
significant_vars.append(Y)

final_set = np.array(significant_vars).T.tolist()[::-1]

df = pd.DataFrame(final_set, columns=significant_cols)

df.to_csv('NewSet.csv')
    
    




