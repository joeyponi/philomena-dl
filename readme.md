# Philomena-DL: Bulk Image Downloader
This is a simple script to bulk-download images from websites running the Philomena Imageboard software (such as Derpibooru and Furbooru)

# Dependencies
- Phython 3
- The following modules:
  - Requests
  - Pathvalidate

# Installation
Install Python 3

Install the dependencies

`pip install requests`

`pip install pathvalidate`

Move/copy config.json.example to config.json, then edit it to add your API key. If you're downloading images from a site other than Derpibooru, change the "site" value to the appropriate site URL without the trailing slash.

# Using the script
Simply run

`python philomena_dl.py`

Enter your search query, hit enter, and if all goes well, it should start downloading images