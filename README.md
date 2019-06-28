# scrape_bund
A simple scraper to get the German-language 1st of August (National holiday) speeches from admin.ch

Almost every line in the python script is annotated. Can be easily adapted to other static homepages.
It uses xpath to identify elements.
Necessary libraries that need to be installed are lxml, requests, pandas

First step: (skip if these packages are already installed)
$pip install lxml
$pip install requests
$pip install pandas

Second step:
run scrape_bund.py from the director where it is located with:
$python3 scrape_bund.py

It will create a .csv file with your data in the same directory.
