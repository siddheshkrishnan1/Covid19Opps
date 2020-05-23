#Importing packages
from selenium import webdriver
import pandas as pd

def stanford():

    driver = webdriver.Chrome('/Users/siddh1/Documents/Covid19Program/chromedriver')
    driver.get("https://med.stanford.edu/covid19/research.html")

    title = []
    contacts = []
    desc = []
    posts = driver.find_elements_by_class_name("text.parbase.section")
    for post in posts:
        entryVals = post.text.split("\n")
        if(len(entryVals) == 3):
            title.append(entryVals[0])
            contacts.append(entryVals[1])
            desc.append(entryVals[2])
    driver.close()

    df = pd.DataFrame(list(zip(title, contacts, desc)), 
                columns =['Project Title', 'Point of Contact', 'Project Description']) 

    df.to_csv('StanfordProjects.csv', index = False)
    
#--------------------------------------------------------------
def virginiaTech():
    driver = webdriver.Chrome('/Users/siddh1/Documents/Covid19Program/chromedriver')
    driver.get("https://www.research.vt.edu/covid-19-updates-impacts/opportunities.html")

    title = []
    typeOfResearch = []
    desc = []
    postsEven = driver.find_elements_by_class_name("rowTop.rowEven")
    postsOdd = driver.find_elements_by_class_name("rowTop.rowOdd")
    descs = driver.find_elements_by_class_name("vt-c-table-noPostProcess")[1:]
    index = 0

    for i in postsEven:
        entryVals = i.text.split("\n")
        title.append(entryVals[2])
        typeOfResearch.append(entryVals[4])
        desc.append(descs[index].text)
        index+=2

    index = 1
    for i in postsOdd:
        entryVals = i.text.split("\n")
        title.append(entryVals[2])
        typeOfResearch.append(entryVals[4])
        desc.append(descs[index].text)
        index+=2


    driver.close()

    df = pd.DataFrame(list(zip(title, typeOfResearch, desc)), 
                    columns =['Project Title', 'Type of Research', 'Project Description']) 

    df.to_csv('VirginiaTechProjects.csv', index = False)

stanford()
virginiaTech()

