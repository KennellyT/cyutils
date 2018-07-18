import cymetric as cym
from cymetric import filters
import pandas as pd
import collections
import numpy as np
import matplotlib.pyplot as plt
from pyne import nucname
outputfile = cym.dbopen('/home/tyler/cymetric-develop/singlereactor.sqlite')
ev1 = cym.Evaluator(outputfile)

def evaluator(file_name):
    """Connects and returns a cursor to an sqlite output file

    Parameters
    ----------
    file_name: str
        name of the sqlite file

    Returns
    -------
    sqlite cursor3
    """
    outputfile = cym.dbopen(file_name)
    evaluate = cym.Evaluator(outputfile)
    return evaluate

# =============================================================================
# def significant_quantity(evaler, resource=None):
#     """Creates a dataframe that lists the Significant Quantities of a resource f
#         found in a cyclus output file.
# 
#     Parameters
#     ----------
#     evaler : str
#         Cyclus evaluator
#     resource : str
#         Resource to gather significant quantity data on
#     Returns
#     -------
#     wanted_iso_df: df
#         Data frame with significant quantity data
# 
#     """
#     if resource == '922350000':
#         global wanted_iso_df
#         nuc = resource
#         x = 25.0
#         wanted_iso = filters.transactions_nuc(evaler, nucs=[nuc])
#         wanted_iso_df = wanted_iso.assign(SQ=wanted_iso['Mass'] / x)
#     if resource == '942390000':
#         global wanted_iso_df
#         nuc = resource
#         x = 8.0
#         wanted_iso = filters.transactions_nuc(evaler, nucs=[nuc])
#         wanted_iso_df = wanted_iso.assign(SQ=wanted_iso['Mass'] / x)
#     if resource == 'natural uranium':
#         global wanted_iso_df        
#         nuc = 'u-ore'
#         x = 10000.0
#         wanted_iso = filters.transactions_nuc(evaler, commodities=[nuc])
#         wanted_iso_combine = wanted_iso.reset_index().groupby("ResourceId").sum()
#         wanted_iso_combine.loc[
#             wanted_iso_combine['NucId'] == 1844730000,
#             'NucId'] = 'natural uraninum'
#         wanted_iso_df = wanted_iso_combine.assign(
#             SQ=wanted_iso_combine['Mass'] / x)
#     if resource == '942390000':
#         global wanted_iso_df 
#         nuc = resource
#         x = 8.0
#         wanted_iso = filters.transactions_nuc(evaler, nucs=[nuc])
#         wanted_iso_df = wanted_iso.assign(SQ=wanted_iso['Mass'] / x)
#     return wanted_iso_df
# 
# =============================================================================

def power_timeseries(evaler, agentids=[]):
    """Returns power by AgentId timeseries

    Parameters
    ----------
    evaler : str
        Cyclus evaluator
    agentids : list of int
        AgentIds to collect data on
    Returns
    -------
    power: df
        Data frame of power timeseries
    """
    power = evaler.eval('TimeSeriesPower')
    power.rename(columns={'Value': 'Power [MWe]'}, inplace=True)
    if len(agentids) != 0:
        power = power[power['AgentId'].isin(agentids)]
    return power


def inventory_audit(evaler, agentids=[]):
    """Returns timeseries of AgentStateInventories

    Parameters
    ----------
    evaler : str
        Cyclus evaluator
    agentids : list of int
        AgentIds to collect data on
    Returns
    -------
    audit: df
        Data frame of AgentStateInventories timeseries
    """
    audit = evaler.eval('AgentStateInventories')
    if len(agentids) != 0:
        audit = audit[audit['AgentId'].isin(agentids)]
    return audit


def compositions(evaler):
    """Returns timeseries of composition data

    Parameters
    ----------
    evaler : str
        Cyclus evaluator

    Returns
    -------
    mass_frac: df
        Data frame of QualId mass fraction data
    """
    mass_frac = evaler.eval('Compositions')
    return mass_frac

def sql_filename(evaler):
    """Returns cyclus sql filename

    Parameters
    ----------
    evaler : str
        Cyclus evaluator

    Returns
    -------
    sql_filename: str
        sql cyclus filename
    """
    filename = evaler.db.name
    return filename

def timeseries_power(sql_filename,agentids=[]):
    """Returns timeseries of power data by AgentId

    Parameters
    ----------
    sql_filename : str
        Cyclus sqllite file location

    Returns
    -------
    power_series: df
        Data frame of power series data 
    """
    db = cym.dbopen(sql_filename)
    power_series = cym.eval('TimeSeriesPower', db)
    if len(agentids) != 0:
        power_series = power_series[power_series['AgentId'].isin(agentids)]
    return power_series

def power_agent_id(sql_filename,agentids=[]):
    """Returns list of power data by AgentId

    Parameters
    ----------
    sql_filename : str
        Cyclus sqllite file location

    Returns
    -------
    agent_id_power: list
        list of power series data for a certain AgentId 
    """
    db = cym.dbopen(sql_filename)
    power_series = cym.eval('TimeSeriesPower', db)
    agent_id_power = power_series['Value']
    if len(agentids) != 0:
        power_series = power_series[power_series['AgentId'].isin(agentids)]
        agent_id_power = power_series['Value']
    plt.plot(power_series['Time'],agent_id_power)
    
    return agent_id_power

def total_isotope_mined(evaler,isotope=[],mines=[]):
    total_iso = filters.transactions_nuc(evaler,nucs=isotope,senders=mines)
    total_isotope_mass = np.cumsum(list(total_iso['Mass']))
    print('total_mass of isotope in kg:') 
    return total_isotope_mass[-1]

def facility_commodity_flux(evaler, agentids=[],
                            facility_commodities=[]
                            ,receivers=[],senders=[]):
    """Returns timeseries isotoptics of commodity in/outflux
    from agents

    Parameters
    ----------
    evaler : cyclus evaluator
        cyclus evaluator
    agentids : list
        list of agentids
    facility_commodities : list
        list of commodities
    receivers : list
        list of ReceiverPrototypes
    senders : list
        list of SenderProtoypes


    Returns
    -------
    isotopes_transactions: df
        dataframe with isotope transaction timeseries
    """
    commodities = facility_commodities
    isotopes_transactions = filters.transactions_nuc(evaler,commodities,receivers,senders)
    return isotopes_transactions

