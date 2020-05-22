#Importing packages
from selenium import webdriver
import pandas as pd

driver = webdriver.Chrome('/Users/siddh1/Documents/Covid19Program/chromedriver')
driver.get("https://med.stanford.edu/covid19/research.html")

title = []
contacts = []
desc = []
posts = driver.find_elements_by_class_name("text.parbase.section")
print(posts)
for post in posts:
    entryVals = post.text.split("\n")
    if(len(entryVals) == 3):
        title.append(entryVals[0])
        contacts.append(entryVals[1])
        desc.append(entryVals[2])


df = pd.DataFrame(list(zip(title, contacts, desc)), 
               columns =['Project Title', 'Point of Contact', 'Project Description']) 

df.to_csv('StanfordProjects.csv', index = False)



