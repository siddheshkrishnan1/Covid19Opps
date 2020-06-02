import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from pymongo import MongoClient


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

    return result


stanTab = getTable('StanfordProjects', 'red', 'white')
vTTab = getTable('VirginiaTechProjects', 'maroon', 'orange')
techTab = getTable('Technology and Computer Science', 'green', 'white')
bioTab = getTable('Biomedical', 'pink', 'white')
otherTab = getTable('Other', 'grey', 'white')



st.title('Covid-19 Research Opportunities')
oppVals = {'Stanford': stanTab, 'Virginia Tech': vTTab, "Technology": techTab, "Biomedical": bioTab, "Other": otherTab}
val = st.selectbox("Opportunity Choices", list(oppVals.keys()), 0)
st.plotly_chart(oppVals[val])