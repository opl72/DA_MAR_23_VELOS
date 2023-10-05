#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import pandas as pd
#import numpy as np
import matplotlib.pyplot as plt
#import seaborn as sns
#import plotly_express as px

# Config par defaut de l'appli
st.set_page_config(layout="wide", # affichage par défaut en mode wide
		   page_title="Trafic cycliste parisien", # titre de l'appli dans la barre du navigateur
		   page_icon=":bike:") # icone de l'appli dans la barre du navigateur

# mise en cache des ressources à charger
@st.cache_data
def load_and_cache(file_path):
	df = pd.read_csv(file_path)
	return df
# chargement et mise en cahe des fichiers utiles à la prédictions du trafic
df_group_par_j_2023 = load_and_cache('df_group_par_jour_2023.csv')
df_predict_2023 = load_and_cache('df_pred_2023.csv')

@st.cache_data
def plot_site_2023(df_src, df_pred, mois, numero_mois, nom_compteur) :
	# filtre sur les données du mois à afficher
	df_site_src = df_src[(df_src.Mois == numero_mois) & (df_src.nom_compteur == nom_compteur)]		
	# taille du graphe
	fig, ax = plt.subplots(figsize = (20,7))   
	# données relevées
	ax.plot(df_site_src.Jour, df_site_src.sum_counts, 'b-', label='comptages réels')
	# prédictions
	df_site_pred = df_pred[(df_pred.Mois == numero_mois) & (df_pred["site_"+nom_compteur] == 1)]
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



# SIDEBAR
st.sidebar.markdown("<b>Sommaire", unsafe_allow_html=True)
pages = ["Dataset principal", 
		 "Datasets secondaires", 
		 "Explorations", 
		 "Data Viz", 
		 "ML & Prédictions", 
		 "Perspectives"]
page = st.sidebar.radio("", pages)
st.sidebar.markdown("<br><br><b>Auteurs :</b><br>Cécile ALBET<br>  Olivier PELLETEY", unsafe_allow_html=True)
st.sidebar.markdown("Formation Data Analyst<br>Promotion Mars 2023", unsafe_allow_html=True)	
st.sidebar.image("logoDS.png", width=150)
st.markdown(
    """
    <style>
    /* Masquer la barre de défilement verticale de la barre latérale */
    .sidebar {
        overflow-y: hidden !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# TITRE
st.title("Analyse du trafic cycliste à Paris")

# GESTION DE CHAQUE PAGES
if page == pages[0] : 
	
	st.header("Dataset principal")
	
	st.markdown("<u>Source :</u><br>Le jeu de données provient du site : [opendata.paris.fr](https://opendata.paris.fr/explore/dataset/comptage-velo-donnees-compteurs/information/?disjunctive.id_compteur&disjunctive.nom_compteur&disjunctive.id&disjunctive.name)", unsafe_allow_html=True)    	
	st.markdown('<p style="text-align: justify;"><br>La Ville de Paris déploie depuis plusieurs années des compteurs vélo permanents  (site ou point de comptage) pour évaluer le développement de la pratique cycliste. Les compteurs sont situés sur des pistes cyclables et dans certains couloirs bus ouverts aux vélos. Les autres véhicules (ex : trottinettes…) ne sont pas comptés.</p>', unsafe_allow_html=True)	
	st.markdown('<p style="text-align: justify;"><u>Remarque :</u><br> Le nombre de compteurs évolue au fur et à mesure des aménagements cyclables. Certains compteurs peuvent être désactivés pour travaux ou subir ponctuellement une panne.</p>', unsafe_allow_html=True)





if page == pages[4] : 	
	
	st.header("Prédictions du trafic 2023")

	liste_sites = df_group_par_j_2023.nom_compteur.unique()
	site = st.selectbox('Sélectionnez un site de comptage :', liste_sites)
	
	liste_mois = ['Janvier', 'Février', 'Mars', 'Avril']
	#liste_mois_cap = [calendar.month_name[mois].capitalize() for mois in liste_mois]
	mois = st.selectbox('Sélectionnez le mois à prédir :', liste_mois)	
	numero_mois = liste_mois.index(mois.capitalize()) + 1
	
	plot_site_2023(df_group_par_j_2023, df_predict_2023, mois, numero_mois, site) 
