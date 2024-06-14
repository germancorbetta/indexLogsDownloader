# Description: This python3 script is meant to downlaod files from Index sites with some frequency
# Note: this script considers that the logs are present in an "Index" format within a "/logs" folder of a domain, but this could be changed

# Libraries (no need to install any custom Python library, all of these comes from the python3 basic installation)
import urllib.request
import re
import os
import time

# Configuration
sites = ["www.google.com","www.hotmail.com"]
exceptionNames = ["mule_agent","mule-app-default","mule-domain-default"]
downloadFolder = "C:\\Users\\german\\Documents\\MuleLogs"
delayMin = 15

# Required functions
# Function to get all HTML links from Index site
def extract_links(url):
    try:
        with urllib.request.urlopen(url) as response:
            html_content = response.read().decode('utf-8')
        links = re.findall(r'href=["\'](.*?)["\']', html_content)
        links = [link if "://" in link else urllib.parse.urljoin(url, link) for link in links]

        return links    
    except Exception as e:
        print("Error: " + e)
        return []

# Function to filter links and remove some files (based on the "exceptionNames" array variable)
def filterLinks(links):
    responseLinks = []
    for link in links:
        if link.endswith(".log"):
            if "2024" not in link:
                exceptionCheck = True
                for item in exceptionNames:
                    if item in link:
                        exceptionCheck = False
                if exceptionCheck == True:
                    responseLinks.append(link)
    return responseLinks

# Download file from environment in a folder
def download_file(link, folder, env):
    filename = os.path.join(folder, env + "-" + os.path.basename(link))
    try:
        with urllib.request.urlopen(link) as response, open(filename, 'wb') as out_file:
            data = response.read()
            out_file.write(data)
    except Exception as e:
        print("Exception: ", e)

# Start processing
print("Starting process")

while True:
    for site in sites:
        rawlinks = extract_links("https://" + site + "/logs/")
        links = filterLinks(rawlinks)
        for link in links:
            print("Downloading " + os.path.basename(link) + " from " + site)
            download_file(link, downloadFolder, site)

    print("Waiting for " + str(delayMin) + " minutes to run again...")
    time.sleep(delayMin * 60)
