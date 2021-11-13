# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 17:27:47 2021

@author: Gilles
"""
# -*- coding: utf-8 -*-

#installation utile : pip install pipreqs pour le fichier requirements
#créer le fichier requirements.txt = d'abord aller dans le dossier du streamlit puis pipreqs ./
#installer pip install branca
#installer pip install streamlit_folium
#utiliser obligatoirement les crochets quand on a un accent dans les noms des variables

import streamlit as st
import pandas as pd
import numpy as np

from plotly.subplots import make_subplots
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

import folium
from streamlit_folium import folium_static

import openrouteservice 
from openrouteservice import client

df= pd.read_csv("Data/datatourisme.POI_OK_20210921.PACA.csv")
centroid= pd.read_csv("Data/CentroidFrance.csv")
df_habitant = df.groupby(['Nom_département']).agg({'Nbre_habitants' : 'sum','Nbre_touristes' : 'sum' })

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


#PIE PLOT
plotlypie_theme = px.pie(PACA_theme_count, 
                         values=PACA_theme_count, 
                         names=PACA_theme_count.index, 
                         title="Répartition des thèmes de POI")

plotlypie_theme.update_traces(textposition='outside', textinfo='percent')

st.plotly_chart(plotlypie_theme)
st.caption('Répartition des POIs du DataSet')

#BAR PLOT
fig,ax = plt.subplots()
ax = sns.countplot(x=df['Nom_département'],
                   hue=df['Thématique_POI'], 
                   palette='Set2')

plt.title("Répartitions de POI par Départements ")
ax.legend(bbox_to_anchor = (1, 1), 
          loc = 'upper right', 
          prop = {'size': 10})
plt.xticks(rotation=45)
st.pyplot(fig)

#BAR PLOT NB HABITANT
fig,ax = plt.subplots()
ax= df_habitant.plot.bar( y = ['Nbre_habitants','Nbre_touristes' ], 
                         rot= 30, color= ['wheat', 'salmon'],
                         label=['Nbre_habitants (en million)','Nbre_touristes(en million)'])
st.pyplot(fig)

#DROP DOWN MENU
commune = df['Nom_commune'].drop_duplicates()
choix_commune = st.sidebar.selectbox('Selectionnez votre commune:', commune)

theme = df["Thématique_POI"].drop_duplicates()
choix_theme = st.sidebar.selectbox('Sélectionnez votr type d itinéraire', theme) 

#AFFICHAGE DE LA CARTE
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
        return maps
                    
st.write(intineraire (choix_commune, choix_theme))
