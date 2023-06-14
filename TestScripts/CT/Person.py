##Imports
import os
import csv
import argparse
import re
import shutil
import subprocess
import sys
import time
import requests
from datetime import datetime, timedelta
import pandas as pd
from bs4 import BeautifulSoup

###Create temporary folder
os.makedirs("temp", exist_ok=True)

###Start variables
person_info = {}
directory =  'path/to/csv/files'
df_list = []

###Add the option to use the script with parameters
parser = argparse.ArgumentParser(description='Perform OSINT on a person or company')
parser.add_argument('-n', '--name', help='Name of person')
parser.add_argument('-e', '--email', help='Email of person')
args = parser.parse_args()

###Define OSINT tools and parameters
####For person
spiderfoot = 'spiderfoot -s {name} -u all'
sherlock = 'sherlock {name} --nsfw --csv'
blackbird = 'blackbird.py -u {name}'
haveibeenpwned = 'haveibeenpwned' ##API

####For company


##Functions
def run_tool(tool, args):
    # code to run tool with arguments
    output = subprocess.check_output([tool, args])
    return output

###Get person by name
def get_person_by_name(name):
    output = subprocess.check_output(run_tool(spiderfoot, '-s {name} -u all'))
    person_info = pd.DataFrame([line.split() for line in output.decode().splitlines()],columns=["col1", "col2", "col3"])
    return all_person_info
    
###Get person by email
def get_person_by_email(email):
    output = subprocess.check_output(["my_tool", "arg1", "arg2"])
    person_info = pd.DataFrame([line.split() for line in output.decode().splitlines()],columns=["col1", "col2", "col3"])
    return all_person_info

###Save person results
def save_person_results(person_info):
    with open('results/person/{person}/{person}.csv', 'w', newline='') as file:
        # Create a CSV writer object
        writer = csv.writer(file)
        # Write the data to the file row by row
        for row in person_info:
            writer.writerow(row) 
    return


##Main
if sys.args[1] in ["-n", "-e", "--name", "--email"]:
    if sys.args[1] == "-n" or sys.args[1] == "--name":
        person_info = get_person_by_name(sys.args[2])
        save_person_results(person_info)
    elif sys.args[1] == "-e" or sys.args[1] == "--email":
        person_info = get_person_by_email(sys.args[2])
        save_person_results(person_info)
else:
    ###Check if first parameter is valid
    print("Invalid parameter")
    sys.exit(1)
###Check if second parameter is valid
if sys.args[2] == "":
    print("Invalid parameter")
    sys.exit(1)

###Running the tools and saving the results



##Saving and combining results
###Make directory results, with in that a directory person and a directory company
os.makedirs("results", exist_ok=True)
os.makedirs("results/person", exist_ok=True)

###Make directory for each company by name of the company in company directory
os.makedirs("results/person/{person}", exist_ok=True)

###Write results to CSV in the correct folder
if sys.args[1] == "-e" or sys.args[1] == "-n" or sys.args[1] == "--email" or sys.args[1] == "--name":
    ###Save person to CSV as {person_name}.csv in the person directory
    for file in os.listdir(directory):
        if file.endswith(".csv"):
            # read the csv file into a dataframe
            df = pd.read_csv(os.path.join(directory, file))
            # append the dataframe to the list
            df_list.append(df)
            print('Saving results')
    combined_df = pd.concat(df_list)
    combined_df.to_csv('combined.csv', index=False)
else:
   print('No need to save results')