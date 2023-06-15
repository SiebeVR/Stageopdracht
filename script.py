import argparse
import json
import requests
import os
import sys
import pandas as pd
from contextlib import contextmanager
from contextlib import redirect_stdout, redirect_stderr
from pymongo import MongoClient
from APIDNSD.dnsdumpster.DNSDumpsterAPI import DNSDumpsterAPI

# Presets
SEARCH_BY_NAME_API_URL = 'https://api.cbe2json.be/byDenomination'
SEARCH_BY_NUMBER_API_URL = 'https://api.cbe2json.be/byCBE'
CLIENT_ID = 'd70edd1fa82f98d8'
SECRET_KEY = '*****'
DEHASHED_API_URL = 'https://api.dehashed.com/search'
DEHASHED_API_KEY = ''
DEHASHED_OWN_EMAIL = 'feesttent123@gmail.com'

try:
    client = MongoClient('mongodb://localhost:27017/')
    db = client['oPInt']  # Replace with your database name
    collection_oPInt = db['results']  # Replace with your collection name
    print("Connected to MongoDB successfully!")

    @contextmanager
    def suppress_stdout():
        with open(os.devnull, "w") as devnull:
            old_stdout = sys.stdout
            sys.stdout = devnull
            try:  
                yield
            finally:
                sys.stdout = old_stdout

    def search_sherlock(name):
        command = f"python3 /home/kali/oPInt/tools/sherlock/sherlock/sherlock.py {name} --print-found --nsfw | grep https* > {name}_s.csv"
        with suppress_stdout():
            os.system(command)

    def search_blackbird(name):
        command = f"python3 /home/kali/oPInt/tools/blackbird/blackbird.py -u {name} | grep 200 > {name}_b.csv"
        with suppress_stdout():
            os.system(command)

    def search_dehashed_by_name(name):
        command = f"curl 'https://api.dehashed.com/search?query=username:{name}&size=10000' \
                    -u {DEHASHED_OWN_EMAIL}:{DEHASHED_API_KEY} \
                    -H 'Accept: application/json'"
        with suppress_stdout():
            os.system(command)

    def search_dehashed_by_email(email):
        command = f"curl 'https://api.dehashed.com/search?query=email:{email}&size=10000' \
                    -u {DEHASHED_OWN_EMAIL}:{DEHASHED_API_KEY} \
                    -H 'Accept: application/json'"
        with suppress_stdout():
            os.system(command)    

    def search_dnsdumpsterAPI(domain):
        res = DNSDumpsterAPI({'verbose': True}).search("'"+ domain +"'")
        print(res)

    def search_theharvester(domain):
        command = f"theHarvester -d {domain} -b all"
        with suppress_stdout():
            os.system(command)

    def search_dnsrecon(domain):
        command = f"dnsrecon -d {domain}"
        with suppress_stdout():
            os.system(command)

    def search_photon(domain):
        command = f"python3 /home/kali/oPInt/tools/Photon/photon.py -u {domain}"
        with suppress_stdout():
            os.system(command)

    def search_crosslinked(domain):
        command = f"crosslinked {domain} -f '{{first}}.{{last}}@{domain}'"
        with suppress_stdout():
            os.system(command)

    def search_person_by_name(name):
        search_sherlock(name)
        search_blackbird(name)
        #search_dehashed_by_name(name)
        result1 = pd.read_csv(name +'_b.csv')
        result2 = pd.read_csv(name +'_s.csv')
        combined = pd.concat([result1,result2], ignore_index=True)
        combined.to_csv('Searched_by_name_'+name+'.csv', index=False)
        command = (f'rm ' + name+'*')
        documents = combined.to_dict('records')
        collection_oPInt.insert_many(documents)
        with open('Searched_by_name_'+name+'.csv', 'r+') as file:
            lines = file.readlines()
            lines = [line.replace(',', '').replace('+', '').replace('[', '').replace(']', '').replace('-','').replace('200 OK', '').replace('account found',':') for line in lines]
            filtered_lines = [line for line in lines if not any(word in line for word in ['mastodon', 'opennet', 'opennet','mstdn','chaos','jeuxvideo','OurDJTalk','Salon24'])]
            file.seek(0)
            file.truncate()
            file.writelines(filtered_lines)
        file.close()
        os.system(command)

    def search_person_by_email(email):
        search_sherlock(email)
        search_blackbird(email)
        #search_dehashed_by_email(email)
        result1 = pd.read_csv(email +'_b.csv')
        result2 = pd.read_csv(email +'_s.csv')
        combined = pd.concat([result1,result2], ignore_index=True)
        combined.to_csv('Searched_by_email_'+email+'.csv', index=False)
        command = (f'rm ' + email+'*')
        documents = combined.to_dict('records')
        collection_oPInt.insert_many(documents)
        with open('Searched_by_email_'+email+'.csv', 'r+') as file:
            file.replace(',','')
            file.replace('+','')
            file.replace('[','')
            file.replace(']','')
            lines = file.readlines()
            filtered_lines = [line for line in lines if not any(word in line for word in ['mastodon','opennet','mstdn','chaos','jeuxvideo'])]
            file.writelines(filtered_lines)
        file.close()
        os.system(command)

    #Search for company by number
    def search_company_by_number(number):
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }
        payload = {
            'clientId': CLIENT_ID,
            'secretKey': SECRET_KEY, 
            'data': {
                'cbe': number
            }
        } 
        response = requests.post(SEARCH_BY_NUMBER_API_URL, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            jsonresponse = response.json()
            print('-----------------------------------DEBUG----------------------------------------')
            print(jsonresponse)
            print('---------------------------------End of DEBUG----------------------------------------------------')

            company_number = jsonresponse.get('enterpriseNumber', '')
            company_name = jsonresponse.get('denominations', [{}])[0].get('denomination', '')
            contacts = jsonresponse.get('contacts', [{}])
            company_email = contacts[0].get('value') if len(contacts) > 0 else None
            if company_email == None:
                company_email = 'Not found'

            establishments = jsonresponse.get('establishments')
            if establishments:
                establishment_number = establishments[0].get('establishmentNumber', '')
                establishment_name = establishments[0].get('denominations')
                if establishment_name == []:
                    establishment_name = 'Not found'
                else:
                    establishment_name = establishments[0].get('denominations', [{}])[0].get('denomination', '')
                establishment_zipcode = establishments[0].get('addresses', [{}])[0].get('zipcode', '')
                establishment_city = establishments[0].get('addresses', [{}])[0].get('municipalityNL', '')
                establishment_street = establishments[0].get('addresses', [{}])[0].get('streetNL', '')
                establishment_housenumber = establishments[0].get('addresses', [{}])[0].get('houseNumber', '')
            else:
                establishment_name = 'Not found'
                establishment_number = 'Not found'
                establishment_name = 'Not found'
                establishment_zipcode = 'Not found'
                establishment_city = 'Not found'
                establishment_street = 'Not found'
                establishment_housenumber = 'Not found'
                print('Nothing found')
            print('|------------------------------------------------------------------------------------------------------------|')
            print('| Company Number: '+ str(company_number) +' | Company Name: '+ str(company_name))
            print('|------------------------------------------------------------------------------------------------------------|')
            print('| Company E-mail: '+ str(company_email))
            print('|------------------------------------------------------------------------------------------------------------|')
            print('| Establishment number: '+ str(establishment_number) +' | Establishment name: '+ str(establishment_name))
            print('|------------------------------------------------------------------------------------------------------------|')
            print('| Establishment address: '+ str(establishment_zipcode) +', '+ str(establishment_city) +', '+ str(establishment_street) +' '+ str(establishment_housenumber))
            print('|------------------------------------------------------------------------------------------------------------|')
            collection_oPInt.insert_one(jsonresponse)
        else:
            print(f'Error: {response.status_code} - {response.reason}')

    def search_company_by_domain(domain):
        combined = []
        with suppress_stdout():
            search_crosslinked(domain)
            search_theharvester(domain)
            search_photon(domain)
            search_dnsrecon(domain)
            search_dnsdumpsterAPI(domain)
            with open("./names.txt", 'r+') as fp:
                rows = fp.readlines()
                fp.seek(0)
                fp.truncate()
                fp.writelines(rows[1:])
                combined.extend(fp)
        # documents = combined.to_dict('records')
        # collection_oPInt.insert_many(documents)

    def main():
        parser = argparse.ArgumentParser(description='Search for information about a person or company.')
        parser.add_argument('search_term', type=str, help='The name or email of the person or the company number or domain to search for.')
        parser.add_argument('--person-name', dest='is_person_name', action='store_true', help='Search for a person by name.')
        parser.add_argument('--person-email', dest='is_person_email', action='store_true', help='Search for a person by email')
        parser.add_argument('--company-number', dest='is_company_number', action='store_true', help='Search for a company by number.')
        parser.add_argument('--company-domain', dest='is_company_domain', action='store_true', help='Search for a company by domain.')
        parser.add_argument('--FR', dest='full_research', action='store_true', help='Do a full research of the found info (Only possible when using company searches)')

        args = parser.parse_args()

        if args.is_person_name:
            print('Searching for the chosen name.')
            with suppress_stdout():
                search_person_by_name(args.search_term)
            print('Saved results in Searched_by_name_'+ args.search_term+'.csv')
        
        elif args.is_person_email:
            print('Searching for the chosen email.')
            with suppress_stdout():
                search_person_by_email(args.search_term)
            print('Saved results in Searched_by_email_'+ args.search_term+'.csv')

        elif args.is_company_number:
            print('Searching by company number')
            search_company_by_number(args.search_term)
            if args.full_research:
                print('Researching further')
        elif args.is_company_domain:
            print('Searching for company domain.')
            with suppress_stdout():
                search_company_by_domain(args.search_term)
            if args.full_research:
                print('Researching found employees of chosen company')
                print('This might take a while')
                with open('./names.txt','r') as file:
                    lijst = file.readlines()
                    print('list found')
                    print(lijst)
                    for i in lijst:
                        print(i)
                        email = i.strip()
                        print(email)
                        print('Searching')
                        search_person_by_email(email)
        else:
            print('Please specify whether to search for a person by name or email or a company by number or domain. (Use -h for help)')

    if __name__ == '__main__':
        main()
    
except Exception as e:
    print('failed')
