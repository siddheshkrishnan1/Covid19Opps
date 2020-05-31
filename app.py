import streamlit as st
import plotly.graph_objects as go
import pandas as pd

def getTable(path, colorA, colorB):
    dataFrame = pd.read_csv(path)

    result = go.Figure(data=[go.Table(
        header=dict(values=list(dataFrame.columns),
                    fill_color=colorA,
                    align='left'),
        cells=dict(values=[dataFrame[k].tolist() for k in dataFrame.columns[0:]],
                fill_color=colorB,
                align='left'))
    ])

    return result


stanTab = getTable('StanfordProjects.csv', 'red', 'white')
vTTab = getTable('VirginiaTechProjects.csv', 'maroon', 'orange')
techTab = getTable('Technology and Computer Science.csv', 'green', 'white')
bioTab = getTable('Biomedical.csv', 'pink', 'white')
otherTab = getTable('Other.csv', 'grey', 'white')


st.title('Covid-19 Research Opportunities')
oppVals = {'Stanford': stanTab, 'Virginia Tech': vTTab, "Technology": techTab, "Biomedical": bioTab, "Other": otherTab}
val = st.selectbox("Opportunity Choices", list(oppVals.keys()), 0)
st.plotly_chart(oppVals[val])