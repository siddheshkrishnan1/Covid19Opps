import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from pymongo import MongoClient

#Appropriate pairings for the descriptions and types of projects
pairings = ["Technology Projects: ", "Biomedical Projects", "Other Projects"]

#This method gets a table based on the associated name
def getTable(path, colorA, colorB):
    #Read in dataframe from mongodb
    client =  MongoClient("mongodb+srv://covid19Scraper:Covid-19@coviddata-ouz9f.mongodb.net/test?retryWrites=true&w=majority")
    db = client.Covid19Data
    collection = db[path]
    dataFrame = pd.DataFrame(list(collection.find()))
    #Delete unwanted columns
    del dataFrame['_id']
    del dataFrame['index']

    #Create a plotly go-figure table for the dataframe
    result = go.Figure(data=[go.Table(
        header=dict(values=list(dataFrame.columns),
                    fill_color=colorA,
                    align='left'),
        cells=dict(values=[dataFrame[k].tolist() for k in dataFrame.columns[0:]],
                fill_color=colorB,
                align='left'))
    ])
    
    
    #Return the dataframe and its size
    return [result, dataFrame.shape[0]]

#Normalize the amount of entries array by dividing by the max amount
def normalizeVals(numEntries):
    maxVal = max(numEntries)
    for i in range (len(numEntries)):
        numEntries[i] = (numEntries[i]/maxVal)
    return numEntries

#Loading in the data by calling all of the appropriate getTable calls
@st.cache #Cache function offered by streamlit
def loadData():
    stanTab = getTable('StanfordProjects', 'red', 'white')
    vTTab = getTable('VirginiaTechProjects', 'lavender', 'white')
    utTab = getTable('UTAustinProjects', 'orange', 'white')
    techTab = getTable('Technology and Computer Science', 'green', 'white')
    bioTab = getTable('Biomedical', 'pink', 'white')
    otherTab = getTable('Other', 'grey', 'white')
    #Getting the frequency of tech, bio, and other projects for a visualization
    freqs = [techTab[1], bioTab[1], otherTab[1]]
    freqs = normalizeVals(freqs)

    #Return all of the tables as well as the frequencies
    return [utTab[0], stanTab[0], vTTab[0], techTab[0], bioTab[0], otherTab[0], freqs]

#Loading the data
dataVals = loadData()

#The title and project description written to the app
st.title('Covid-19 Research Opportunities')
st.write("Below are research projects from different places which you could become a part of!")
st.write("Simply look for a project and contact those associated with it to see if you can collaborate to the effort.")

#Creating a drop-down menu for each of the sources
oppVals = {'UT Austin': dataVals[0], 'Stanford': dataVals[1], 'Virginia Tech': dataVals[2], "Technology": dataVals[3], "Biomedical": dataVals[4], "Other": dataVals[5]}
val = st.selectbox("Opportunity Choices", list(oppVals.keys()), 0)
#Plot the appropriate/selected chart
st.plotly_chart(oppVals[val])

#Simple visualization for the number of projects
for i in range(0, len(dataVals[6])):
    st.write(pairings[i])
    st.progress(dataVals[6][i])

#Blank line for aesthetic purposes
st.write("\n")

#Feedback text
st.write("We're always looking for feedback on how we can improve this tool! Please type in any feedback you have for us in the box down below! :) ")
#Initializing the mongodb client
client =  MongoClient("mongodb+srv://covid19Scraper:Covid-19@coviddata-ouz9f.mongodb.net/test?retryWrites=true&w=majority")
db = client['Covid19Data']
collection = db['Feedback']
#Creating an input area
feedback = st.text_area("Write here!")
#If the user presses enter
if feedback:
    #Write the feedback to the mongodb database
    feedBackRaw = {'FeedbackVal': [feedback]}
    dataFrame = pd.DataFrame(data=feedBackRaw)
    dataFrame.reset_index(inplace=True)
    data_dict = dataFrame.to_dict("records")
    collection.insert_many(data_dict)
    #let the user know that their feedback was received
    st.write("Great, we got your feedback!")

#fin
