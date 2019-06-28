#!/usr/bin/env python
#title           :scrape_bund.py
#description     :Scrapes "1. August" speeches from admin.ch.
#author          :Thomas C. Messerli
#date            :20190628
#version         :1.0
#usage           :python3 scrape_bund.py
#notes           :issues: speeches from some years have a different title format, therefore the year will
#                  not return a year --> needs to be cleaned up in post-processing
#python_version  :3.6.3  
##########################################################################################
#lxml is a library to process html and xml
from lxml import html
#The requests library is the de facto standard for making HTTP requests in Python
import requests
#Pandas is a  library written for data manipulation and analysis
import pandas as pd
#Define the name of the ouput csv
outcsv="Augustreden.csv"

#function to process each individual url and return a list with 1)Year, 2)Title, 3)The text of the speech
def get_speech(url):
#use the url and get the page
    page=requests.get(url)
#load the content of the page into an lxml tree
    tree=html.fromstring(page.content)
#get the title with xpath
    title=tree.xpath("//h1/text()")[0]
#get the year as a string based on the assumption that the title starts with the year
    year=title[:4]
#if the title turns out empty, try to get the title from the <h2> element
    if title in (None," "):
        title=tree.xpath("//h2/text()")[0]
#get all the <p> elements, i.e. the paragraphs
    pars=tree.xpath("//*[@class=\"mod mod-audio\"]/p/text()")
#based on the condition that a title has been found...
    if title not in (None," "):
#start a string with the text element, with the title as an attribute
        thespeech="<text title=\""+title+"\">"
#loop through the paragraphs
        for p in pars:
#write <p> tags around each paragraph
            thespeech+="<p>"+p+"</p>"
#close the string with </text> tag
        thespeech+="</text>"
#create a list based on year, title, and string of the speech
        this_data=[year,title,thespeech]
#return the list
        return (this_data)
    
#function to define what pages should be processed, returns a dataframe with the speeches
def get_speeches():
# create a list that will serve as a list of lists
    data=[]
#define the base of the urls
    urlbase="https://www.admin.ch/gov/de/start/dokumentation/reden/ansprachen-zum-nationalfeiertag/"
#Define two variables the delimit the range of years
    startyear=1977
    endyear=2020
#Looping through the range of years
    for i in range(startyear, endyear):
#create the url based on the base, the year, and the ending
        url=urlbase+str(i)+".html"
#try to read the speeches and add the list this returns to the list of lists
        try:
            data.append(get_speech(url))
        except:
            pass
#create a Data frame based on the list of lists
    df=pd.DataFrame(data, columns = ['Year', 'Title', 'Speech'])
#drop all the lines with error messages
    new_df=df[df.Year != 'Ein ']
    return new_df

    
def main():
#run the functions to get all speeches
    df=get_speeches()
#write a csv
    df.to_csv(outcsv, index=False)
    
if __name__ == "__main__":
#unless told otherwise, run the main function
    main()