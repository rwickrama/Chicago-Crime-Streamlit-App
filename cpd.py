import streamlit as st 
import pandas as pd
import pydeck as pdk
import numpy as np
import xlrd
import plotly.express as px


st.title("Crime in Chicago 👮‍♂(2019)")

@st.cache(persist=True)
def load_data(nrows):
    data=pd.read_excel('chicago crime 2019.xls',nrows=nrows,encoding="ISO-8859-1")
    data.dropna(subset=['Latitude','Longitude'],inplace=True)
    data['time'] = data['Date'].dt.hour
    data['date']=[d.date() for d in data['Date']]
    data['day']=[d.day_name() for d in data['Date']]
   
    data.dropna(subset=['Latitude','Longitude'],inplace=True)
    data.drop(columns=['Date'],inplace=True)
    lowercase=lambda x: str(x).lower()
    data.rename(lowercase,axis="columns",inplace=True)
    return data
    
data=load_data(65000)


st.header("Number of crimes at a given time of a day")
hour=st.slider("Hour to look at",0,23)
hour
original_data=data
data=data[data["time"]==hour]
#data

midpoint=(np.average(data['latitude']),np.average(data['longitude']))
st.markdown("All Crimes")

st.write(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v10",
    initial_view_state={
        "latitude":midpoint[0],
        "longitude":midpoint[1],
        "zoom":11,
        "pitch":30,
    },
    layers=[
        pdk.Layer(
        "HexagonLayer",
        data=data[['time','latitude','longitude']],
        get_position=["longitude","latitude"],
        auto_highlight=True,
        radius=100,
        extruded=True,
        pickable=True,
        elevation_scale=4,
        elevation_range=[0,1000],
        ),
    ],
))


data2=original_data


st.header("Number of crimes on a given day of the week")


option = st.selectbox(
    'Select a day of the week',
    ('Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'))

st.write('You selected:', option)

data2=data2[data2['day']==option]



df_crime_types=pd.DataFrame(data2['primary type'].value_counts())
df_crime_types['crime type']=df_crime_types.index
df_crime_types.rename(columns={'primary type':'count'}, inplace=True)

df_types=df_crime_types[['crime type','count']]

import plotly.express as px

long_df = px.data.medals_long()

fig = px.bar(df_types, x="crime type", y="count", title="Types of Crimes",height=800,width=800)
st.write(fig)

st.header("Locations with most crime at a given time of a day")

hour2=st.slider("Select a time",0,23)
hour2

data3=original_data

data3=data3[data3['time']==hour2]

def treemap(categories,title,path,values):
    fig = px.treemap(categories, path=path, values=values, height=700,
                 title=title, color_discrete_sequence = px.colors.sequential.RdBu)
    fig.data[0].textinfo = 'label+text+value'
    st.write(fig)
    
df_loc=pd.DataFrame(data3['location description'].value_counts())

df_loc['location']=df_loc.index
df_loc['count']=df_loc['location description']

treemap(df_loc,'Locations with most crime',['location'],df_loc['count'])
    
 
st.header("Locations with most theft/burglaries")
hour3=st.slider("Select any time",0,23)
hour3

data4=original_data[original_data["primary type"]=="THEFT"]
data5=data4[data4["time"]==hour3]
#data

midpoint=(np.average(data5['latitude']),np.average(data5['longitude']))
st.markdown("Theft")

st.write(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v10",
    initial_view_state={
        "latitude":midpoint[0],
        "longitude":midpoint[1],
        "zoom":11,
        "pitch":30,
    },
    layers=[
        pdk.Layer(
        "HexagonLayer",
        data=data5[['time','latitude','longitude']],
        get_position=["longitude","latitude"],
        auto_highlight=True,
        radius=100,
        extruded=True,
        pickable=True,
        elevation_scale=4,
        elevation_range=[0,1000],
        ),
    ],
))