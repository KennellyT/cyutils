from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import csv 

class Pris_reactor(object):
    """Pris_reactor class includes information on certain reactors"""

    def __init__(self, reactor_name='', reactor_status='', reactor_type='',
                 model='', operator='', start_date='',
                 shutdown_date='', years = None,ele_supplied_GWh = None,ref_unit_power_MW = None,annual_time_online_hr = None,op_factor = None,energy_aval_factor_annual = None,load_factor_annual = None):
        """Define gamma spectrum specific variables """
        super(Pris_reactor, self).__init__()
        self.reactor_name = reactor_name
        self.reactor_status = reactor_status
        self.reactor_type = reactor_type
        self.model = model
        self.operator = operator
        self.start_date = start_date
        self.shutdown_date = shutdown_date
        self.years = [] if years is None else years
        self.ele_supplied_GWh = [] if ele_supplied_GWh is None else ele_supplied_GWh
        self.ref_unit_power_MW = [] if ref_unit_power_MW is None else ref_unit_power_MW
        self.annual_time_online_hr = [] if annual_time_online_hr is None else annual_time_online_hr
        self.op_factor = [] if op_factor is None else op_factor
        self.energy_aval_factor_annual = [] if energy_aval_factor_annual is None else energy_aval_factor_annual
        self.load_factor_annual = [] if load_factor_annual is None else load_factor_annual


def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None

def is_good_response(resp):
    """
    Returns true if the response seems to be HTML, false otherwise
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors. 
    This function just prints them, but you can
    make it do anything.
    """
    print(e)


def pris_raw_data(url):
    url = 'https://www.iaea.org/PRIS/CountryStatistics/ReactorDetails.aspx?current=640'
    raw_html = simple_get(url)
    html = BeautifulSoup(raw_html, 'html.parser')
    data = html.findAll('tr')
    raw_reactor_data = []
    for i in range(len(data)):
        nums = data[i].findAll('td')
        for j in nums:
            info = j.text
            info_no_new_lines=info.replace('\n','')
            striped_info = info_no_new_lines.replace('\r','').replace(" ","")
            raw_reactor_data.append(striped_info)
    return raw_reactor_data


def html_cur(url):
    raw_html = simple_get(url)
    html = BeautifulSoup(raw_html, 'html.parser')
    return html

def reactor_info(url):
    reactor = Pris_reactor()
    html = html_cur(url)
    reactor_name_find = html.findAll('h1')
    reactor_name = reactor_name_find[0].text.replace('\n','')
    reactor.reactor_name = reactor_name
    reactor_status_find = html.findAll('h5')
    reactor_status = reactor_status_find[0].text.replace('\n','')
    reactor.reactor_status = reactor_status
     
    owner_type_info = ['ReactorType','Model', 'Owner', 'Operator','CommercialOperationDate','PermanentShutdownDate'] 
    owner = {}    
    for info in owner_type_info:
        if info in pris_raw_data(url):
            info_place = pris_raw_data(url).index(info) + 4 
            owner[info] =  pris_raw_data(url)[info_place]
    reactor_type = owner['ReactorType']   
    reactor.reactor_type = reactor_type
    model = owner['Model']   
    reactor.model = model
    reactor_owner = owner['Owner']
    reactor.owner = reactor_owner
    reactor_operator = owner['Operator']
    reactor.operator = reactor_operator
    commercial_start_date= owner['CommercialOperationDate']
    reactor.start_date = commercial_start_date
    permanent_shutdown_date = owner['PermanentShutdownDate']
    reactor.shutdown_date = permanent_shutdown_date
    return reactor

