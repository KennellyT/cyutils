import sys
import jinja2
import numpy as np
import os
import pandas as pd
import csv
import collections
import matplotlib.pyplot as plt
import sqlite3 as lite
from itertools import cycle
import matplotlib
from matplotlib import cm
import pyne
from pyne import nucname
from operator import itemgetter


def write_csv(header, raw_input, filename='csv-data.csv'):
    """Writes a csv file given the header, data, and the desired name of the
        csv file

    Parameters
    ----------
    header: list
        list of strings of the headers for the csv file
    data_input: csv data
        data to be added to csv file
    filename: string
        output file name, default: 'csv-data.csv'

    Returns
    -------
    Notes
    -------
    note:  this function expects raw data in the form of [[a1, a2, ... , aN],[b1, b2, ... ,bN]...[n1, n2, nN]],
            but it will put this data in the form of [[a1,b1,...,n1],[a2,b2,...,n2],...,[aN,bN,...,nN]] before
            writing it to the csv file.  Additionally, please be sure that the order of data in the raw input
            matches the order of headers.  Using the previous example of an arbitrary raw input, the header
            should be: ['header a','header b',...,'header n'].
    """
    if os.path.exists('./' + filename) is True:
        os.remove(filename)

    if isinstance(raw_input[0], list):

        data_input = []

        for element in range(len(raw_input[0])):
            data_input.append([])

        for element in range(len(raw_input[0])):
            for index in range(len(raw_input)):
                placeholder = raw_input[index]
                data_input[element].append(placeholder[element])

        with open(filename, 'a+') as file:
            w = csv.writer(file)
            w.writerow(header)
            for element in range(len(data_input)):
                w.writerow(data_input[element])

    else:
        with open(filename, 'a+') as file:
            w = csv.writer(file)
            w.writerow(header)
            w.writerow(raw_input)


def recipe(fresh_id, fresh_comp, spent_id, spent_comp):
    """Takes recipes for fresh and spent fuel, split into lists of isotope names and compostions, and
    organizes them into a dictionary in the key:value format

    Parameters
    ----------
    fresh_id: list
        isotope names in fresh fuel: list
    fresh_comp: list
        isotope compositions in fresh fuel
    spent_id: list
        isotope compostions in spent fuel

    Returns
    -------
    fresh: dict
        key:value fresh recipe format
    spent: dict
        key:value spent recipe format

    """

    assert len(fresh_id) == len(
        fresh_comp), 'The lengths of fresh_id and fresh_comp are not equal'
    assert len(spent_id) == len(
        spent_comp), 'The lengths of spent_id and spent_comp are not equal'

    fresh = {}
    for element in range(len(fresh_id)):
        fresh.update({fresh_id[element]: fresh_comp[element]})

    spent = {}
    for element in range(len(spent_id)):
        spent.update({spent_id[element]: spent_comp[element]})

    return fresh, spent


def load_template(template):
    """Reads a jinja2 template.

    Parameters
    ----------
    template: str
        filename of the desired jinja2 templatefresh_id: list

    Returns
    -------
    """
    with open(template, 'r') as input_template:
        output_template = jinja2.Template(input_template.read())

    return output_template


