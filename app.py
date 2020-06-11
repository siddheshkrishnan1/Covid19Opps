import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from pymongo import MongoClient


pairings = ["Technology Projects: ", "Biomedical Projects", "Other Projects"]

def getTable(path, colorA, colorB):
    client =  MongoClient("mongodb+srv://covid19Scraper:Covid-19@coviddata-ouz9f.mongodb.net/test?retryWrites=true&w=majority")
    db = client.Covid19Data
    collection = db[path]
    dataFrame = pd.DataFrame(list(collection.find()))
    del dataFrame['_id']
    del dataFrame['index']

    result = go.Figure(data=[go.Table(
        header=dict(values=list(dataFrame.columns),
                    fill_color=colorA,
                    align='left'),
        cells=dict(values=[dataFrame[k].tolist() for k in dataFrame.columns[0:]],
                fill_color=colorB,
                align='left'))
    ])
    
    

    return [result, dataFrame.shape[0]]


def normalizeVals(numEntries):
    maxVal = max(numEntries)
    for i in range (len(numEntries)):
        numEntries[i] = (numEntries[i]/maxVal)
    return numEntries

@st.cache
def loadData():
    stanTab = getTable('StanfordProjects', 'red', 'white')
    vTTab = getTable('VirginiaTechProjects', 'lavender', 'white')
    utTab = getTable('UTAustinProjects', 'orange', 'white')
    techTab = getTable('Technology and Computer Science', 'green', 'white')
    bioTab = getTable('Biomedical', 'pink', 'white')
    otherTab = getTable('Other', 'grey', 'white')
    freqs = [techTab[1], bioTab[1], otherTab[1]]
    freqs = normalizeVals(freqs)

    return [utTab[0], stanTab[0], vTTab[0], techTab[0], bioTab[0], otherTab[0], freqs]

dataVals = loadData()


st.title('Covid-19 Research Opportunities')
st.write("Below are research projects from different places which you could become a part of!")
st.write("Simply look for a project and contact those associated with it to see if you can collaborate to the effort.")

oppVals = {'UT Austin': dataVals[0], 'Stanford': dataVals[1], 'Virginia Tech': dataVals[2], "Technology": dataVals[3], "Biomedical": dataVals[4], "Other": dataVals[5]}
val = st.selectbox("Opportunity Choices", list(oppVals.keys()), 0)
st.plotly_chart(oppVals[val])


for i in range(0, len(dataVals[6])):
    st.write(pairings[i])
    st.progress(dataVals[6][i])

st.write("\n")

st.write("We're always looking for feedback on how we can improve this tool! Please type in any feedback you have for us in the box down below! :) ")
client =  MongoClient("mongodb+srv://covid19Scraper:Covid-19@coviddata-ouz9f.mongodb.net/test?retryWrites=true&w=majority")
db = client['Covid19Data']
collection = db['Feedback']
feedback = st.text_area("Write here!")
if feedback:
    feedBackRaw = {'FeedbackVal': [feedback]}
    dataFrame = pd.DataFrame(data=feedBackRaw)
    dataFrame.reset_index(inplace=True)
    data_dict = dataFrame.to_dict("records")
    collection.insert_many(data_dict)
    st.write("Great, we got your feedback!")
