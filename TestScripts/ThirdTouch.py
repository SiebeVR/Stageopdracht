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

###Add the option to use the script with parameters
parser = argparse.ArgumentParser(description='Perform OSINT on a person or company')
parser.add_argument('-t', '--type', required=True, choices=['person', 'company'], help='Type of search (person or company)')
parser.add_argument('-n', '--name',  help='Name of person')
parser.add_argument('-c', '--company', help='Name of company')
parser.add_argument('-e', '--email', help='Email of person')
parser.add_argument('-u', '--url', help='URL of company website')
args = parser.parse_args()


###Create Folders
if not os.path.exists("results"):
    os.mkdir("results")
if not os.path.exists("results/company"):
    os.mkdir("results/company")
if not os.path.exists("results/person"):
    os.mkdir("results/person")

###Define OSINT tools and parameters

####For person
spiderfoot = 'spiderfoot -s {name} -u all'
#dorkscout = 'dorkscout.py'
sherlock = 'sherlock {name} --nsfw --csv'
blackbird = 'blackbird.py -u {name}'
#whatsmyname = 'whatsmyname.py'
haveibeenpwned = 'haveibeenpwned' ##API

####For company
theharvester = 'theharvester.py -d {company} -b all'
#recon_ng = 'recon-cli '
pagodo = 'python3 pagodo.py -d {url} -g /pagodo/dorks/all_google_dorks.txt'
#infoga = 'infoga.py'
#nmap = 'nmap'
crunchbase = 'crunchbase.py'
zoominfo = 'zoominfo.py'


##Functions
###Get person by name
def search_person_name(name):
    
###Get person by email
def search_person_email(email):

###Get company by name
def search_company_name(name):

###Get company by url
def search_company_url(url):

##Main
###Check if first parameter is valid
if sys.argv[1] not in ["-c", "-u", "-n", "-e"]:
    print("Usage: python osint.py [-c <company name> | -u <company url> | -n <person name> | -e <person email>]")
    exit()
##Saving

###Make directory for each company by name of the company in company directory

###Save company information to CSV as [company_name].csv in the company directory

###Save company employees information to CSV as [company_name]_employees.csv in the company directory

###Save person to CSV as [person_name].csv in the person directory