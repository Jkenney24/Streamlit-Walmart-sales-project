#-----Importing Modules-----#

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import seaborn as sns

#Setting the page layout right away (I prefer the wide view)
st.set_page_config(layout='wide')

#-----Import Dataframe-----#

df=pd.read_csv(r"Walmart_Sales.csv")

#-----Wrangle and structure data for analysis-----#
# I want to see total/average sales per store
# I want to see total sales per store for each year
# I want to see my monthly top store performer quickly
# I want to see my region performance overall quickly over the timeframe


#Converting messy date string to datetime so I can use the dates 
df['Date'] = pd.to_datetime(df['Date'], format='mixed')

#Creating a Month column
df['Month']=df['Date'].dt.month
#Creating a year column
df['Year']=df['Date'].dt.year


#Creating a unique month variable
months=df["Month"].unique()
#creating a unique year variable
year=df['Year'].unique()
#Creating a unique store variable
store=df['Store'].unique()

#-----Streamlit APP-----#

#Title
st.title("Regional Revenue Review")
#Using a blank subheader as a divider with the main walmart color (blue) for a little company familiarity
st.subheader('', divider='blue')

#Columns for formatting options, I want each selection on either side and looking professional
col1, _, _, col4 = st.columns([1,1,1,.5])
#Radio selectors for year
year_selected=col1.radio('Select Year', year, index= 0)

#Select box for store
store_selected=col4.selectbox('Select Store #', store)

#Selected store filtering
selected_store_df=df[df["Store"]==store_selected]
#Selected year for filtering
selected_year_df=df[df["Year"]==year_selected]

#New dataframe with store sales total
df_store_summed=selected_store_df.groupby("Store").agg({"Weekly_Sales": "sum"}).reset_index()
df_store_summed['Store Average']=round(df_store_summed["Weekly_Sales"]/36,0)

#New dataframe with year sales total for year
df_year_summed=selected_year_df.groupby("Year").agg({"Weekly_Sales": "sum"}).reset_index()
df_year_summed['Average Sales']=round(df_year_summed["Weekly_Sales"]/3,0)

#Using a blank subheader as a divider with walmart color for company familiarity again
st.subheader('', divider='blue')


#-----Metrics-----#

#Store metrics with a caption and dicider for a nice touch to break the monotony 
st.subheader("Store Revenue Metrics", divider='green') ; st.caption('Statistics per store 💵')
with st.container(border=True):
    #Creating columns
    col1, col2, col3 =st.columns([.5, 1, 1])

    #Metrics for each column
    col1.metric('Store Number', "{:.0f}".format(df_store_summed['Store'].values[0]))
    col2.metric('Monthly Average Store Revenue', "${:,.0f}".format(df_store_summed['Store Average'].values[0]))
    col3.metric('Total Store Revenue', "${:,.0f}".format(df_store_summed['Weekly_Sales'].values[0]))

#Year metrics with a caption and divider for a nice touch to break the monotony
st.subheader("Regional Revenue Metrics", divider='green'); st.caption('Statistics for the region💸🪙')
with st.container(border=True):
    #Creating columns
    col1, col2, col3 =st.columns([.5, 1, 1])

    #Metrics for each column
    col1.metric('Year', df_year_summed['Year'].values[0])
    col2.metric('Annual Average Revenue', "${:,.0f}".format(df_year_summed['Average Sales'].values[0]))
    col3.metric('Annual Total Revenue', "${:,.0f}".format(df_year_summed['Weekly_Sales'].values[0]))

#-----Visualizations-----#

#Adding a little spacing
st.subheader('')

#Graph visualizations
st.subheader('Visualizing the Numbers', divider='red')

#Creating Tabs for each visualization
Tab1, Tab2 = st.tabs(['Annual Revenue Total', 'Store Revenue Monthly Average'])

#Creating dataframes for the specific graphs
df_year_graph=df.groupby('Year')['Weekly_Sales'].sum().reset_index()
df_store_graph=df.groupby('Store').agg({'Weekly_Sales': 'sum'}).reset_index()
df_store_graph["Store Average"]=round(df_store_graph["Weekly_Sales"]/36, 0)
#st.dataframe(df_store_graph) <----(TEST)

#Creating my customized graphs with plotly graph objects
with Tab1:
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df_year_graph['Year'], y=df_year_graph['Weekly_Sales'], name='Revenue by Year'))
    fig.update_layout(xaxis_title= 'Year', yaxis_title='Revenue in Billions')
    fig.layout.template = 'seaborn'
    st.plotly_chart(fig, use_container_width=True)
with Tab2:
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(x=df_store_graph['Store'], y=df_store_graph['Store Average'], name='Revenue by Store'))
    fig2.update_layout(xaxis_title= 'Store Number', yaxis_title='Revenue in Millions')
    fig2.layout.template = 'simple_white'
    st.plotly_chart(fig2, use_container_width=True)



#I Tested dataframes throughout the project to see the tables in the web browser.
#st.dataframe(df_store_summed)  <----(TEST)
#st.dataframe(df_year_summed)  <----(TEST)
