import cymetric as cym
from cymetric import filters
import pandas as pd
outputfile = cym.dbopen('/home/tyler/cymetric-develop/singlereactor.sqlite')
ev1 = cym.Evaluator(outputfile)


def significant_quantity(evaler, resource=None):
    """Creates a dataframe that lists the Significant Quantities of a resource f
        found in a cyclus output file.

    Parameters
    ----------
    evaler : str
        Cyclus evaluator
    resource : str
        Resource to gather significant quantity data on
    Returns
    -------
    wanted_iso_df: df
        Data frame with significant quantity data

    """
    if resource == '922350000':
        nuc = resource
        x = 25.0
        wanted_iso = filters.transactions_nuc(evaler, nucs=[nuc])
        wanted_iso_df = wanted_iso.assign(SQ=wanted_iso['Mass'] / x)
    if resource == '942390000':
        nuc = resource
        x = 8.0
        wanted_iso = filters.transactions_nuc(evaler, nucs=[nuc])
        wanted_iso_df = wanted_iso.assign(SQ=wanted_iso['Mass'] / x)
    if resource == 'natural uranium':
        nuc = 'u-ore'
        x = 10000.0
        wanted_iso = filters.transactions_nuc(evaler, commodities=[nuc])
        wanted_iso_combine = wanted_iso.reset_index().groupby("ResourceId").sum()
        wanted_iso_combine.loc[
            wanted_iso_combine['NucId'] == 1844730000,
            'NucId'] = 'natural uraninum'
        wanted_iso_df = wanted_iso_combine.assign(
            SQ=wanted_iso_combine['Mass'] / x)
    if resource == '942390000':
        nuc = resource
        x = 8.0
        wanted_iso = filters.transactions_nuc(evaler, nucs=[nuc])
        wanted_iso_df = wanted_iso.assign(SQ=wanted_iso['Mass'] / x)
    return wanted_iso_df


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
