import streamlit as st
import numpy as np
import pandas as pd
import pickle
import helper2
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

locations = helper2.locations
number = helper2.number
df1 = pickle.load(open('df1.pkl','rb'))
data1 = pd.DataFrame(df1)
data1['price_per_sqft']=data1['price']*100000/data1['total_sqft']
top_10_locations_high_price = data1.groupby('location')['price_per_sqft'].mean().nlargest(10)
top_10_locations_low_price = data1.groupby('location')['price_per_sqft'].mean().nsmallest(10)

st.markdown(
    f'''
        <style>
            .sidebar .sidebar-content {{
                width: 300px;
            }}
        </style>
    ''',
    unsafe_allow_html=True
)

st.sidebar.title('Bangalore House Price Analysis and Predictor')
user_menu = st.sidebar.radio('Select an Option', ('Price Analysis', 'Price Prediction'))


if user_menu == 'Price Analysis':
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


if user_menu == 'Price Prediction':

    c1, c2, c3 = st.columns([3,8,3])

    with c1:
        st.image('https://media1.giphy.com/media/IaWfbu0u4mF2SxOUiN/giphy.gif?cid=ecf05e479ebn08dgo3iy0wsm8fo5k8ahgjh6yfmyhyu36vgv&ep=v1_gifs_related&rid=giphy.gif&ct=g')

    with c2:
        st.title('Bangalore House Price Predictor')

    with c3:
        st.image('https://media1.giphy.com/media/IaWfbu0u4mF2SxOUiN/giphy.gif?cid=ecf05e479ebn08dgo3iy0wsm8fo5k8ahgjh6yfmyhyu36vgv&ep=v1_gifs_related&rid=giphy.gif&ct=g')

    loc = st.selectbox("Select location: ", options = locations)

    c4, c5 = st.columns([12,12])

    with c4:
        area = st.number_input("Enter the desired area of the flat in sqft: ")

    with c5:
        room = st.selectbox("How many living rooms you want: ", options = number)

    c6, c7 = st.columns([12,12])

    with c6:
        bath = st.selectbox("How many bathrooms you want: ", options = number)

    with c7:
        balcony = st.selectbox("How many balconys you want: ", options = number)


    if st.button("Predict"):
        df = pickle.load(open('df.pkl','rb'))
        data = pd.DataFrame(df)
        lr_model = pickle.load(open('model.pkl','rb'))
        X = data.drop('price',axis=1)

        def predict_price(location,sqft,bath,BHK,balcony):
            loc_index =np.where(X.columns==location)[0][0]
        
            x = np.zeros(len(X.columns))
            x[0] = sqft
            x[1] = bath
            x[2] = BHK
            x[3] = balcony
            if loc_index >= 0:
                x[loc_index] = 1
            return lr_model.predict([x])[0]


        price = int(predict_price(loc,area,bath,room,balcony))
        st.text("The predicated price is: " +str(price)+" lakh rupees")
        st.image('https://media1.giphy.com/media/e8ik35i8LaO3BqRwY6/giphy.gif?cid=ecf05e47z8i1iphq5vsrf0dudzhob3ofl5grtxtawj2byoxl&ep=v1_gifs_search&rid=giphy.gif&ct=g')