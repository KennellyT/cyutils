#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 24 09:37:16 2018

@author: tyler
"""
#https://realpython.com/python-web-scraping-practical-introduction/
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import csv   

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

raw_html = simple_get('https://www.iaea.org/PRIS/CountryStatistics/ReactorDetails.aspx?current=640')
html = BeautifulSoup(raw_html, 'html.parser')
titles = html.findAll('th')  # skip the first 2 header rows        
data = html.findAll('tr')
reactor_info = []
for i in range(len(data)):
    nums = data[i].findAll('td')
    for j in nums:
        info = j.text
        info_no_new_lines=info.replace('\n','')
        striped_info = info_no_new_lines.replace('\r','').replace(" ","")
        reactor_info.append(striped_info)
re_data = html.findAll('tbody')
reactor_name_find = html.findAll('h1')
reactor_name = reactor_name_find[0].text.replace('\n','')
reactor_status_find = html.findAll('h5')
reactor_status = reactor_status_find[0].text.replace('\n','')



owner_type_info = ['ReactorType','Model', 'Owner', 'Operator','CommercialOperationDate','PermanentShutdownDate'] 
owner = {}    
for info in owner_type_info:
    if info in reactor_info:
        info_place = reactor_info.index(info) + 4 
        owner[info] =  reactor_info[info_place]
        
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
operating_hist  = {}
time_start = reactor_info.index(list(lifetime_preformance.keys())[-1]) + 6
years = reactor_info[time_start::9][:-1]
ele_supplied_GWh = reactor_info[time_start+1::9][:-1]
ref_unit_power_MW = reactor_info[time_start+2::9][:-1]
annual_time_online_hr = reactor_info[time_start+3::9][:-1]
op_factor = reactor_info[time_start+4::9]
energy_aval_factor_annual = reactor_info[time_start+5::9]
load_factor_factor_annual = reactor_info[time_start+7::9]
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
import csv
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
