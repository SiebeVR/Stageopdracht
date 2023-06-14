import os
import csv
import argparse
from datetime import datetime, timedelta

def search_person_by_name(name):
    # Search for people with the same name
    osint_tools = [
        'theharvester -d {0} -l 100 -b all'.format(name),
        'sherlock {0}'.format(name)
    ]

    results = []

    # Run each tool and extract the relevant information
    for tool in osint_tools:
        output = os.popen(tool).read()

        if 'No results found' not in output:
            # Extract the relevant information from the output
            if tool.startswith('theharvester'):
                emails = set()
                addresses = set()
                phone_numbers = set()
                social_media_accounts = set()
                company = 'unknown'
                password_breaches = []
                password_breaches_recent = []

                for line in output.splitlines():
                    if '@' in line:
                        emails.add(line.strip())

                    if 'address:' in line.lower():
                        address = line.split('address:')[1].strip()
                        addresses.add(address)

                    if 'phone:' in line.lower():
                        phone_number = line.split('phone:')[1].strip()
                        phone_numbers.add(phone_number)

                results.append({
                    'name': name,
                    'emails': ', '.join(emails),
                    'addresses': ', '.join(addresses),
                    'phone_numbers': ', '.join(phone_numbers),
                    'social_media_accounts': ', '.join(social_media_accounts),
                    'company': company,
                    'password_breaches': ', '.join(password_breaches),
                    'password_breaches_recent': ', '.join(password_breaches_recent)
                })
            elif tool.startswith('sherlock'):
                for line in output.splitlines():
                    if '|' in line:
                        site, url = line.split('|')
                        social_media_accounts.add(site.strip())

                        if 'twitter.com' in url:
                            username = url.split('/')[-1].strip()
                            output = os.popen('twint -u {0} -j'.format(username)).read()

                            if '{"name":"' in output:
                                data = json.loads(output.splitlines()[0])
                                company = data.get('bio', 'unknown')
                                results[-1]['company'] = company

                        if 'haveibeenpwned.com' in url:
                            email = url.split('/')[-1].strip()
                            output = os.popen('h8mail target {0} --all'.format(email)).read()

                            if 'Breach: ' in output:
                                breach = output.split('Breach: ')[1].strip()
                                password_breaches.append(breach)

                            if 'Leak: ' in output:
                                leak = output.split('Leak: ')[1].strip()
                                password_breaches.append(leak)

                            if 'Password: ' in output:
                                password = output.split('Password: ')[1].strip()
                                password_breaches.append(password)

                            if 'Last paste: ' in output:
                                last_paste_str = output.split('Last paste: ')[1].split(' ago')[0].strip()
                                last_paste_time = datetime.strptime(last_paste_str, '%Y-%m-%d %H:%M:%S.%f')
                                if datetime.now() - last_paste_time <= timedelta(days=365):
                                    password_breaches_recent.append('Yes')

    return results

def search_person_by_email(email):
    # Search for information on a person using an email address
    osint_tools = [
        'h8mail target {0} --all'.format(email),
        'theharvester -d {0} -l 100 -b all'.format(email),
        'sherlock {0}'.format(email),
        'metagoofil -d {0} -t doc,pdf -l 100 -o output'.format(email)
    ]

    results = []

    # Run each tool and extract the relevant information
    for tool in osint_tools:
        output = os.popen(tool).read()

        if 'No results found' not in output:
            # Extract the relevant information from the output
            if tool.startswith('h8mail'):
                password_breaches = []
                password_breaches_recent = []

                for line in output.splitlines():
                    if 'Breach: ' in line:
                        breach = line.split('Breach: ')[1].strip()
                        password_breaches.append(breach)

                    if 'Leak: ' in line:
                        leak = line.split('Leak: ')[1].strip()
                        password_breaches.append(leak)

                    if 'Password: ' in line:
                        password = line.split('Password: ')[1].strip()
                        password_breaches.append(password)

                    if 'Last paste: ' in line:
                        last_paste_str = line.split('Last paste: ')[1].split(' ago')[0].strip()
                        last_paste_time = datetime.strptime(last_paste_str, '%Y-%m-%d %H:%M:%S.%f')
                        if datetime.now() - last_paste_time <= timedelta(days=365):
                            password_breaches_recent.append('Yes')

                results.append({
                    'name': 'unknown',
                    'email': email,
                    'addresses': 'unknown',
                    'phone_numbers': 'unknown',
                    'social_media_accounts': 'unknown',
                    'company': 'unknown',
                    'password_breaches': ', '.join(password_breaches),
                    'password_breaches_recent': ', '.join(password_breaches_recent)
                })
            elif tool.startswith('theharvester'):
                emails = set()
                addresses = set()
                phone_numbers = set()
                social_media_accounts = set()
                company = 'unknown'
                password_breaches = []
                password_breaches_recent = []

                for line in output.splitlines():
                    if '@' in line:
                        emails.add(line.strip())

                    if 'address:' in line.lower():
                        address = line.split('address:')[1].strip()
                        addresses.add(address)

                    if 'phone:' in line.lower():
                        phone_number = line.split('phone:')[1].strip()
                        phone_numbers.add(phone_number)

                results.append({
                    'name': 'unknown',
                    'email': email,
                    'addresses': ', '.join(addresses),
                    'phone_numbers': ', '.join(phone_numbers),
                    'social_media_accounts': ', '.join(social_media_accounts),
                    'company': company,
                    'password_breaches': ', '.join(password_breaches),
                    'password_breaches_recent': ', '.join(password_breaches_recent)
                })
            elif tool.startswith('sherlock'):
                for line in output.splitlines():
                    if '|' in line:
                        site, url = line.split('|')
                        social_media_accounts.add(site.strip())

                        if 'twitter.com' in url:
                            username = url.split('/')[-1].strip()
                            output = os.popen('twint -u {0} -j'.format(username)).
