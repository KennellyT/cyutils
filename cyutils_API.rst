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
cyutils.waste_timeseries(isotopes, mass_timeseries, duration)
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
cyutils.capacity_calc(insts, timestep, entry_exit)
    """Adds and subtracts capacity over time for plotting

    Parameters
    ----------
    insts: list
        list of insts (countries)
    timestep: np.linspace
        list of timestep from 0 to simulation time
    entry_exit: list
        power_cap, agentid, parentid, entertime, exittime
        of all entered reactors

    Returns
    -------
    power: dictionary
        "dictionary with key=government, and
        value=timeseries list capacity"
    """
cyutils.reactor_deployments(insts, timestep, entry, exit_step)
    """Adds and subtracts number of reactors deployed over time
    for plotting

    Parameters
    ----------
    insts: list
        list of insts (countries)
    timestep: np.linspace
        list of timestep from 0 to simulation time
    entry: list
        power_cap, agentid, parentid, entertime
        of all entered reactors

    exit_step: list
        power_cap, agentid, parenitd, exittime
        of all decommissioned reactors

    Returns
    -------
    deployment: dictionary
        "dictionary with key=government, and
        value=timeseries number of reactors"
    """
cyutils.multiple_line_plots(dictionary, timestep,
                        xlabel, ylabel, title,
                        outputname, init_year):
    """Creates multiple line plots of timestep vs dictionary

    Parameters
    ----------
    dictionary: dictionary
        dictionary with "key=description of timestep, and
        value=list of timestep progressions"
    timestep: numpy linspace
        timestep of simulation
    xlabel: str
        xlabel of plot
    ylabel: str
        ylabel of plot
    title: str
        title of plot
    init_year: int
        initial year of simulation

    Returns
    -------
    """
cyutils.combined_line_plot(dictionary, timestep,
                       xlabel, ylabel, title,
                       outputname, init_year):
    """Creates a combined line plot of timestep vs dictionary

    Parameters
    ----------
    dictionary: dictionary
        dictionary with "key=description of timestep, and
        value=list of timestep progressions"
    timestep: numpy linspace
        timestep of simulation
    xlabel: str
        xlabel of plot
    ylabel: str
        ylabel of plot
    title: str
        title of plot
    init_year: int
        initial year of simulation

    Returns
    -------
    """
cyutils.double_axis_bar_line_plot(dictionary1, dictionary2, timestep,
                              xlabel, ylabel1, ylabel2,
                              title, outputname, init_year)
    """Creates a double-axis plot of timestep vs dictionary

    It is recommended that a non-cumulative timeseries is on dictionary1.

    Parameters
    ----------
    dictionary1: dictionary
        dictionary with "key=description of timestep, and
        value=list of timestep progressions"
    dictionary2: dictionary
        dictionary with "key=description of timestep, and
        value=list of timestep progressions"
    timestep: numpy linspace
        timestep of simulation
    xlabel: str
        xlabel of plot
    ylabel: str
        ylabel of plot
    title: str
        title of plot
    init_year: int
        initial year of simulation

    Returns
    -------
    """
cyutils.double_axis_line_line_plot(dictionary1, dictionary2, timestep,
                               xlabel, ylabel1, ylabel2,
                               title, outputname, init_year):
    """Creates a double-axis plot of timestep vs dictionary

    Parameters
    ----------
    dictionary1: dictionary
        dictionary with "key=description of timestep, and
        value=list of timestep progressions"
    dictionary2: dictionary
        dictionary with "key=description of timestep, and
        value=list of timestep progressions"
    timestep: numpy linspace
        timestep of simulation
    xlabel: str
        xlabel of plot
    ylabel: str
        ylabel of plot
    title: str
        title of plot
    init_year: int
        initial year of simulation

    Returns
    -------
    """
cyutils.stacked_bar_chart(dictionary, timestep,
                      xlabel, ylabel, title,
                      outputname, init_year)
    """Creates stacked bar chart of timstep vs dictionary

    Parameters
    ----------
    dictionary: dictionary
        dictionary with value: timeseries data
    timestep: numpy linspace
        list of timestep (x axis)
    xlabel: str
        xlabel of plot
    ylabel: str
        ylabel of plot
    title: str
        title of plot
    init_year: int
        simulation start year

    Returns
    -------
    """
cyutils.plot_power(cur)
    """Gets capacity vs time for every country
        in stacked bar chart.

    Parameters
    ----------
    cur: sqlite cursor
        sqlite cursor

    Returns
    -------
    """
cyutils.entered_power(cur)
    """Returns dictionary of power entered into simulation.

    Parameters
    ---------
    cur: sqlite cursor
        sqlite cursor

    Returns
    -------
    power: dictionary
        key: 'power'
        value: timeseries of power entered (non-cumulative)
    """
cyutils.source_throughput(cur, duration, frac_prod, frac_tail)
    """Calculates throughput required for nat_u source before enrichment
    by calculating the average mass of fuel gone into reactors over
    simulation. Assuming natural uranium is put as feed

    Parameters
    ----------
    cur: sqlite cursor
        sqlite cursor
    duration: int
        duration of simulation
    frac_prod: float
        mass fraction of U235 in fuel after enrichment in decimals
    frac_tail: float
        mass fraction of U235 in tailings after enrichment in decimals

    Returns
    -------
    throughput: float
        appropriate nat_u throughput for source
    """
