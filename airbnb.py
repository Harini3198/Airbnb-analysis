import pandas as pd
import streamlit as st
from PIL import Image
import plotly.express as px

#Reading airbnb dataset from excel
host=pd.read_excel("host.xlsx")
host_cleaned=host.dropna()

#Creating plotly chart for analysis
def country_wise(country,option):
    cw=host_cleaned[host_cleaned["country"]==country]
    cw.reset_index(drop= True, inplace= True)

    cwp=cw.groupby("city")[[option]].sum()
    cwp.reset_index(inplace=True)

    fig=px.scatter_mapbox(cw,lat='latitude',lon='longitude',size=option,color=option,hover_name='city',title=f"{option.upper()} IN {country.upper()}",
                          color_continuous_scale='rainbow',mapbox_style='carto-positron')
    st.plotly_chart(fig)

    return cw

def country_wise_table(country):
    cwt=host_cleaned[host_cleaned["country"]==country]
    cwt.reset_index(drop= True, inplace= True)

    return cwt


def room_wise(df,type,option1):
    rw=df[df["room_type"]==type]
    rw.reset_index(drop= True, inplace= True)

    rwp=rw.groupby("neighborhood")[[option1]].sum()
    rwp.reset_index(inplace=True)
    if option1 == 'price':
        fig_bar1= px.bar(rwp, x="neighborhood", y=option1, title=f"{option1.upper()} IN ROOM-WISE", color_discrete_sequence=px.colors.sequential.dense_r, 
                        height=650, width=600)
        st.plotly_chart(fig_bar1)
    elif option1 == 'number_of_reviews':
        fig_bar1= px.bar(rwp, x="neighborhood", y=option1, title=f"{option1.upper()} IN ROOM-WISE", color_discrete_sequence=px.colors.sequential.Agsunset_r, 
                        height=650, width=600)
        st.plotly_chart(fig_bar1)
    elif option1 == 'rating':
        fig_bar1= px.bar(rwp, x="neighborhood", y=option1, title=f"{option1.upper()} IN ROOM-WISE", color_discrete_sequence=px.colors.sequential.Darkmint_r, 
                        height=650, width=600)
        st.plotly_chart(fig_bar1)
    elif option1 == 'availabitily':
        fig_bar1= px.bar(rwp, x="neighborhood", y=option1, title=f"{option1.upper()} IN ROOM-WISE", color_discrete_sequence=px.colors.sequential.Cividis_r, 
                        height=650, width=600)
        st.plotly_chart(fig_bar1)

def room_wise_table(df,type):
    rw=df[df["room_type"]==type]
    rw.reset_index(drop= True, inplace= True)
    return rw

def avail(area,df1):
    at=df1[df1["neighborhood"]==area]
    at.reset_index(drop= True, inplace= True)

    atr=at.groupby("room_type")[["availabitily"]].sum()
    atr.reset_index(inplace=True)

    fig_pie=px.pie(data_frame=atr,names="room_type",values="availabitily",width=600,title="Room availability",hole=0.5)
    st.plotly_chart(fig_pie)

#Streamlit part
st.set_page_config(layout="wide")
st.markdown("""
        <div style="text-align:center">
            <h1 style="color: purple;">AIRBNB DATA ANALYSIS</h1>
        </div>
    """, unsafe_allow_html=True)

with st.sidebar:
    select=st.selectbox("Select an Option",["Home","Data Exploration by chart","Data Exploration by Table","Analysis Report"])

#Home page
if select=="Home":
    
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

#Data Exploration page
elif select=="Data Exploration by chart":
    st.subheader(":violet[ANALYSING DATA BY CHART]")
    country=st.selectbox("Select any country",host_cleaned["country"].unique())
    option=st.radio("Choose any option to view",("price","number_of_reviews","rating","availabitily"))
    d1=country_wise(country,option)
    
    room=st.selectbox("Select any type of room",host_cleaned["room_type"].unique())
    rwopt=st.selectbox("Choose any option to view",["price","number_of_reviews","rating","availabitily"])
    room_wise(d1,room,rwopt)

    area=st.selectbox("Select any area", d1["neighborhood"].unique())
    avail(area,d1)

elif select == "Data Exploration by Table":
    st.subheader(":green[ANALYSING DATA BY TABLE]")
    country=st.selectbox("Select any country",host_cleaned["country"].unique())
    option=st.radio("Choose any option to view",("price","number_of_reviews","rating","availabitily"))
    cwtable=country_wise_table(country)
    cwtable_selcted=cwtable[['country','city','neighborhood',option]]
    st.dataframe(cwtable_selcted)

    room=st.selectbox("Select any type of room",host_cleaned["room_type"].unique())
    rwopt=st.selectbox("Choose any option to view",["price","number_of_reviews","rating","availabitily"])
    rwtable=room_wise_table(cwtable,room)
    rwtable_selected=rwtable[['country','city','neighborhood','room_type',option]]
    st.dataframe(rwtable_selected)

    area=st.selectbox("Select any area", rwtable["neighborhood"].unique())
    area_table=rwtable[rwtable["neighborhood"]==area]
    areaTable_selected=area_table[['neighborhood','availabitily','minimun_nights']]
    st.dataframe(areaTable_selected)

elif select == "Analysis Report":

    # Title for the app
    st.title("Power BI Report in Streamlit")

    # Embed Power BI report using an iframe
    powerbi_url = "https://app.powerbi.com/reportEmbed?reportId=cfcd6898-b303-44e5-b8e3-3d02d30fc079&autoAuth=true&ctid=de72fe03-2c2e-4d82-8388-caed97e2d767"

    st.markdown(f'<iframe width="1140" height="600" src="{powerbi_url}" frameborder="0" allowFullScreen="true"></iframe>', unsafe_allow_html=True)
