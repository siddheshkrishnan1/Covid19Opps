#Importing packages
from selenium import webdriver
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from rake_nltk import Rake
import stringdist


r = Rake()


drivers = {"Technology/Computer Science": ["technical", "AWS", "software", "development", "cyber", "python", "parameter", "computer", "model", "predictive", "data", "machine", "artificial intelligence", "map"], 
           "Biomedical": ["biology", "ventilator", "lung", "FDA", "hospital", "medicine","tissue", "nasal", "oropharyngeal", "specimen", "oxygen", "placebo", "virus", "antibiotic", "infection", "chronic", "health", "drug", "swab", "blood", "heart", "genome", "clinical"]}
           #"Social Services": ["state", "lockdown", "environment", "community", "social", "low income", "distancing", "pandemic"]}

def stanford():

    driver = webdriver.Chrome('/Users/siddh1/Documents/Covid19Program/chromedriver')
    driver.get("https://med.stanford.edu/covid19/research.html")

    title = []
    contacts = []
    desc = []
    keyWords = []
    posts = driver.find_elements_by_class_name("text.parbase.section")
    for post in posts:
        entryVals = post.text.split("\n")
        if(len(entryVals) == 3):
            title.append(entryVals[0])
            contacts.append(entryVals[1])
            desc.append(entryVals[2])
            r.extract_keywords_from_text(entryVals[2])
            keyWords.append(getKeyWord(r.get_ranked_phrases()))



    driver.close()

    df = pd.DataFrame(list(zip(title, contacts, desc, keyWords)), 
                columns =['Project Title', 'Point of Contact', 'Project Description', 'Key Words']) 

    df.to_csv('StanfordProjects.csv', index = False)
    return df
    
#--------------------------------------------------------------


def longeststring(lst):
    longest = ""
    for x in lst:
        if isinstance(x, str) and len(x) > len(longest):
            longest = x
    return len(longest)


def getKeyWord(rankedPhrases):
    min_dist_ratio = 1
    driv = ""
    for driver in drivers: 
        indic = drivers.get(driver)
        div =  0
        total_ratio = 0
        for key_val in indic:
            for key_words in rankedPhrases:
                
                #This gets the levenshtein distance between each word if the row data is not 'None'
                if key_words is not None:
                    dist = stringdist.levenshtein(key_val.lower(), key_words.lower())
                    curr_dist_ratio = (dist/longeststring([key_val, key_words]))
                    total_ratio += curr_dist_ratio
                    div = div+1
        
        total_ratio = total_ratio/div
        if total_ratio <min_dist_ratio:
            min_dist_ratio = total_ratio
            driv = driver
    
    if min_dist_ratio <0.87:
        driv = "Other"
    return driv    


#--------------------------------------------------------------------------------------

def virginiaTech():
    driver = webdriver.Chrome('/Users/siddh1/Documents/Covid19Program/chromedriver')
    driver.get("https://www.research.vt.edu/covid-19-updates-impacts/opportunities.html")

    title = []
    typeOfResearch = []
    desc = []
    keyWords = []

    postsEven = driver.find_elements_by_class_name("rowTop.rowEven")
    postsOdd = driver.find_elements_by_class_name("rowTop.rowOdd")
    descs = driver.find_elements_by_class_name("vt-c-table-noPostProcess")[1:]
    index = 0

    for i in postsEven:
        entryVals = i.text.split("\n")
        title.append(entryVals[2])
        typeOfResearch.append(entryVals[4])
        desc.append(descs[index].text)
        r.extract_keywords_from_text(descs[index].text)
        keyWords.append(getKeyWord(r.get_ranked_phrases()))
        index+=2

    index = 1
    for i in postsOdd:
        entryVals = i.text.split("\n")
        title.append(entryVals[2])
        typeOfResearch.append(entryVals[4])
        desc.append(descs[index].text)
        r.extract_keywords_from_text(descs[index].text)
        keyWords.append(getKeyWord(r.get_ranked_phrases()))
        index+=2


    driver.close()

    df = pd.DataFrame(list(zip(title, typeOfResearch, desc, keyWords)), 
                    columns =['Project Title', 'Type of Research', 'Project Description', 'Key Words']) 

    df.to_csv('VirginiaTechProjects.csv', index = False)
    return df

stanford()
virginiaTech()

stanVal = pd.read_csv('StanfordProjects.csv')

stanTab = go.Figure(data=[go.Table(
    header=dict(values=list(stanVal.columns),
                fill_color='red',
                align='left'),
    cells=dict(values=[stanVal[k].tolist() for k in stanVal.columns[0:]],
               fill_color='white',
               align='left'))
])


vTVal = pd.read_csv('VirginiaTechProjects.csv')

vTTab = go.Figure(data=[go.Table(
    header=dict(values=list(vTVal.columns),
                fill_color='maroon',
                align='left'),
    cells=dict(values=[vTVal[k].tolist() for k in vTVal.columns[0:]],
               fill_color='orange',
               align='left'))
])




st.title('Covid-19 Research Opportunities')
oppVals = {'Stanford': stanTab, 'Virginia Tech': vTTab}
val = st.selectbox("Opportunity Choices", list(oppVals.keys()), 0)
st.plotly_chart(oppVals[val])

