Python packages
===============

Pandas is a useful package for data analysis. Click on `python_pandas.ipynb` and a Jupyter Notebook (python webpage) will render.

Pandas uses DataFrames (like R), where you can pick at your data using named rows and columns. This makes it very easy to wrangle your data. Some key points: 

* Read in csv or text files very easily with `read_csv`.
* Choose data based on dates, months, times e.g. `data['2003-12':'2004-02']`.
* "Groupby" aspects of your data. So, if you want statistics grouped for each hour in your timeseries, go `data.groupby(data.index.hour).describe()`
* Resample your data, say from hourly to every 15 mins:  `data.resample('15min').interpolate(method='linear')`
* Nicer plots easily: `data.plot()`

See these examples in `python_pandas.ipynb`.