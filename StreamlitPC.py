# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 17:27:47 2021

@author: Gilles
"""
# -*- coding: utf-8 -*-

#installation utile : pip install pipreqs pour le fichier requirements (fichier obligatoire publier l'appli sur Streamlit)

#créer le fichier requirements.txt 
#1. Ouvrir une fenêtre CMD Prompt puis aller dans le dossier du cd /streamlit 
#2.taper:  pipreqs ./
#3. Le fichier sera créé dans le dossier streamlit

#installer pip install branca==0.3.1  pour eviter les soucis d'affichage avec Folium
#installer pip install streamlit_folium pour l'integration de Folium

#utiliser obligatoirement les crochets quand on a un accent dans les noms des variables

#pour lire le fichier py = cd Documents/OneDrive/DataScientest/Data  ensuite streamlit run StreamlitPC.py


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

from sklearn.cluster import KMeans

df= pd.read_csv("Data/datatourisme.POI_OK_20210921.PACA.csv")
centroid= pd.read_csv("Data/CentroidFrance.csv")
#df_habitant = df.groupby(['Nom_département']).agg({'Nbre_habitants' : 'sum','Nbre_touristes' : 'sum' })
#df[['Nbre_habitants','Nbre_touristes' ]] = df[['Nbre_habitants','Nbre_touristes' ]].astype(int)

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

#DROP DOWN MENU
commune = df['Nom_commune'].drop_duplicates()
choix_commune = st.sidebar.selectbox('Selectionnez votre commune:', commune)

theme = df["Thématique_POI"].drop_duplicates()
choix_theme = st.sidebar.selectbox('Sélectionnez votr type d itinéraire', theme) 

#AFFICHAGE DE LA CARTE
cartes = st.container()
with cartes:
    st.header('Carte des Points d intêrets selon la commune et le thème choisi')
    def intineraire (choix_commune,choix_theme):
        for i,value in enumerate (centroid['nom_com']):
          if choix_commune == value:
            com = centroid[centroid['nom_com'] == value]
          
        for i,value in enumerate (df['Nom_commune']):
            if choix_commune == value:
                df_com = df [df['Nom_commune'] == value]
            if choix_commune not in (df['Nom_commune'].values):
                st.write ("Cette commune n'est pas listée dans notre base de données")
                return  
            
        for i,value in enumerate (df_com['Thématique_POI']):
                if choix_theme == value:
                    theme = df_com [df_com['Thématique_POI'] == value]
                if choix_theme not in (df_com['Thématique_POI'].values):
                    st.write ("Ce thème n'est listé dans notre base de données pour cette commune")
                    return
   #création des clusters en utilisant le KMeans
    #On a une randomisation des résultats naturellement avec le KMeans
        X= theme[['Latitude', 'Longitude']]
        k = round((theme[['Latitude', 'Longitude']].shape[0])/5)
        kmeans = KMeans(k)
        kmeans.fit(X)
        clusters = kmeans.predict(X)
        theme['Clusters'] = clusters
        random = list(theme['Clusters'].sample(n=7, random_state=1).values) #On choisi un n= nombre de jour pour avoir un cluster par jour
        theme = theme.loc[theme['Clusters'].isin(random)]
    
        #Création de la carte
        for index, row in com.iterrows():
          maps= folium.Map(location=[row.loc['latitude'], row.loc['longitude']], tiles='cartodbpositron', zoom_start=10)
          color_list= ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'lightred', 'beige', 'darkblue', 'darkgreen', 'cadetblue', 'darkpurple','whitpink', 'lightblue', 'lightgreen', 'gray', 'black', 'lightgray']
          clusters_id = list(theme["Clusters"].unique())
          color_dic = dict(zip (clusters_id, color_list))
          theme['Couleur']= theme['Clusters'].map(color_dic)
          
        for i in theme.itertuples(): 
           folium.Marker(location=[i.Latitude, i.Longitude], 
                         tooltip= i.Nom_du_POI,
                         icon=folium.Icon(icon='bicycle', prefix="fa", color = i.Couleur)).add_to(maps)
        return maps
                    
st.write(intineraire (choix_commune, choix_theme))
