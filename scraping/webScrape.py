#Importing packages
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pdfplumber
import pandas as pd
from rake_nltk import Rake
import stringdist
from pymongo import MongoClient





r = Rake()


drivers = {"Technology and Computer Science": ["technical", "AWS", "software", "development", "cyber", "python", "parameter", "computer", "model", "predictive", "data", "machine", "artificial intelligence", "map"], 
           "Biomedical": ["biology", "ventilator", "lung", "FDA", "hospital", "medicine","tissue", "nasal", "oropharyngeal", "specimen", "oxygen", "placebo", "virus", "antibiotic", "infection", "chronic", "health", "drug", "swab", "blood", "heart", "genome", "clinical"]}
           #"Social Services": ["state", "lockdown", "environment", "community", "social", "low income", "distancing", "pandemic"]}

catTables = {'Technology and Computer Science': [],
              'Biomedical': [],
              'Other': []}

for keys in catTables:
    for i in range(0, 4):
        catTables[keys].append([])

def stanford():
    options = Options()
    options.headless = True
    driver = webdriver.Chrome('/Users/siddh1/Documents/Covid19Program/chromedriver', chrome_options=options)
    driver.get("https://med.stanford.edu/covid19/research.html")

    title = []
    contacts = []
    desc = []
    keyWords = []
    links = []
    posts = driver.find_elements_by_class_name("text.parbase.section")
    linkVals = driver.find_elements_by_class_name("text.parbase.section [href]")
 
   
    

    for post in posts:
        entryVals = post.text.split("\n")
        if(len(entryVals) == 3):
            title.append(entryVals[0])
            contacts.append(entryVals[1])
            desc.append(entryVals[2])
            r.extract_keywords_from_text(entryVals[2])
            keyPhrase = getKeyWord(r.get_ranked_phrases())
            keyWords.append(keyPhrase)
            catTables[keyPhrase][0].append(entryVals[0])
            catTables[keyPhrase][1].append("Stanford")
            catTables[keyPhrase][3].append(entryVals[2])
            
            linkTxt = []
            for relLinks in linkVals:
                textVal = relLinks.text
                if textVal in entryVals[1]:
                    linkTxt.append(str(relLinks.get_attribute('href'))+" ")
            
            linkTxt = list(set(linkTxt))
            resVal = "\n".join(linkTxt)
            resVal = " "+resVal
            links.append(resVal)
            catTables[keyPhrase][2].append(resVal)



            


    driver.close()

    df = pd.DataFrame(list(zip(title, contacts, desc, links, keyWords)), 
                columns =['Project Title', 'Point of Contact', 'Project Description', 'Relevant Links', 'Key Words']) 

    df.to_csv('StanfordProjects.csv', index = False)


    client =  MongoClient("mongodb+srv://covid19Scraper:Covid-19@coviddata-ouz9f.mongodb.net/test?retryWrites=true&w=majority")
    db = client['Covid19Data']
    name = 'StanfordProjects'
    collection = db[name]
    collection.drop()
    collection = db[name]
    df.reset_index(inplace=True)
    data_dict = df.to_dict("records")
    # Insert collection
    collection.insert_many(data_dict)
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
    options = Options()
    options.headless = True
    driver = webdriver.Chrome('/Users/siddh1/Documents/Covid19Program/chromedriver', chrome_options=options)
    driver.get("https://www.research.vt.edu/covid-19-updates-impacts/opportunities.html")

    title = []
    typeOfResearch = []
    desc = []
    links = []
    keyWords = []

    postsEven = driver.find_elements_by_class_name("rowTop.rowEven")
    linkValsEven = driver.find_elements_by_class_name("rowTop.rowEven [href]")

    
    postsOdd = driver.find_elements_by_class_name("rowTop.rowOdd")
    linkValsOdd = driver.find_elements_by_class_name("rowTop.rowOdd [href]")
    descs = driver.find_elements_by_class_name("vt-c-table-noPostProcess")
    
    index = 0

    for i in postsEven:
        entryVals = i.text.split("\n")
        title.append(entryVals[2])
        typeOfResearch.append(entryVals[4])
        desc.append(descs[index].text)
        r.extract_keywords_from_text(descs[index].text)
        keyPhrase = getKeyWord(r.get_ranked_phrases())
        keyWords.append(keyPhrase)
        catTables[keyPhrase][0].append(entryVals[2])
        catTables[keyPhrase][1].append("Virginia Tech")
        catTables[keyPhrase][3].append(descs[index].text)
        
        index+=2

    for linksVals in linkValsEven:
        indivLink = str(linksVals.get_attribute('href'))
        links.append(indivLink)
        catTables[keyPhrase][2].append(indivLink)


    index = 1
    for i in postsOdd:
        entryVals = i.text.split("\n")
        title.append(entryVals[2])
        typeOfResearch.append(entryVals[4])
        desc.append(descs[index].text)
        r.extract_keywords_from_text(descs[index].text)
        keyPhrase = getKeyWord(r.get_ranked_phrases())
        keyWords.append(keyPhrase)
        catTables[keyPhrase][0].append(entryVals[2])
        catTables[keyPhrase][1].append("Virginia Tech")
        catTables[keyPhrase][3].append(descs[index].text)
  
        index+=2

    for linksVals in linkValsOdd:
        indivLink = str(linksVals.get_attribute('href'))
        links.append(indivLink)
        catTables[keyPhrase][2].append(indivLink)


    driver.close()

    df = pd.DataFrame(list(zip(title, typeOfResearch, desc, links, keyWords)), 
                    columns =['Project Title', 'Type of Research', 'Project Description', 'Relevant Links', 'Key Words']) 

    df.to_csv('VirginiaTechProjects.csv', index = False)

    client =  MongoClient("mongodb+srv://covid19Scraper:Covid-19@coviddata-ouz9f.mongodb.net/test?retryWrites=true&w=majority")
    db = client['Covid19Data']
    name = 'VirginiaTechProjects'
    collection = db[name]
    collection.drop()
    collection = db[name]
    df.reset_index(inplace=True)
    data_dict = df.to_dict("records")
    # Insert collection
    collection.insert_many(data_dict)
    return df
