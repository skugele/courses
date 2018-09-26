import numpy as np
# from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import pandas as pd

data_path = '../../data/earthquake_db.txt'
data = pd.read_csv(data_path, sep='\t')

sample = data.sample(n=35, random_state=1)
sample.EQ_MAG_MS = sample.EQ_MAG_MS.fillna('0')

features = sample.loc[:,['LATITUDE', 'LONGITUDE', 'EQ_MAG_MS']]
lats = sample.loc[:,['LATITUDE']].values.astype(float)
longs = sample.loc[:,['LONGITUDE']].values.astype(float)
magnitudes = sample.loc[:,['EQ_MAG_MS']].values.astype(float)

# m = Basemap(projection='hammer',lon_0=0)
# x,y = m(longs, lats)
# m.scatter(x,y,s=12,marker='x',color='r', zorder=10)
# m.drawmapboundary(fill_color='#99ffff')
# m.fillcontinents(color='#cc9966',lake_color='#99ffff')
#
# plt.title('Plot of the locations of 35 earthquake events randomly selected from the data set', fontsize=12)
# plt.show()

plt.gcf().clear()
plt.title('Plot of Earthquake Magnitude for 35\nRandomly Selected Earthquake Events', fontsize=12)
plt.xlabel('Earthquake Magnitude (EQ_MAG_MS)', size='large')
plt.ylabel('# of Earthquakes', size='large')
plt.hist(magnitudes, range=[1,10], alpha=0.35, density=False, facecolor='purple', edgecolor='black', linewidth=1.0)
plt.show()
