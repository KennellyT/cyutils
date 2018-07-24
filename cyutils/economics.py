import collections
import numpy as np
import matplotlib.pyplot as plt
import sqlite3 as lite
import sys
from itertools import cycle
from matplotlib import cm
from pyne import nucname
import cymetric as cym
from cymetric import filters
import pandas as pd
from collections import Counter
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from cymetric import graphs
from cyutils import analysis

if len(sys.argv) < 2:
    print('Usage: python economics.py [cylus_output_file]')

def swu_economic_cost(cur,cost_per_swu):
    """Returns plot of swu timeseries for each enrichment plant

    Parameters
    ----------
    cur: sqlite cursor
        sqlite cursor
    cost_per_swu : int or list
        cost per swu 

    Returns
    -------
    facility_swu_cost : dict
        swu cost series per facility
    """
    swu_values = analysis.swu_series(cur)[0]
    swu_times = analysis.swu_series(cur)[1]
    facilities = [item[0] for item in swu_values.items()]
    swus = [item[1] for item in swu_values.items()]
    swu_cost = np.array(cost_per_swu)
    swu_cost_series = [item*swu_cost for item in swus]
    times = [item[1] for item in swu_times.items()][0]   
    facility_swu_cost = {}
    for facility,swu_cost in list(zip(facilities,swu_cost_series)):
            facility_swu_cost.update({facility:swu_cost}) 
    return facility_swu_cost

def cumulative_swu_economic_cost(cur,cost_per_swu):
    """Returns plot of swu timeseries for each enrichment plant

    Parameters
    ----------
    cur: sqlite cursor
        sqlite cursor
    cost_per_swu : int or list
        cost per swu 

    Returns
    -------
    facility_swu_cumulative_cost : dict
        swu cumulative cost series per facility
    """
    swu_values = analysis.swu_series(cur)[0]
    swu_times = analysis.swu_series(cur)[1]
    facilities = [item[0] for item in swu_values.items()]
    swus = [item[1] for item in swu_values.items()]
    swu_cost = np.array(cost_per_swu)
    swu_cost_series = [np.cumsum(item*swu_cost) for item in swus]
    times = [item[1] for item in swu_times.items()][0]   
    facility_cumulative_swu_cost = {}
    for facility,swu_cost in list(zip(facilities,swu_cost_series)):
            facility_cumulative_swu_cost.update({facility:swu_cost}) 
    return facility_cumulative_swu_cost

def plot_swu_economic_cost(cur,cost_per_swu):
    """Returns plot of swu timeseries for each enrichment plant

    Parameters
    ----------
    cur: sqlite cursor
        sqlite cursor
    cost_per_swu : int or list
        cost per swu 

    Returns
    -------
    """
    swu_values = analysis.swu_series(cur)[0]
    swu_times = analysis.swu_series(cur)[1]
    facilities = [item[0] for item in swu_values.items()]
    swus = [item[1] for item in swu_values.items()]
    swu_cost = np.array(cost_per_swu)
    swu_cost_series = [item*swu_cost for item in swus]
    times = [item[1] for item in swu_times.items()][0]
    plt.stackplot(times, swu_cost_series, labels=facilities)
    plt.legend(loc='upper left')
    plt.xlabel('Time [months]')
    plt.ylabel('SWU Cost [$]')
    plt.title('SWU cost by facility')
    plt.show()  
 
def plot_cumulative_swu_economic_cost(cur,cost_per_swu):
    """Returns plot of swu timeseries for each enrichment plant

    Parameters
    ----------
    cur: sqlite cursor
        sqlite cursor
    cost_per_swu : int or list
        cost per swu 

    Returns
    -------
    """
    swu_values = analysis.swu_series(cur)[0]
    swu_times = analysis.swu_series(cur)[1]
    swu_sort = sorted(swu_values.items(), key=lambda e: e[
        1][0], reverse=True)
    facilities = [item[0] for item in swu_sort]
    swus = [item[1] for item in swu_sort]
    swu_cost = np.array(cost_per_swu)
    swu_cost_series = [np.cumsum(item*swu_cost) for item in swus]
    times = [item[1] for item in swu_times.items()][0]
    plt.stackplot(times, swu_cost_series, labels=facilities)
    plt.legend(loc='upper left')
    plt.xlabel('Time [months]')
    plt.ylabel('SWU Cost [$]')
    plt.title('SWU cost by facility')
    plt.show()    