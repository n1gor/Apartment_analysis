import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from statsmodels.formula.api import ols
import seaborn as sns
import pylab

df = pd.read_csv('apartments_cian.csv')
df = df * ([1] * 21 + [10])
# df = df.fillna(0)
# df = df.drop('living_space', 1)
# df = df.drop('rooms', 1)
# df = df.drop('emergency_exit', 1)
# m = ols('price ~ square',df).fit()
# infl = m.get_influence()
# sm_fr = infl.summary_frame()
# a = sm_fr['dffits']<0.2841371938943025
# a = a.reindex(range(1090))
# a = a.fillna(True)
# df = df.iloc[:-115]
# df = df[a]
colns_c = 3
fig, axes = plt.subplots(nrows=2, ncols=colns_c, figsize=(20, 10))
features = ['rooms',
            'square',
            'living_space',
            'kitchen_scace',
            'build_year']
        # 'curr_floor']
        # 'max_floor',
        # 'home_type',
        # 'build_year',
        # 'district',
        # 'repair_type']
# for idx, feat in  enumerate(features):
#     sns.scatterplot(x='price', y=feat, data=df, ax=axes[idx // colns_c, idx % colns_c])
#     axes[idx // colns_c, idx % colns_c].legend()
#     axes[idx // colns_c, idx % colns_c].set_xlabel('price')
#     axes[idx // colns_c, idx % colns_c].set_ylabel(feat)
# df = df.drop('square', 1)
# df = df.drop('rooms', 1)
df_dm = pd.get_dummies(df, drop_first=True)
corr = df_dm.corr()
fig, ax = plt.subplots()
ax.matshow(corr, cmap='seismic')

for (i, j), z in np.ndenumerate(corr):
    ax.text(j, i, '{:0.1f}'.format(z), ha='center', va='center')

plt.xticks(range(len(corr.columns)), corr.columns, rotation = 90)
plt.yticks(range(len(corr.columns)), corr.columns)
plt.show()

# plt.scatter(df['rooms'], df['price']*10)
plt.show()


# m = ols('price ~ square',df).fit().resid
# sm.qqplot(m, line='s')
# pylab.show()
