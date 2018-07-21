analysis.py

##cyutils.analysis

cyutils.analysis.cursor(file_name)
    """Connects and returns a cursor to an sqlite output file

    Parameters
    ----------
    file_name: str
        name of the sqlite file

    Returns
    -------
    sqlite cursor3
    """
cyutils.analysis.agent_ids(cur, archetype)
    """Gets all agentids from Agententry table for wanted archetype

        agententry table has the following format:
            SimId / AgentId / Kind / Spec /
            Prototype / ParentID / Lifetime / EnterTime

    Parameters
    ----------
    cur: cursor
        sqlite cursor3
    archetype: str
        agent's archetype specification

    Returns
    -------
    agentids: list
        list of all agentId strings
    """
cyutils.analysis.prototype_id(cur,prototype)
    """Returns agentid of a prototype

    Parameters
    ----------
    cur: sqlite cursor
        sqlite cursor
    prototype: str
        name of prototype

    Returns
    -------
    agent_id: list
        list of prototype agentids as strings
    """
cyutils.analysis.institutions(cur)
    """Returns prototype and agentids of institutions

    Parameters
    ----------
    cur: sqlite cursor
        sqlite cursor

    Returns
    -------
    sqlite query result (list of tuples)
    """
cyutils.analysis.timestep_to_years(init_year, timestep)
    """Returns list of years in simulation

    Parameters
    ----------
    init_year: int
        initial year in simulation
    timestep: np.array
        timestep of simulation (months)

    Returns
    -------
    array of years
    """
cyutils.analysis.exec_string(specific_search, search, request_colmn)
    """Generates sqlite query command to select things and
        inner join resources and transactions.

    Parameters
    ----------
    specific_search: list
        list of items to specify search
        This variable will be inserted as sqlite
        query arugment following the search keyword
    search: str
        criteria for specific_search search
        This variable will be inserted as sqlite
        query arugment following the WHERE keyword
    request_colmn: str
        column (set of values) that the sqlite query should return
        This variable will be inserted as sqlite
        query arugment following the SELECT keyword

    Returns
    -------
    str
        sqlite query command.
    """

cyutils.analysis.simulation_timesteps(cur)
    """Returns simulation start year, month, duration and
    timesteps (in numpy linspace).

    Parameters
    ----------
    cur: sqlite cursor
        sqlite cursor

    Returns
    -------
    init_year: int
        start year of simulation
    init_month: int
        start month of simulation
    duration: int
        duration of simulation
    timestep: list
        linspace up to duration
    """

cyutils.analysis.timeseries(specific_search, duration, kg_to_tons)
    """returns a timeseries list from specific_search data.

    Parameters
    ----------
    specific_search: list
        list of data to be created into timeseries
        list[0] = time
        list[1] = value, quantity
    duration: int
        duration of the simulation
    kg_to_tons: bool
        if True, list returned has units of tons
        if False, list returned as units of kilograms

    Returns
    -------
    timeseries list of commodities stored in specific_search
    """
cyutils.analysis.timeseries_cum(specific_search, duration, kg_to_tons)
    """Returns a timeseries list from specific_search data.

    Parameters
    ----------
    specific_search: list
        list of data to be created into timeseries
        list[0] = time
        list[1] = value, quantity
    multiplyby: int
        integer to multiply the value in the list by for
        unit conversion from kilograms
    kg_to_tons: bool
        if True, list returned has units of tons
        if False, list returned as units of kilograms

    Returns
    -------
    timeseries of commodities in kg or tons
    """
cyutils.analysis.isotope_transactions(resources, compositions)
    """Creates a dictionary with isotope name, mass, and time

    Parameters
    ----------
    resources: list of tuples
        resource data from the resources table
        (times, sum(quantity), qualid)
    compositions: list of tuples
        composition data from the compositions table
        (qualid, nucid, massfrac)

    Returns
    -------
    transactions: dictionary
        dictionary with "key=isotope, and
        value=list of tuples (time, mass_moved)"
    """
cyutils.analysis.facility_commodity_flux(cur, agentids,
                            facility_commodities, is_outflux,
                            is_cum=True)
    """Returns dictionary of commodity in/outflux from agents

    Parameters
    ----------
    cur: sqlite cursor
        sqlite cursor
    agentids: list
        list of agentids
    facility_commodities: list
        list of commodities
    is_outflux: bool
        gets outflux if True, influx if False
    is_cum: bool
        gets cumulative timeseris if True, monthly value if False

    Returns
    -------
    commodity_region: dictionary
        dictionary with "key=commodity, and
        value=timeseries list of masses in kg"
    """
