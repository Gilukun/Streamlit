# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import streamlit as st
import pandas as pd
import numpy as np
import pandas as pd
import numpy as np

import seaborn as sns
from bokeh.plotting import figure, output_notebook, show
output_notebook()

from bokeh.tile_providers import get_provider 
from  bokeh.models import ColumnDataSource, HoverTool
from  bokeh.models import LabelSet
from plotly.subplots import make_subplots
import plotly.express as px
import re

import folium

import openrouteservice 
from openrouteservice import client


PACA = pd.read_csv('/Users/gillesv/Documents/DataScientest/datatourisme.POI_OK_20210921.PACA.csv')
centroidFrance = pd.read_csv('/Users/gillesv/Documents/DataScientest/CentroidFrance.csv') 




header = st.container()

with header:
    st.title("Pytinéo")
    st.text('Pytinéo le renouveau de la création d intinéraire')
    
PACA_theme_count = PACA['Thématique_POI'].value_counts()

plotlypie_theme = px.pie(PACA_theme_count, 
                         values=PACA_theme_count, 
                         names=PACA_theme_count.index, 
                         title="Répartition des thèmes de POI")

plotlypie_theme.update_traces(textposition='outside', textinfo='percent')

st.plotly_chart(plotlypie_theme)


page = st.radio("Radio box", ["Arles", "Marseille"], index=0)

if page == "Arles":
    Arles = PACA.loc[PACA['Nom_commune']=="Arles"].head(10)
    coords = Arles[['Longitude', 'Latitude']].values.tolist()[:10]
    client = openrouteservice.Client(key='5b3ce3597851110001cf62489585426c1497421aa8b3c7a5d4c5c5f0')
    routes = client.directions(coords)
    route = client.directions(coordinates = coords,
                         profile = 'cycling-road',  # [“driving-car”, “driving-hgv”, “foot-walking”, “foot-hiking”, “cycling-regular”, “cycling-road”,”cycling-mountain”, “cycling-electric”,]. Default “driving-car”.
                         format ='geojson')

    maps = folium.Map(location=[43.677795, 4.628619], tiles='cartodbpositron', zoom_start=9)

    for index, row in Arles.iterrows():
        folium.Marker(location=[row.loc['Latitude'], row.loc['Longitude']], tooltip= row.loc['Nom_du_POI'], icon=folium.Icon(color='lightgray', icon='fire', prefix='fa')).add_to(maps)

    folium.GeoJson(route, name='test').add_to(maps)

    maps
    
elif page == "Marseille":
    Arles = PACA.loc[PACA['Nom_commune']=="Marseille"].head(10)
    coords = Arles[['Longitude', 'Latitude']].values.tolist()[:10]


    client = openrouteservice.Client(key='5b3ce3597851110001cf62489585426c1497421aa8b3c7a5d4c5c5f0') # Specify your personal API key
    routes = client.directions(coords)

    route = client.directions(coordinates = coords,
                         profile = 'cycling-road',  # [“driving-car”, “driving-hgv”, “foot-walking”, “foot-hiking”, “cycling-regular”, “cycling-road”,”cycling-mountain”, “cycling-electric”,]. Default “driving-car”.
                         format ='geojson')

    maps = folium.Map(location=[43.300000, 5.400000], tiles='cartodbpositron', zoom_start=9)

    for index, row in Arles.iterrows():
        folium.Marker(location=[row.loc['Latitude'], row.loc['Longitude']], tooltip= row.loc['Nom_du_POI'], icon=folium.Icon(color='lightgray', icon='fire', prefix='fa')).add_to(maps)

    folium.GeoJson(route, name='test').add_to(maps)

    maps                      