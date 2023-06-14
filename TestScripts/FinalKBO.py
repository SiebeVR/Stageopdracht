import argparse
import json
import requests

# Presets
SEARCH_BY_NAME_API_URL = 'https://api.cbe2json.be/byDenomination'
SEARCH_BY_NUMBER_API_URL = 'https://api.cbe2json.be/byCBE'
CLIENT_ID = 'd70edd1fa82f98d8'
SECRET_KEY = 'd663672e856c7ca8aefee6e0e108a2e5298f5c04bd118753708dd17cab62f714'

# Search by company, keeps giving ERROR 500, not sure why, I assume error on API side
# Should return a list of enterprise numbers with company name, user can pick from list which one is the actual target
# Then it searches by number with that number so that it returns the actual info of the company

def search_company_by_name(name):
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    payload = {
        'clientId': CLIENT_ID,
        'secretKey': SECRET_KEY,
        'data': {
            'denomination': name,
            "limit": 10,
            "offset": 0
        }
    }

    response = requests.post(SEARCH_BY_NAME_API_URL, headers=headers, data=json.dumps(payload))

    print(response.text)
    
    if response.status_code == 200:
        jsonresponse = response.json()
        companies = jsonresponse['result']['entities']
        if len(companies) == 0:
            print(f"No companies found with the name '{name}'")
        else:
            print(f"Found {len(companies)} companies with the name '{name}':")
            for i, company in enumerate(companies):
                print(f"{i+1}. {company['denomination']} ({company['enterpriseNumber']})")
            selected_company = int(input("Select a company (enter the number): "))
            enterprise_number = companies[selected_company-1]['enterpriseNumber']
            return enterprise_number
    else:
        print(f'Error: {response.status_code} - {response.reason}')

# Search by number does work, only possible if company number is searched manually

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
        print(jsonresponse)
        print('|------------------------------------------------------------------------------------------------------------|')
        print('| Company Number: ' + jsonresponse['enterpriseNumber'] + ' | Company Name: ' + jsonresponse['denominations'][0]['denomination'])
        print('|------------------------------------------------------------------------------------------------------------|')
        print('| Company E-mail: ' + jsonresponse['contacts'][0]['value'])
        print('|------------------------------------------------------------------------------------------------------------|')
        print('| Establishment number: ' + jsonresponse['establishments'][0]['establishmentNumber'] + ' | Establishment name: ' + jsonresponse['establishments'][0]['denominations'][0]['denomination'])
        print('|------------------------------------------------------------------------------------------------------------|')
        print('| Establishment address: ' + jsonresponse['addresses'][0]['zipcode'] + ', ' + jsonresponse['addresses'][0]['municipalityNL'] + ', ' + jsonresponse['addresses'][0]['streetNL'] + ' ' + jsonresponse['addresses'][0]['houseNumber'])
        print('|------------------------------------------------------------------------------------------------------------|')
    else:
        print(f'Error: {response.status_code} - {response.reason}')

parser = argparse.ArgumentParser(description='Search for companies by name or number.')
parser.add_argument('-N', '--name', help='Search for companies by name.')
parser.add_argument('-n', '--number', help='Search for companies by number.')
args = parser.parse_args()

if args.name:
    print('Searching by company name')
    enterprisenumber = search_company_by_name(args.name)
    search_company_by_number(enterprisenumber)
elif args.number:
    print('Searching by CBE')
    search_company_by_number(args.number)
else:
    print('Error: You must provide either a --name or a --number to search for.')