def write_reactor(
        reactor_data,
        reactor_template,
        output_name='rendered-reactor.xml'):
    """Writes a csv file given the header, data, and the desired name of the
        csv file

    Parameters
    ----------
    reactor_data: pandas dataframe
        reactor data
    reactor_template: str
        name of reactor template file
    output_name: str
        filename of rendered reactor input - default: 'rendered-reactor.xml'

    Returns
    -------

    """
    if os.path.exists('./' + output_name) is True:
        os.remove(output_name)

    template = load_template(reactor_template)

    PWR_cond = {'assem_size': 33000, 'n_assem_core': 3, 'n_assem_batch': 1}

    BWR_cond = {'assem_size': 33000, 'n_assem_core': 3, 'n_assem_batch': 1}

    reactor_data = reactor_data.drop(['Country', 'Operator'], 'columns')
    reactor_data = reactor_data.drop_duplicates()

    if len(reactor_data) == 1:

        if reactor_data.iloc[0, :].loc['Type'] == 'PWR':
            reactor_body = template.render(
                reactor_name=reactor_data.iloc[0, :].loc['Reactor Name'],
                assem_size=PWR_cond['assem_size'],
                n_assem_core=PWR_cond['n_assem_core'],
                n_assem_batch=PWR_cond['n_assem_batch'],
                capacity=reactor_data.iloc[0, :].loc['Net Electric Capacity'])

            with open(output_name, 'a+') as output:
                output.write(reactor_body)

        elif reactor_data.iloc[0, :].loc['Type'] == 'BWR':
            reactor_body = template.render(
                reactor_name=reactor_data.iloc[0, :].loc['Reactor Name'],
                assem_size=BWR_cond['assem_size'],
                n_assem_core=BWR_cond['n_assem_core'],
                n_assem_batch=BWR_cond['n_assem_batch'],
                capacity=reactor_data.iloc[0, :].loc['Net Electric Capacity'])

            with open(output_name, 'a+') as output:
                output.write(reactor_body)

        else:
            print(
                'Warning: specifications of this reactor type have not been given.  Using placeholder values.')

            reactor_body = template.render(
                reactor_name=reactor_data.iloc[0, :].loc['Reactor Name'],
                assem_size=PWR_cond['assem_size'],
                n_assem_core=PWR_cond['n_assem_core'],
                n_assem_batch=PWR_cond['n_assem_batch'],
                capacity=reactor_data.iloc[0, :].loc['Net Electric Capacity'])

            with open(output_name, 'a+') as output:
                output.write(reactor_body)

    else:
        for element in range(len(reactor_data)):

            if reactor_data.iloc[element, :].loc['Type'] == 'PWR':
                reactor_body = template.render(
                    reactor_name=reactor_data.iloc[
                        element,
                        :].loc['Reactor Name'],
                    assem_size=PWR_cond['assem_size'],
                    n_assem_core=PWR_cond['n_assem_core'],
                    n_assem_batch=PWR_cond['n_assem_batch'],
                    capacity=reactor_data.iloc[
                        element,
                        :].loc['Net Electric Capacity'])

                with open(output_name, 'a+') as output:
                    output.write(reactor_body + "\n \n")

            elif reactor_data.iloc[element, :].loc['Type'] == 'BWR':
                reactor_body = template.render(
                    reactor_name=reactor_data.iloc[
                        element,
                        :].loc['Reactor Name'],
                    assem_size=BWR_cond['assem_size'],
                    n_assem_core=BWR_cond['n_assem_core'],
                    n_assem_batch=BWR_cond['n_assem_batch'],
                    capacity=reactor_data.iloc[
                        element,
                        :].loc['Net Electric Capacity'])

                with open(output_name, 'a+') as output:
                    output.write(reactor_body + "\n \n")

            else:
                print(
                    'Warning: specifications of this reactor type have not been given.  Using placeholder values.')

                reactor_body = template.render(
                    reactor_name=reactor_data.iloc[
                        element,
                        :].loc['Reactor Name'],
                    assem_size=PWR_cond['assem_size'],
                    n_assem_core=PWR_cond['n_assem_core'],
                    n_assem_batch=PWR_cond['n_assem_batch'],
                    capacity=reactor_data.iloc[
                        element,
                        :].loc['Net Electric Capacity'])

                with open(output_name, 'a+') as output:
                    output.write(reactor_body + "\n \n")
    return output_name


