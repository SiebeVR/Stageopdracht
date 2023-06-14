import requests
import json

# Function to search for a person by name
def search_person_by_name(name):
    url = f"https://api.nameapi.org/rest/v5.3/person/nameparser?apiKey=<YOUR_API_KEY>&name={name}"
    response = requests.get(url)
    data = json.loads(response.text)
    persons = []
    for person in data["persons"]:
        person_details = {}
        person_details["name"] = person["fullName"]
        person_details["email"] = "unknown"
        person_details["address"] = "unknown"
        person_details["phone"] = "unknown"
        person_details["social_media"] = "unknown"
        person_details["company"] = "unknown"
        person_details["password_breaches"] = "unknown"
        person_details["recent_password_breaches"] = "unknown"
        persons.append(person_details)
    return persons

# Function to search for a person by email
def search_person_by_email(email):
    url = f"https://api.hunter.io/v2/email-finder?domain=<YOUR_DOMAIN>&api_key=<YOUR_API_KEY>&email={email}"
    response = requests.get(url)
    data = json.loads(response.text)
    persons = []
    if data["data"]["result"] == "deliverable":
        person_details = {}
        person_details["name"] = data["data"]["first_name"] + " " + data["data"]["last_name"]
        person_details["email"] = email
        person_details["address"] = "unknown"
        person_details["phone"] = "unknown"
        person_details["social_media"] = "unknown"
        person_details["company"] = "unknown"
        person_details["password_breaches"] = "unknown"
        person_details["recent_password_breaches"] = "unknown"
        persons.append(person_details)
    return persons

# Function to search for a company by name
def search_company_by_name(name):
    url = f"https://api.hunter.io/v2/domain-search?api_key=<YOUR_API_KEY>&domain={name}.com"
    response = requests.get(url)
    data = json.loads(response.text)
    employees = []
    if data["meta"]["results"]["total"] > 0:
        for employee in data["data"]["emails"]:
            employee_details = {}
            employee_details["name"] = employee["value"]
            employee_details["email"] = employee["value"]
            employee_details["address"] = "unknown"
            employee_details["phone"] = "unknown"
            employee_details["social_media"] = "unknown"
            employee_details["company"] = name
            employee_details["password_breaches"] = "unknown"
            employee_details["recent_password_breaches"] = "unknown"
            employees.append(employee_details)
    return employees

# Function to search for a company by domain
def search_company_by_domain(domain):
    url = f"https://api.hunter.io/v2/domain-search?api_key=<YOUR_API_KEY>&domain={domain}"
    response = requests.get(url)
    data = json.loads(response.text)
    employees = []
    if data["meta"]["results"]["total"] > 0:
        for employee in data["data"]["emails"]:
            employee_details = {}
            employee_details["name"] = employee["value"]
            employee_details["email"]= employee["value"]
            employee_details["address"] = "unknown"
            employee_details["phone"] = "unknown"
            employee_details["social_media"] = "unknown"
            employee_details["company"] = domain
            employee_details["password_breaches"] = "unknown"
            employee_details["recent_password_breaches"] = "unknown"
            employees.append(employee_details)
    return employees