cyutils.plot_in_flux_cumulative(
        cur,
        facility,
        title)
    """plots timeseries influx/ outflux from facility name in kg.

    Parameters:
    ----------
    cur: sqlite cursor
        sqlite cursor
    facility: str
        facility name
    influx_bool: bool
        if true, calculates influx,
        if false, calculates outflux
    title: str
        title of the multi line plot
    outputname: str
        filename of the multi line plot file
    is_cum: Boolean:
        true: add isotope masses over time
        false: do not add isotope masses at each timestep

    Returns:
    --------
    """
cyutils.plot_out_flux_cumulative(
        cur,
        facility,
        title):
    """plots timeseries influx/ outflux from facility name in kg.

    Parameters:
    ----------
    cur: sqlite cursor
        sqlite cursor
    facility: str
        facility name
    influx_bool: bool
        if true, calculates influx,
        if false, calculates outflux
    title: str
        title of the multi line plot
    outputname: str
        filename of the multi line plot file
    is_cum: Boolean:
        true: add isotope masses over time
        false: do not add isotope masses at each timestep

    Returns:
    --------
    """
cyutils. plot_in_flux_basic(
        cur,
        facility,
        title):
    """plots timeseries influx/ outflux from facility name in kg.
    
    Parameters:
    ----------
    cur: sqlite cursor
        sqlite cursor
    facility: str
        facility name
    influx_bool: bool
        if true, calculates influx,
        if false, calculates outflux
    title: str
        title of the multi line plot
    outputname: str
        filename of the multi line plot file
    is_cum: Boolean:
        true: add isotope masses over time
        false: do not add isotope masses at each timestep

    Returns:
    --------
    """
cyutils.plot_out_flux_basic(
        cur,
        facility,
        title):
    """plots timeseries influx/ outflux from facility name in kg.

    Parameters:
    ----------
    cur: sqlite cursor
        sqlite cursor
    facility: str
        facility name
    influx_bool: bool
        if true, calculates influx,
        if false, calculates outflux
    title: str
        title of the multi line plot
    outputname: str
        filename of the multi line plot file
    is_cum: Boolean:
        true: add isotope masses over time
        false: do not add isotope masses at each timestep

    Returns:
    --------
    """
cyutils.plot_net_flux(
        cur,
        facility,
        title):
    """
    Plots net flux of all isotopes over the duration of the simulation.
    
    Parameters
    ----------
    cur : sqlite cursor
        sqlite cursor
    facility : str
        name of facility
    title : str
        title of plot
    Returns
    -------
    """
cyutils.mass_timeseries(cur, facility, flux):
    """
    Returns dictionary of mass timeseries of each isotope at a facility.
    Parameters
    ----------
    cur : sqlite cursor
        sqlite cursor
    facility : str
        name of facility
    flux : str
        direction of flux
    Returns
    -------
    masstime : dict
        dictionary of isotopes and their mass series
    times : list
        list of times in the simulation
    """
cyutils.cumulative_mass_timeseries(cur, facility, flux):
    """
    Returns dictionary of the cumulative mass timeseries of each isotope at a facility.
    Parameters
    ----------
    cur : sqlite cursor
        sqlite cursor
    facility : str
        name of facility
    flux : str
        direction of flux
    Returns
    -------
    masstime : dict
        dictionary of isotopes and their mass series
    times : list
        list of times in the simulation
    """
cyutils.plot_cumulative_swu(cur, facilities=[]):
    """returns dictionary of swu timeseries for each enrichment plant

    Parameters
    ----------
    cur: sqlite cursor
        sqlite cursor
    facilities : list
        list of facilities to plot

    Returns
    -------
    swu_dict: dictionary
        dictionary with "key=Enrichment (facility number), and
        value=swu timeseries list"
    """
cyutils.plot_swu(cur, facilities=[]):
    """Returns dictionary of swu timeseries for each enrichment plant

    Parameters
    ----------
    cur: sqlite cursor
        sqlite cursor
    facilities : list
        list of facilities to plot

    Returns
    -------
    swu_dict: dictionary
        dictionary with "key=Enrichment (facility number), and
        value=swu timeseries list"
    """
cyutils.plot_cumulative_power(cur, reactors):
    """
    Plots cumulative power of reactor fleet over the simulation duration.

    Parameters
    ----------
    cur : sqlite cursor
        sqlite cursor
    reactors : list
        list of reactors to plot
    Returns
    -------
    """
cyutils.plot_power_reactor(cur, reactors):
    """
    Plots power of reactor fleet over the simulation duration.

    Parameters
    ----------
    cur :  mlite cursor
        sqlite cursor
    reactors : list
        list of reactors to plot

    Returns
    -------
    """
cyutils.powerseries_reactor(cur, reactors):
    """
    Returns power of reactor fleet over the simulation duration.

    Parameters
    ----------
    cur :  mlite cursor
        sqlite cursor
    reactors : list
        list of reactors to plot

    Returns
    -------
    """
cyutils.evaluator(file_name):
    """Connects and returns a cursor to an sqlite output file

    Parameters
    ----------
    file_name: str
        name of the sqlite file

    Returns
    -------
    evaluate : Evaluator
        cymetric evalutator         
    """
cyutils.inventory_audit(evaler, agentids=[]):
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
cyutils.compositions(evaler):
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
cyutils.sql_filename(evaler):
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
cyutils.total_isotope_used(cur, facility):
    """Returns dictionary of total masses of isotopes mined

    Parameters
    ----------
     cur :  mlite cursor
        sqlite cursor
    facility : str
        str of mine facility

    Returns
    -------
    total_isotopes_mined : dict
        dictionary of isotopes mined and the total mass mined
    """
