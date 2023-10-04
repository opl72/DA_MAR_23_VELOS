#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import calendar
import locale
#import plotly_express as px

@st.cache_data
def load_df():
	df_group_par_j_2023 = pd.read_csv('df_group_par_jour_2023.csv')
	df_predict_2023 = pd.read_csv('df_pred_2023.csv')
	return df_group_par_j_2023, df_predict_2023
	
@st.cache_data
def plot_site_2023(df_src, df_pred, Mois, nom_compteur) :
	mois = calendar.month_name[Mois].capitalize()    
	df_site_src = df_src[(df_src.Mois == Mois) & (df_src.nom_compteur == nom_compteur)]
			
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
	st.pyplot(fig)

try:
    	# affichage des mois en francais
	locale.setlocale(locale.LC_TIME, 'fr_FR')
except locale.Error:
    	# Si la locale n'est pas disponible sur le système, traitez l'exception ici
   	print("La locale 'fr_FR' n'est pas disponible sur ce système.")
	
st.title("Analyse du trafic cycliste à Paris")
st.sidebar.title("Sommaire")
pages = ["Dataset principal", "Datasets secondaires", "Exploration", "DataVisualization", "Modélisation"]
page = st.sidebar.radio("Aller vers", pages)

if page == pages[0] : 
	st.write("### Dataset principal")   
	st.write("1. Source: Le jeu de données provient du site opendata.paris.")     
	st.write("La Ville de Paris déploie depuis plusieurs années des compteurs vélo permanents  (site ou point de comptage) pour évaluer le développement de la pratique cycliste. Les compteurs sont situés sur des pistes cyclables et dans certains couloirs bus ouverts aux vélos. Les autres véhicules (ex : trottinettes…) ne sont pas comptés.")
	st.write("Remarque : Le nombre de compteurs évolue au fur et à mesure des aménagements cyclables. Certains compteurs peuvent être désactivés pour travaux ou subir ponctuellement une panne.")

if page == pages[4] : 	
	st.write("### Modélisation")
	st.write("### Prédictions du trafic 2023")
	df_group_par_j_2023, df_predict_2023 = load_df()
	liste_sites = df_group_par_j_2023.nom_compteur.unique()
	site = st.selectbox('Sélectionnez un site de comptage :', liste_sites)
	
	liste_mois = df_group_par_j_2023.Mois.unique()	
	liste_mois_cap = [calendar.month_name[mois].capitalize() for mois in liste_mois]
	mois = st.selectbox('Sélectionnez le mois à prédir :', liste_mois_cap)	
	index_du_mois = liste_mois_cap.index(mois.capitalize()) + 1
	plot_site_2023(df_group_par_j_2023, df_predict_2023, index_du_mois, site) 
