import requests
import json
import argparse
import subprocess
import os
import csv

QUERY = "example@example.com"

# Define the API endpoints and query parameters for the OSINT tools you want to use
SHERLOCK_API = "https://api.github.com/repos/sherlock-project/sherlock/contents/sherlock/resources/data.json"
BLACKBIRD_API = "https://app.blackbird.ai/api/v1/search/"
SPIDERFOOT_API = "http://localhost:5001/api/scan"
HIBP_API_URL = "https://haveibeenpwned.com/api/v3/"


# Define your API keys and other parameters
BLACKBIRD_KEY = "your-blackbird-api-key"
QUERY = "your-search-query"
HIBP_API_KEY = "your-haveibeenpwned-api-key"


# Make API requests to the OSINT tools and collect the data
sherlock_response = requests.get(SHERLOCK_API)
blackbird_response = requests.post(BLACKBIRD_API, headers={"Authorization": BLACKBIRD_KEY}, json={"query": QUERY})
haveibeenpwned_response = requests.get(f"{HIBP_API_URL}{QUERY}", headers={"hibp-api-key": HIBP_API_KEY})
spiderfoot_response = requests.post(SPIDERFOOT_API, json={"scan": "Scan", "module": "search_osint", "parameters": {"query": QUERY}})

# Convert the responses to JSON and save them to a file
with open("data.json", "w") as f:
    json.dump({
        "sherlock": sherlock_response.json(),
        "blackbird": blackbird_response.json(),
        "haveibeenpwned": haveibeenpwned_response.json(),
        "spiderfoot": spiderfoot_response.json()
    }, f)

# Read the data from the file and perform the necessary checks
with open("data.json", "r") as f:
    data = json.load(f)

# Verify the data returned by Sherlock
if sherlock_response.status_code == 200:
    results = data["sherlock"]
    if len(results) > 0:
        print("Sherlock returned valid results.")
    else:
        print("Sherlock returned no results. Check your query.")
else:
    print("Sherlock API error.")

# Verify the data returned by Blackbird
if blackbird_response.status_code == 200:
    results = data["blackbird"]["results"]
    if len(results) > 0:
        print("Blackbird returned valid results.")
    else:
        print("Blackbird returned no results. Check your query.")
else:
    print("Blackbird API error.")

# Define the API endpoint for the "breachedaccount" API and send a GET request with the query and headers
api_endpoint = f"{HIBP_API_URL}breachedaccount/{QUERY}"
response = requests.get(api_endpoint, headers={"hibp-api-key": HIBP_API_KEY})

# Check the status code of the response
if response.status_code == 200:
    # Convert the response to JSON format
    results = response.json()
    # Print the list of breached sites and the number of times the email or username was found in each breach
    for result in results:
        print(f"Breached Site: {result['Name']}")
        print(f"Breached Records: {result['BreachDate']} - {result['PwnCount']} times")
        print(f"Data Classes: {result['DataClasses']}")
        print(f"Description: {result['Description']}\n")
    # Save the results to a file
    with open("hibp_results.json", "w") as f:
        json.dump(results, f)
else:
    print(f"API error: {response.status_code}")

# Verify the data returned by SpiderFoot
if spiderfoot_response.status_code == 200:
    results = data["spiderfoot"]["results"]["search_osint"]["summary"]["results"]
    if len(results) > 0:
        print("SpiderFoot returned valid results.")
    else:
        print("SpiderFoot returned no results. Check your query.")
else:
    print("SpiderFoot API error.")