cyutils.analysis.commodity_flux_region(cur, agentids, commodities,
                          is_outflux, is_cum=True)
    """Returns dictionary of timeseries of all the commodity outflux,
        that is either coming in/out of the agent
        separated by region

    Parameters
    ----------
    cur: sqlite cursor
        sqlite cursor
    agentids: list
        list of agentids
    commodities: list
        list of commodities to include
    is_outflux: bool
        gets outflux from agent if True
        gets influx to agent if False
    is_cum: bool
        gets cumulative timeseris if True, monthly value if False

    Returns
    -------
    commodity_region: dictionary
        dictionary with "key=region, and
        value= timeseries list of masses in kg"
    """
cyutils.analysis.facility_commodity_flux_isotopics(
        cur,
        agentids,
        facility_commodities,
        is_outflux,
        is_cum=True)
    """Returns timeseries isotoptics of commodity in/outflux
    from agents

    Parameters
    ----------
    cur: sqlite cursor
        sqlite cursor
    agentids: list
        list of agentids
    facility_commodities: list
        list of commodities
    is_outflux: bool
        gets outflux if True, influx if False
    is_cum: bool
        gets cumulative timeseries if True, monthly value if False

    Returns
    -------
    isotope_timeseries: dictionary
        dictionary with "key=isotope, and
        value=timeseries list of masses in kg"
    """

cyutils.analysis.stockpiles(cur, facility, is_cum=True):
    """gets inventory timeseries in a fuel facility

    Parameters
    ----------
    cur: sqlite cursor
        sqlite cursor
    facility: str
        name of facility
    is_cum: bool
        gets cumulative timeseris if True, monthly value if False

    Returns
    -------
    pile: dictionary
        dictionary with "key=agent type, and
        value=timeseries list of stockpile"
    """
cyutils.analysis.swu_timeseries(cur, is_cum=True):
    """returns dictionary of swu timeseries for each enrichment plant

    Parameters
    ----------
    cur: sqlite cursor
        sqlite cursor
    is_cum: bool
        gets cumulative timeseris if True, monthly value if False

    Returns
    -------
    swu: dictionary
        dictionary with "key=Enrichment (facility number), and
        value=swu timeseries list"
    """
cyutils.analysis.power_capacity(cur):
    """Gets dictionary of power capacity by calling capacity_calc

    Parameters
    ----------
    cur: sqlite cursor
        sqlite cursor

    Returns
    ------
    power: dictionary
        "dictionary with key=government, and
        value=timeseries list of installed capacity"
    """
cyutils.analysis.power_capacity_of_region(cur, region_name)
    """Gets dictionary of power capacity of a specific region

    Parameters
    ----------
    cur: sqlite cursor
    region_name: str
        name of region to serach for

    Returns
    -------
    power: dictionary
        "dictionary with key=government and
        value=timeseries list of installed capacity"
    """
cyutils.analysis.deployments(cur)
    """Gets dictionary of reactors deployed over time
    by calling reactor_deployments

    Parameters
    ----------
    cur: sqlite cursor
        sqlite cursor

    Returns
    ------
    deployment_government: dictionary
        "dictionary with key=government, and
        value=timeseries list of number of reactors"
    """
cyutils.analysis.fuel_usage_timeseries(cur, fuels, is_cum=True)
    """Calculates total fuel usage over time

    Parameters
    ----------
    cur: sqlite cursor
        sqlite cursor
    fuels: list
        list of fuel commodity names (eg. uox, mox) as string
        to consider in fuel usage.
    is_cum: bool
        gets cumulative timeseris if True, monthly value if False

    Returns
    -------
    fuel_usage: dictionary
        dictionary with "key=fuel (from fuels),
        value=timeseries list of fuel amount [kg]"
    """
cyutils.analysis.nat_u_timeseries(cur, is_cum=True)
    """Finds natural uranium supply from source
        Since currently the source supplies all its capacity,
        the timeseriesenrichmentfeed is used.

    Parameters
    ----------
    cur: sqlite cursor
        sqlite cursor
    is_cum: bool
        gets cumulative timeseris if True, monthly value if False

    Returns
    -------
    timeseries: function
        calls a function that returns timeseries list of natural U
        demand from enrichment [MTHM]
    """
