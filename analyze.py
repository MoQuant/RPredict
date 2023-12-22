import numpy as np
import pandas as pd







def Align(dC, dS, dY):
    def FCrypto(x):
        a = x.split(' ')[0].split('-')
        return f'{a[-1]}-{a[0]}-{a[1]}'
    def FYields(x):
        a = x.split('/')
        return f'{a[-1]}-{a[0]}-{a[1]}'
    dC = list(map(FCrypto, dC))
    dY = list(map(FYields, dY))
    hold = []
    for i, j in enumerate(dY):
        if j in dS:
            ix = dS.index(j)
            hold.append([i, ix])
    gold = []
    for (a, b) in hold:
        if dY[a] in dC:
            ix = dC.index(dY[a])
            gold.append([a, b, ix])
    return gold
        

def BuildSet(align, btc, yds, stks):
    tickers = ['GLD','JPM','NVDA','SPY','VXX']
    del btc['Time']
    del yds['Date']
    for s in range(len(stks)):
        del stks[s]['date']
    BTC = btc['Close'].values.tolist()
    YDS = (yds.values/100).tolist()
    STK = np.array([s['adjClose'].values.tolist() for s in stks]).T.tolist()
    dataset = []
    for (a, b, c) in align:
        dataset.append(YDS[a] + STK[b] + [BTC[c]])
    cols = ['Y' + i.replace(' ','') for i in yds.columns]
    columns = cols + tickers + ['Bitcoin']
    
    df = pd.DataFrame(dataset, columns=columns)
    return df


# Import and clean datasets
bitcoin = pd.read_csv('BTC-USD.csv')
yields = pd.read_csv('daily-treasury-rates.csv')
tickers = ['GC=F','JPM','NVDA','SPY','VXX']
stocks = [pd.read_csv(f'{tick}.csv') for tick in tickers]

del bitcoin['Unnamed: 0']
for s in range(len(stocks)):
    del stocks[s]['Unnamed: 0']

sn = np.min([len(i) for i in stocks])
stocks = [c[:sn] for c in stocks]

dateCrypto = bitcoin['Time'].values.tolist()
dateStock = stocks[0]['date'].values.tolist()
dateYield = yields['Date'].values.tolist()


alignment = Align(dateCrypto, dateStock, dateYield)
df = BuildSet(alignment, bitcoin, yields, stocks)
df.to_csv('Dataset.csv')

