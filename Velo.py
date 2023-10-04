#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
#import plotly_express as px

#df=pd.read_csv("velo_paris_20202023.csv")

st.title("Analyse du trafic cycliste à Paris")
st.sidebar.title("Sommaire")
pages=["Dataset principal",
       "Datasets secondaires", 
       "Exploration", 
       "DataVizualization", 
       "Modélisation"]
page=st.sidebar.radio("Aller vers", pages)

if page == pages[0] : 
  st.write("### Dataset principal")
   
  st.write("1. Source: Le jeu de données provient du site opendata.paris.")
     
  st.write("La Ville de Paris déploie depuis plusieurs années des compteurs vélo permanents  (site ou point de comptage) pour évaluer le développement de la pratique cycliste. Les compteurs sont situés sur des pistes cyclables et dans certains couloirs bus ouverts aux vélos. Les autres véhicules (ex : trottinettes…) ne sont pas comptés.")
  st.write("Remarque : Le nombre de compteurs évolue au fur et à mesure des aménagements cyclables. Certains compteurs peuvent être désactivés pour travaux ou subir ponctuellement une panne.")

if page == pages[1] : 
    st.write("### Datasets secondaires")
    st.write("1.Aperçu du fichier")
    st.dataframe(df.head(10))

    st.write("La taille du fichier est :",df.shape)
    st.dataframe(df.describe(include='all').T)

    if st.checkbox("Afficher les NaN"):
        nan_counts = df.isna().sum()
        nan_df = pd.DataFrame(nan_counts, columns=["Nombre de NaN"])
        st.dataframe(nan_df)


def DateMinMax_df(df_in):
    df_out = df_in.sort_values(by=['Date'], ascending=True)
    DateMin = df_out.Date.min().strftime('%d-%m-%Y')
    DateMax = df_out.Date.max().strftime('%d-%m-%Y')
    return DateMin, DateMax

def main():
    st.title("Affichage de la période couverte par le fichier")

    # Charger le fichier CSV
    df = pd.read_csv("nom_du_fichier.csv")
    
    # Conversion au format de date si nécessaire
    df['Date'] = pd.to_datetime(df['Date'])

    # Affichage de la période couverte
    if st.checkbox("Afficher la période couverte par le fichier"):
        dateMin, dateMax = DateMinMax_df(df)
        st.write("Les dates s'échelonnent du :", dateMin, "au", dateMax)

if __name__ == "__main__":
    main()


if page == pages[2] : 
  st.write("### Exploration")
  
if page == pages[3] : 
  st.write("### DataVizualization")

if page == pages[4] : 
    def st_plot_site_2023(df_src, df_pred, Mois, nom_compteur) :
    
        df_site_src = df_src[(df_src.Mois == Mois) & (df_src.nom_compteur == nom_compteur)]
        # affichage des mois en français
        locale.setlocale(locale.LC_TIME, 'fr_FR')
    
        mois = calendar.month_name[df_site_src.iloc[0].Mois].capitalize()
        site = df_site_src.iloc[0].nom_compteur
    
        fig, ax = plt.subplots(figsize = (20,7))   
        # données relevées
        ax.plot(df_site_src.Jour, df_site_src.sum_counts, 'b-', label='comptages réels')
        # prédictions
        df_site_pred = df_pred[(df_pred.Mois == Mois) & (df_pred["site_"+nom_compteur] == 1)]
        ax.plot(df_site_pred.Jour, df_site_pred.sum_counts, 'r-', label='prédictions')
    
        # affichage des jours du mois
        ax.set_xticks(range(1,max(df_site_src.Jour)+1))
        plt.ylabel('Nb de vélos par jour') 
        # déplacement du titre de l'axe Y vers la gauche
        ax.yaxis.set_label_coords(-0.05, 0.5)
        plt.title(f"Trafic cycliste parisien sur le mois de {mois} 2023\nSite de comptage : {site} ");
        plt.grid(True)
        plt.legend()
        plt.show()
        
    st.write("### Modélisation")
    df_group_par_j_2023 = pd.read_csv('df_group_par_jour_2023.csv')
    df_predict_2023 = pd.read_csv('df_pred_2023.csv')
    site = "180 avenue d'Italie N-S"
    mois = 4
    st_plot_site_2023(df_group_par_j_2023, df_predict_2023, mois, site)


    
    