cyutils.analysis.trade_timeseries(cur, sender, receiver,
                     is_prototype, do_isotopic,
                     is_cum=True)
    """Returns trade timeseries between two prototypes' or facilities
    with or without isotopics

    Parameters
    ----------
    cur: sqlite cursor
        sqlite cursor
    sender: str
        name of sender as facility type or prototype name
    receiver: str
        name of receiver as facility type or prototype name
    is_prototype: bool
        if True, search sender and receiver as prototype,
        if False, as facility type from spec.
    do_isotopic: bool
        if True, perform isotopics (takes significantly longer)
    is_cum: bool
        gets cumulative timeseris if True, monthly value if False

    Returns:
    --------
    trades: dictionary
        if do_isotopic:
            dictionary with "key=isotope, and
                        value=timeseries list
                        of mass traded between
                        two prototypes"
        else:
            dictionary with "key=string, sender to receiver,
                        value=timeseries list of mass traded
                        between two prototypes"

    """
cyutils.analysis.final_stockpile(cur, facility)
    """get final stockpile in a fuel facility

    Parameters
    ----------
    cur: sqlite cursor
        sqlite cursor
    facility: str
        name of facility

    Returns
    -------
    mthm_stockpile: str
        MTHM value of stockpile
    """
cyutils.analysis.fuel_into_reactors(cur, is_cum=True)
    """Finds timeseries of mass of fuel received by reactors

    Parameters
    ----------
    cur: sqlite cursor
        sqlite cursor
    is_cum: bool
        gets cumulative timeseris if True, monthly value if False

    Returns
    -------
    timeseries list of fuel into reactors [tons]
    """
cyutils.analysis.u_util_calc(cur)
    """Returns fuel utilization factor of fuel cycle

    Parameters
    ----------
    cur: sqlite cursor
        sqlite cursor

    Returns
    -------
    u_util_timeseries: numpy array
        Timeseries of Uranium utilization factor
    Prints simulation average Uranium Utilization
    """
cyutils.analysis.plot_uranium_utilization(cur)
    """Plots uranium utilization factor of fuel cycle

    Parameters
    ----------
    cur: sqlite cursor
        sqlite cursor

    Returns
    -------
    none
    """
cyutils.analysis.commodity_origin(cur, commodity, prototypes, is_cum=True)
    """Returns dict of where a commodity is from

    Parameters
    ----------
    cur: sqlite cursor
        sqlite cursor
    commodity: str
        name of commodity
    prototypes: list
        list of prototypes that provide the commodity

    Returns
    -------
    prototype_trades: dictionary
        "dictionary with key=prototype name, and
        value=timeseries list of commodity sent from prototypes"
    """
cyutils.analysis.commodity_per_institution(cur, commodity, timestep=10000)
    """Outputs outflux of commodity per institution
        before timestep

    Parameters
    ----------
    cur: sqlite cursor
        sqlite cursor
    commodity: str
        commodity to search for

    Returns
    -------
    institution_output: dictionary
        key = institution
        value = timeseries list of outflux of commodity
    """
cyutils.analysis.waste_mass_series(isotopes, mass_timeseries, duration)
    """Given an isotope, mass and time list, creates a dictionary
       With key as isotope and time series of the isotope mass.

    Parameters
    ----------
    isotopes: list
        list with all the isotopes from resources table
    mass_timeseries: list
        a list of lists.  each outer list corresponds to a different isotope
        and contains tuples in the form (time,mass) for the isotope transaction.
    duration: integer
        simulation duration

    Returns
    -------
    waste_mass: dictionary
        dictionary with "key=isotope, and
        value=mass timeseries of each unique isotope"   
    """
cyutils.analysis.waste_timeseries(isotopes, mass_timeseries, duration)
    """Given an isotope, mass and time list, creates a dictionary
       With key as isotope and time series of the isotope mass.

    Parameters
    ----------
    isotopes: list
        list with all the isotopes from resources table
    mass_timeseries: list
        a list of lists.  each outer list corresponds to a different isotope
        and contains tuples in the form (time,mass) for the isotope transaction.
    duration: integer
        simulation duration

    Returns
    -------
    waste_time: dictionary
        dictionary with "key=isotope, and
        value=mass timeseries of each unique isotope"   
    """
