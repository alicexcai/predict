import sqlite3
import pandas as pd

# SETUP #

db = sqlite3.connect('project.sqlite')
cursor = db.cursor()

# Create a table to store project metadata
cursor.execute('''CREATE TABLE meta (
               name TEXT, 
               timeline TEXT, 
               params TEXT, 
               notes TEXT,
               )''')

cursor.execute('''INSERT INTO meta (name, timeline, params, notes)
               VALUES('Prediction Market Simulation', '12/2021', '[liquidity, num_rounds, outcomes, agents_list, mechanism, i_shares]', 'CS136 Final Project',
               )''')

# Create a table to store metadata about the experiments
cursor.execute('''CREATE TABLE experiments (
               id INTEGER PRIMARY KEY NOT NULL, 
               name TEXT, 
               timestamp TEXT, 
               params_const BLOB,
               params_tested BLOB, 
               experiment_key TEXT,
               notes TEXT,
               )''')

'''Autofill id column with 1, 2, 3, ...'''

db.commit()  # Commit changes to the database

# ON EXPERIMENT #

'''
Experiment creation: name, params_tested, params_const, results_primary, results_full

Outputs: experiment_data -> experiment table, full_data -> individual tables, referenced in experiment table

Input post-experiment: notes, metric?
Processing: auto-generate timestamp
'''

# Create a table to store metadata about the experiments
experiment_name = input('Experiment name: ')

# Use list comprehension to expand the list of the parameters tested
cursor.execute('''CREATE TABLE experiment_data{} (
               params_const TEXT, 
               params_tested TEXT, 
               results_primary TEXT,
               full_results_link DATAFRAME )''', experiment_name)