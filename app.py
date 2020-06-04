import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from pymongo import MongoClient

numEntries = []
pairings = ["Technology Projects: ", "Biomedical Projects", "Other Projects"]

def getTable(path, colorA, colorB, addProgress):
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
    
    if addProgress is True:
        numEntries.append(dataFrame.shape[0])

    return result


def normalizeVals():
    maxVal = max(numEntries)
    for i in range (len(numEntries)):
        numEntries[i] = (numEntries[i]/maxVal)
    

stanTab = getTable('StanfordProjects', 'red', 'white', False)
vTTab = getTable('VirginiaTechProjects', 'maroon', 'orange', False)
techTab = getTable('Technology and Computer Science', 'green', 'white', True)
bioTab = getTable('Biomedical', 'pink', 'white', True)
otherTab = getTable('Other', 'grey', 'white', True)
normalizeVals()


st.title('Covid-19 Research Opportunities')

oppVals = {'Stanford': stanTab, 'Virginia Tech': vTTab, "Technology": techTab, "Biomedical": bioTab, "Other": otherTab}
val = st.selectbox("Opportunity Choices", list(oppVals.keys()), 0)
st.plotly_chart(oppVals[val])

for i in range (len(numEntries)):
    st.write(pairings[i]) 
    st.progress(numEntries[i])