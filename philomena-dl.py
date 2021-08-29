# Import libraries
import json
import urllib.parse
import urllib.request
import math
import os
import pathvalidate
import time

# Load config
config = json.load(open('config.json'))

# Get search string
search_string = input('Enter your search query: ')

# Search URL
search_url = config['site'] + '/api/v1/json/search/images?key=' + config['key'] + '&perpage=50&q=' + urllib.parse.quote(search_string)

# Generate search request
search_request = urllib.request.Request(search_url,data=None,headers={'User-Agent': 'Philomena Bulk Image Downloader'})

# Get result
search_response = urllib.request.urlopen(search_request).read()
search_data = json.loads(search_response)

# Determine results count
results_count = search_data['total']
results_pages = math.ceil(results_count/50)

# Exit script if no results
if(results_count == 0):
    print('No results found for your query, sorry')
    exit()

# Inform user of results count
print('Found ' + str(results_count) + ' images, producing ' + str(results_pages) + ' pages of results')

# Create results folders
folder_name = pathvalidate.sanitize_filename(search_string)
downloads_folder = './downloads/'
downloads_json_folder = downloads_folder + 'json/'
try:
    os.makedirs(downloads_folder)
except FileExistsError:
    print("Downloads directory already exists.")
try:
    os.makedirs(downloads_json_folder)
except FileExistsError:
    print("JSON directory already exists.")

# Loop through each page
counter = 1
for page in range(0,results_pages):
    # Generate a search URL for this page of results
    page_search_url = config['site'] + '/api/v1/json/search/images?key=' + config['key'] + '&perpage=50&page=' + str(page + 1) + '&q=' + urllib.parse.quote(search_string)

    # Generate search request for page
    page_search_request = urllib.request.Request(page_search_url,data=None,headers={'User-Agent': 'Philomena Bulk Image Downloader'})

    # Get responses for page
    page_search_response = urllib.request.urlopen(page_search_request).read()
    page_search_data = json.loads(page_search_response)
    time.sleep(.1)
    
    # Loop through each image
    for image in page_search_data['images']:
        
        # Output status
        print('Downloading ' + str(image['id'])  + ' (' + str(counter) + ' of ' + str(results_count) + ')')

        # Set file paths
        if(image['format'] == 'svg'):
            image_file_path = downloads_folder + str(image['id']) + '.png'
        else:
            image_file_path = downloads_folder + str(image['id']) + '.' + image['format']
        image_json_path = downloads_json_folder + str(image['id']) + '.json'

        # Download the image
        urllib.request.urlretrieve(image['representations']['full'],image_file_path)

        # Output metadata
        with open(image_json_path, 'w') as outfile:
            json.dump(image,outfile)

        time.sleep(.1)
        # Increment the image counter
        counter += 1