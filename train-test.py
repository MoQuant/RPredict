import pandas as pd


data = pd.read_csv('NewSet.csv')

N = len(data)

Proportion = 0.7

P = int(Proportion*N)

train = data[:P]
test = data[P:]

del train['Unnamed: 0']
del test['Unnamed: 0']

train.to_csv('training_set.csv')
test.to_csv('testing_set.csv')