#--------------------------------------------------------------------------------------
def utAustin():
    pathToFile = "/Users/siddh1/Documents/Covid19Program/scraping/UT COVID-19 Researchers_active projs only_2020-05-19.pdf"
    pdf = pdfplumber.open(pathToFile)
    pages = pdf.pages[1:-1]
    names = []
    departments = []
    description = []
    contacts = []
    keyWords = []

    for page in pages:
        pageVal = page.extract_text().split("\n")
        if(len(pageVal)>1):
            names.append(pageVal[0])
            departments.append(pageVal[1])
            contact = pageVal[-1]
            descVal = "\n".join(pageVal[2:-1])
            contact = contact.split(" ")
            eduIn = False
            poc = ""
            for x in contact:
                if ".edu" in x or ".com" in x:
                    eduIn = True
                    break
            if eduIn == True:
                poc = contact[0]
                contacts.append(contact[0])
                if (len(contact) > 1):
                    contact = " ".join(contact[1:])
                    descVal = descVal + contact
            
            if eduIn == False:
                contact = pageVal[-2].split(" ")
                poc = contact[0]
                contacts.append(contact[0])
                descVal = "\n".join(pageVal[2:-2])
                if (len(contact) > 1):
                    contact = " ".join(contact[1:])
                    descVal = descVal + contact
                descVal = descVal + (" ".join(pageVal[-1]))

            description.append(descVal)
            r.extract_keywords_from_text(descVal)
            keyPhrase = getKeyWord(r.get_ranked_phrases())
            keyWords.append(keyPhrase)
            catTables[keyPhrase][0].append(pageVal[0])
            catTables[keyPhrase][1].append("UT Austin")
            linkVal = "No links but here is the point of contact: "+poc
            catTables[keyPhrase][2].append(linkVal)
            catTables[keyPhrase][3].append(descVal)

    


    df = pd.DataFrame(list(zip(names, departments, description, contacts, keyWords)), 
                    columns =['Person Name', 'Department', 'Project Description', 'Point of Contact', 'Key Words']) 

    df.to_csv('UTAustinProjects.csv', index = False)

    client =  MongoClient("mongodb+srv://covid19Scraper:Covid-19@coviddata-ouz9f.mongodb.net/test?retryWrites=true&w=majority")
    db = client['Covid19Data']
    name = 'UTAustinProjects'
    collection = db[name]
    collection.drop()
    collection = db[name]
    df.reset_index(inplace=True)
    data_dict = df.to_dict("records")
    # Insert collection
    collection.insert_many(data_dict)
    return df
    
#--------------------------------------------------------------------------------------

def princeton():
    print()

#--------------------------------------------------------------------------------------

def ucSanDiego():
    print()

#--------------------------------------------------------------------------------------

def turnCatstoFiles():
    for keys in catTables:
        fileName = str(keys)+".csv"
        df = pd.DataFrame(list(zip(catTables[keys][0], catTables[keys][1], catTables[keys][2], catTables[keys][3])), 
                    columns =['Project Title', 'Source', 'Relevant Links', 'Project Description']) 
        df.to_csv(fileName, index = False)

        client =  MongoClient("mongodb+srv://covid19Scraper:Covid-19@coviddata-ouz9f.mongodb.net/test?retryWrites=true&w=majority")
        db = client['Covid19Data']
        collection = db[str(keys)]
        collection.drop()
        collection = db[str(keys)]
        df.reset_index(inplace=True)
        data_dict = df.to_dict("records")
        # Insert collection
        collection.insert_many(data_dict)



   
stanford()
virginiaTech()
utAustin()
turnCatstoFiles()