def reactor_data(url):
    
    reactor = Pris_reactor()
    reactor_info = pris_raw_data(url)
    lifetime = ['ElectricitySupplied','EnergyAvailabilityFactor',
     'OperationFactor',
     'EnergyUnavailabilityFactor',
     'LoadFactor']
    capacities = ['ReferenceUnitPower(NetCapacity)', 'DesignNetCapacity', 'GrossCapacity', 'ThermalCapacity']
    
    capacity_info = {}
    for capacity in capacities:
        if capacity in reactor_info:
            cap_place = reactor_info.index(capacity) + 4 
            capacity_info[capacity] =  reactor_info[cap_place]
    lifetime_preformance = {}
    
    for metric in lifetime:
        if metric in reactor_info:
            metric_place = reactor_info.index(metric) + 5 
            lifetime_preformance[metric] =  reactor_info[metric_place]
    time_start = reactor_info.index(list(lifetime_preformance.keys())[-1]) + 6
    years = reactor_info[time_start::9][:-1]
    ele_supplied_GWh = reactor_info[time_start+1::9][:-1]
    ref_unit_power_MW = reactor_info[time_start+2::9][:-1]
    annual_time_online_hr = reactor_info[time_start+3::9][:-1]
    op_factor = reactor_info[time_start+4::9]
    energy_aval_factor_annual = reactor_info[time_start+5::9]
    load_factor_factor_annual = reactor_info[time_start+7::9]
    reactor.years = years
    reactor.ele_supplied_GWh = ele_supplied_GWh
    reactor.ref_unit_power_MW = ref_unit_power_MW
    reactor.annual_time_online_hr = annual_time_online_hr
    reactor.op_factor = op_factor
    reactor.energy_aval_factor_annual = energy_aval_factor_annual
    reactor.load_factor_factor_annual = load_factor_factor_annual
    return reactor
def write_pris_csv(url):   
    reactor_info = pris_raw_data(url)
    owner_type_info = ['ReactorType','Model', 'Owner', 'Operator','CommercialOperationDate','PermanentShutdownDate'] 
    owner = {}    
    for info in owner_type_info:
        if info in pris_raw_data(url):
            info_place = pris_raw_data(url).index(info) + 4 
            owner[info] =  pris_raw_data(url)[info_place]
    lifetime = ['ElectricitySupplied','EnergyAvailabilityFactor',
     'OperationFactor',
     'EnergyUnavailabilityFactor',
     'LoadFactor']
    capacities = ['ReferenceUnitPower(NetCapacity)', 'DesignNetCapacity', 'GrossCapacity', 'ThermalCapacity']
    
    capacity_info = {}
    for capacity in capacities:
        if capacity in reactor_info:
            cap_place = reactor_info.index(capacity) + 4 
            capacity_info[capacity] =  reactor_info[cap_place]
    lifetime_preformance = {}
    
    for metric in lifetime:
        if metric in reactor_info:
            metric_place = reactor_info.index(metric) + 5 
            lifetime_preformance[metric] =  reactor_info[metric_place]
    time_start = reactor_info.index(list(lifetime_preformance.keys())[-1]) + 6
    years = reactor_info[time_start::9][:-1]
    ele_supplied_GWh = reactor_info[time_start+1::9][:-1]
    ref_unit_power_MW = reactor_info[time_start+2::9][:-1]
    annual_time_online_hr = reactor_info[time_start+3::9][:-1]
    op_factor = reactor_info[time_start+4::9]
    energy_aval_factor_annual = reactor_info[time_start+5::9]
    load_factor_factor_annual = reactor_info[time_start+7::9]
    operating_hist  = {}
    operating_hist['years'] = years
    operating_hist['ele_supplied_GWh'] = ele_supplied_GWh
    operating_hist['ref_unit_power_MW'] = ref_unit_power_MW
    operating_hist['annual_time_online_hr']= annual_time_online_hr
    operating_hist['op_factor'] = op_factor
    operating_hist['energy_aval_factor_annual'] =energy_aval_factor_annual
    operating_hist['load_factor_factor_annual'] = load_factor_factor_annual
    
    ownership =  list(owner.keys())
    capacity_units = list(capacity_info.keys())
    lifetime_perform_title = list(lifetime_preformance.keys())
    ownership.extend(capacity_units)
    ownership.extend(lifetime_perform_title)
    ownership_vals =  list(owner.values())
    capacity_vals = list(capacity_info.values())
    lifetime_perform_vals = list(lifetime_preformance.values())
    ownership_vals.extend(capacity_vals)
    ownership_vals.extend(lifetime_perform_vals) 
    with open('reactors.csv', 'w') as csvfile:
        reactor_write = csv.writer(csvfile, delimiter=',')
        reactor_write.writerow(ownership)
        reactor_write.writerow(ownership_vals)
        
    operating_data = list(zip(years,ele_supplied_GWh,ref_unit_power_MW,annual_time_online_hr,op_factor,energy_aval_factor_annual,load_factor_factor_annual))
    with open('reactors_year.csv', 'w') as csvfile:
        reactor_write = csv.writer(csvfile, delimiter=',')  
        reactor_write.writerow(operating_hist.keys())
        for i in range(len(operating_data)):
            reactor_write.writerow(operating_data[i])
    