def write_region(
        reactor_data,
        deployment_data,
        region_template,
        output_name='rendered-region.xml'):
    """Renders the region portion of the Cyclus input file.

    Parameters
    ----------
    reactor_data: pandas dataframe
        reactor data
    deployment data: dict
        dictionary object giving values for initial deployment of each facility type,
        key names: n_mine, n_enrichment, n_reactor, n_repository
    region_template: str
        name of region template file
    output_name: str
        filenname of rendered region, default: 'rendered-region.xml'
    Returns
    -------
    rendered region input filename: str
        filename of rendered region

    """

    if os.path.exists('./' + output_name) is True:
        os.remove(output_name)

    template = load_template(region_template)

    reactor_data = reactor_data.drop(['Type'], 'columns')
    reactor_data = reactor_data.groupby(
        reactor_data.columns.tolist()).size().reset_index().rename(
        columns={
            0: 'Number Reactors'})

    country_reactors = {}
    countries_keys = reactor_data.loc[:, 'Country'].drop_duplicates()
    operator_keys = reactor_data.loc[:, 'Operator'].drop_duplicates()

    for country in countries_keys.tolist():

        country_operators = {}
        for operator in operator_keys.tolist():

            reactor_dict = {}
            data_loop = reactor_data.query(
                'Country == @country & Operator == @operator ')

            for element in range(len(data_loop)):
                reactor_dict[
                    data_loop.iloc[
                        element, :].loc['Reactor Name']] = [
                    data_loop.iloc[
                        element, :].loc['Number Reactors'], data_loop.iloc[
                        element, :].loc['Net Electric Capacity']]

            country_operators[operator] = reactor_dict

        country_reactors[country] = country_operators

    region_body = template.render(country_reactor_dict=country_reactors,
                                  countries_infra=deployment_data)

    with open(output_name, 'a+') as output:
        output.write(region_body)

    return output_name


def write_recipes(
        fresh,
        spent,
        recipe_template,
        output_name='rendered-recipe.xml'):
    """Renders the recipe portion of the Cyclus input file.

    Parameters
    ----------
    fresh: dict
        dictionary object, in id:comp format, containing the isotope names
        and compositions (in mass basis) for fresh fuel
    spent: dict
        dictionary object, in id:comp format, containing the isotope names
        and compositions (in mass basis) for spent  fuel
    recipe_template: str
        name of recipe template file
    output_name: str
        desired name of output file, default: 'rendered-recipe.xml'
    Returns
    -------

    """

    if os.path.exists('./' + output_name) is True:
        os.remove(output_name)

    template = load_template(recipe_template)

    recipe_body = template.render(
        fresh_fuel=fresh,
        spent_fuel=spent)

    with open(output_name, 'w') as output:
        output.write(recipe_body)

    return output_name


def write_main_input(
        simulation_parameters,
        reactor_file,
        region_file,
        recipe_file,
        input_template,
        output_name='rendered-main-input.xml'):
    """Renders the final, main input file for a Cyclus simulation.

    Parameters
    ----------
    simulation_parameters: list
        specifics of cyclus simulation, containing the data: [duration, start month, start year]
    reactor_file: str
        rendered reactor filename
    region_file: str
        rendered region filename
    recipe_file: str
        rendered recipe filename
    main_input_template: str
        name of main input template file
    output_name: str
        desired name of output file, default: 'rendered-main-input.xml'

    Returns
    -------
    """

    if os.path.exists('./' + output_name) is True:
        os.remove(output_name)

    template = load_template(input_template)

    with open(reactor_file, 'r') as reactorf:
        reactor = reactorf.read()

    with open(region_file, 'r') as regionf:
        region = regionf.read()

    with open(recipe_file, 'r') as recipef:
        recipe = recipef.read()

    main_input = template.render(
        duration=simulation_parameters[0],
        start_month=simulation_parameters[1],
        start_year=simulation_parameters[2],
        decay=simulation_parameters[3],
        reactor_input=reactor,
        region_input=region,
        recipe_input=recipe)

    with open(output_name, 'w') as output:
        output.write(main_input)


def import_csv(csv_file):
    """Imports the contents of a csv file as a dataframe.

    Parameters
    ----------
    csv_file: str
        name of the csv filename
    Returns
    -------
    reactor_data: pandas dataframe
        data contained in the csv file as a dataframe

    """
    reactor_data = (
        pd.read_csv(
            csv_file,
            names=[
                'Country',
                'Reactor Name',
                'Type',
                'Net Electric Capacity',
                'Operator'],
            skiprows=[0]))

    return reactor_data
