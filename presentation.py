import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
import pickle

df1 = pickle.load(open('df1.pkl','rb'))

data1 = pd.DataFrame(df1)
data1['price_per_sqft']=data1['price']*100000/data1['total_sqft']

top_10_locations_high_price = data1.groupby('location')['price_per_sqft'].mean().nlargest(10)
top_10_locations_low_price = data1.groupby('location')['price_per_sqft'].mean().nsmallest(10)

st.title('Bangalore House Price Analysis')
st.text('Please go through the analysis and choose the perfect property.')


col1, col2 = st.columns([10,10])

with col1:
    st.write("Locations with Highest Price")
    st.bar_chart(top_10_locations_high_price, height= 500, width = 150)

with col2:
    st.write("Locations with Lowest Price")
    st.bar_chart(top_10_locations_low_price, height= 500, width = 150)

top_11_locations = data1['location'].value_counts().nlargest(11)
top_10_locations = top_11_locations.drop('other')

bottom_11_locations = data1['location'].value_counts().nsmallest(10)

col3, col4 = st.columns([10,10])

with col3:
    st.write('Most Popular Locations')
    st.bar_chart(top_10_locations, height= 500, width=150)

with col4:
    st.write('Less Popular Locations')
    st.bar_chart(bottom_11_locations, height= 500, width= 150)


st.image('Dist_BHK_top_ten.png')

