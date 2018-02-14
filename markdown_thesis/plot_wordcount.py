import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

print('plotting wordcount from log_wordcount.txt...')

data = pd.read_csv('log_wordcount.txt',delim_whitespace=True,header=None,
	names=['date','words'],parse_dates=['date'],index_col=[0])

plt.close('all')
fig, ax = plt.subplots(nrows=1,ncols=1,figsize=(8,5))

data.plot(ax=ax,title='Words in commited thesis files',legend=False)

# ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
# ax.xaxis.set_major_formatter(mdates.DateFormatter('%b\n%d'))
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))

ax.set_xlim(pd.Timestamp('2018-01-01'), pd.Timestamp('2018-09-01'))
xmax = data.max()[0]*1.05
ax.set_ylim(0, xmax)

# deadlines
ax.vlines(pd.Timestamp('2018-06-01'),ymin=0, ymax=xmax, color='0.6')
ax.text(pd.Timestamp('2018-06-01'),data.max()[0]*0.05, 'draft',
	color='0.6',rotation=90,va='bottom',ha='right')

ax.vlines(pd.Timestamp('2018-08-01'),ymin=0, ymax=xmax, color='0.6')
ax.text(pd.Timestamp('2018-08-01'),data.max()[0]*0.05, 'final',
	color='0.6',rotation=90,va='bottom',ha='right')

ax.vlines(pd.Timestamp('2018-08-31'),ymin=0, ymax=xmax, color='0.6')
ax.text(pd.Timestamp('2018-08-31'),data.max()[0]*0.05, 'deadline',
	color='0.6',rotation=90,va='bottom',ha='right')

plt.xticks(ax.get_xticks(), rotation=0,ha='center')
plt.xlabel('')
plt.tight_layout()
plt.savefig('plot_wordcount.png')

print('done')