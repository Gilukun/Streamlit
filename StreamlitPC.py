# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 17:27:47 2021

@author: Gilles
"""
# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
from plotly.subplots import make_subplots
import plotly.express as px
import seaborn as sns

import folium
from streamlit_folium import folium_static

import openrouteservice 
from openrouteservice import client

#Avant de lancer Streamlit installer : 

#Import et création des datasets 
df= pd.read_csv('Data/datatourisme.POI_OK_20210921.PACA.csv')
centroid= pd.read_csv('Data/CentroidFrance.csv')
PACA_theme_count = df['Thématique_POI'].value_counts()
df_habitant= df.groupby(['Nom_département']).agg({'Nbre_habitants' : 'sum','Nbre_touristes' : 'sum' })

intro = st.container()

with intro:
    st.title("Pytinéo")
    st.text('Pytinéo le renouveau de la création d intinéraire')

analysis = st.container()

with analysis:
    st.header("Analyse de données")
    st.write('Analyse des datasets pour définir notre projet')
    st.dataframe(data=df.head(10))


st.subheader('Répartition des POI')
pie= px.pie(PACA_theme_count, 
        values=PACA_theme_count, 
        names=PACA_theme_count.index,
        title="Répartition des thèmes de POI")
st.plotly_chart(pie)

st.subheader('Répartition des POIs par départements')
fig2, ax = plt.subplots()
ax = sns.countplot(x=df.Nom_département,
                   hue=df.Thématique_POI, 
                   palette='Set2')
ax.legend(loc='best', bbox_to_anchor=(0.5, 0., 0.5, 0.5))
st.pyplot(fig2)
        


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
          maps= folium.Map(location=[row.loc['latitude'], row.loc['longitude']], tiles='cartodbpositron', zoom_start=10)
        for index, row in theme.iterrows():
            folium.Marker(location=[row.loc['Latitude'], row.loc['Longitude']], tooltip= row.loc['Nom_du_POI']).add_to(maps)
        folium_static(maps)
        
st.write(intineraire(choix_commune, choix_theme))
            
