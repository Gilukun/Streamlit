# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 17:27:47 2021

@author: Gilles
"""
# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
import numpy as np
import pandas as pd
import numpy as np

from plotly.subplots import make_subplots
import plotly.express as px

import folium
from streamlit_folium import folium_static

import openrouteservice 
from openrouteservice import client

#Avant de lancer Streamlit installer : 

df= pd.read_csv('Data/datatourisme.POI_OK_20210921.PACA.csv')
centroid= pd.read_csv('Data/CentroidFrance.csv')

intro = st.container()

with intro:
    st.title("Pytinéo")
    st.text('Pytinéo le renouveau de la création d intinéraire')

analysis = st.container()

with analysis:
    st.header("Analyse de données")
    st.write('Analyse des datasets pour définir notre projet')
    st.dataframe(data=df.head(10))

PACA_theme_count = df['Thématique_POI'].value_counts()

plotlypie_theme = px.pie(PACA_theme_count, 
                         values=PACA_theme_count, 
                         names=PACA_theme_count.index, 
                         title="Répartition des thèmes de POI")

plotlypie_theme.update_traces(textposition='outside', textinfo='percent')

st.plotly_chart(plotlypie_theme)
st.caption('Répartition des POIs du DataSet')


commune = df['Nom_commune'].drop_duplicates()
choix_commune = st.sidebar.selectbox('Selectionnez votre commune:', commune)

theme = df["Thématique_POI"].drop_duplicates()
choix_theme = st.sidebar.selectbox('Sélectionnez votr type d itinéraire', theme) 



cartes = st.container()
with cartes:
    st.header('Carte des Points d intêtets selon la commune et le thème choisi')
    def intineraire (choix_commune,choix_theme):
        for i,value in enumerate (centroid['nom_com']):
          if choix_commune == value:
            com = centroid[centroid['nom_com'] == value]
        for i,value in enumerate (df['Nom_commune']):
            if choix_commune == value:
                df_com = df [df['Nom_commune'] == value]
        for i,value in enumerate (df_com['Thématique_POI']):
                if choix_theme == value:
                    theme = df_com [df_com['Thématique_POI'] == value]
        #Création de la carte
        for index, row in com.iterrows():
          maps= folium.Map(location=[row.loc['latitude'], row.loc['longitude']], tiles='cartodbpositron', zoom_start=13.5)
        for index, row in theme.iterrows():
            folium.Marker(location=[row.loc['Latitude'], row.loc['Longitude']], tooltip= row.loc['Nom_du_POI']).add_to(maps)
        return folium_static(maps)
                    
st.write(intineraire (choix_commune, choix_theme))