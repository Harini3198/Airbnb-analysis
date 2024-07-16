import pandas as pd
from pymongo import MongoClient
import streamlit as st
from PIL import Image
import plotly.express as px

host=pd.read_excel("host.xlsx")
host_cleaned=host.dropna()


def country_wise(city):
    cw=host_cleaned[host_cleaned["city"]==city]
    cw.reset_index(drop= True, inplace= True)

    cwp=cw.groupby("neighborhood")[["price","rating"]].sum()
    cwp.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:
        fig_bar1= px.bar(cwp, x="neighborhood", y="price", title="price in city-wise", color_discrete_sequence=px.colors.sequential.Agsunset, 
                        height=650, width=600)
        st.plotly_chart(fig_bar1)
    with col2:
        fig_bar2= px.bar(cwp, x="neighborhood", y="rating", title="rating in city-wise", color_discrete_sequence=px.colors.sequential.Bluered_r, 
                        height=650, width=600)
        st.plotly_chart(fig_bar2)
    return cw

def room_wise(df,type):
    rw=df[df["room_type"]==type]
    rw.reset_index(drop= True, inplace= True)

    rwp=rw.groupby("neighborhood")[["price","rating"]].sum()
    rwp.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:
        fig_bar1= px.bar(rwp, x="neighborhood", y="price", title="price in room-wise", color_discrete_sequence=px.colors.sequential.dense_r, 
                        height=650, width=600)
        st.plotly_chart(fig_bar1)
    with col2:
        fig_bar2= px.bar(rwp, x="neighborhood", y="rating", title="rating in room-wise", color_discrete_sequence=px.colors.sequential.haline, 
                        height=650, width=600)
        st.plotly_chart(fig_bar2)

def avail(area,df1):
    at=df1[df1["neighborhood"]==area]
    at.reset_index(drop= True, inplace= True)

    atr=at.groupby("room_type")[["availabitily"]].sum()
    atr.reset_index(inplace=True)

    fig_pie=px.pie(data_frame=atr,names="room_type",values="availabitily",width=600,title="Room availability",hole=0.5)
    st.plotly_chart(fig_pie)

st.set_page_config(layout="wide")

with st.sidebar:
    select=st.selectbox("Select an Option",["Home","Data Exploration"])
if select=="Home":
    st.markdown("""
        <div style="text-align:center">
            <h1 style="color: purple;">AIRBNB DATA ANALYSIS</h1>
        </div>
    """, unsafe_allow_html=True)
    airbnb1=Image.open("airbnb1.jpg")
    st.image(airbnb1,width=1000)
    st.markdown("")
    st.markdown("")
    col1,col2=st.columns(2)
    with col1:
        st.header("Host anything, anywhere, so guests can enjoy everything, everywhere")
        st.subheader(":blue[A community built for belongings]")
        st.subheader(":blue[Enjoy unique stays and experiences]")
        st.subheader(":blue[Services you can trust]")
        st.subheader(":blue[24/7 support for Host and guests]")
    with col2:
        st.video("Beautiful Destinations in Rio de Janeiro, Brazil.mp4")
elif select=="Data Exploration":
    
    city=st.selectbox("Select any country",host_cleaned["city"].unique())
    d1=country_wise(city)
    
    room=st.selectbox("Select any type of room",host_cleaned["room_type"].unique())
    room_wise(d1,room)

    area=st.selectbox("Select any area", d1["neighborhood"].unique())
    avail(area,d1)


    





















