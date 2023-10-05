#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import pandas as pd
#import numpy as np
import matplotlib.pyplot as plt
#import seaborn as sns
#import plotly_express as px
from streamlit_option_menu import option_menu

# Config par defaut de l'appli
st.set_page_config(layout="wide", # affichage par défaut en mode wide
				   page_title="Trafic cycliste parisien", # titre de l'appli dans la barre du navigateur
				   initial_sidebar_state = "collapsed",
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

# 1. as sidebar menu
with st.sidebar :
    page = option_menu(
		'Sommaire', 
		['Contexte projet', 'JDD', 'Explorations', 'Data Viz', 'Modélisations', 'Perspectives'], 
        icons=['house', '', '', '', 'gear'], 
		menu_icon="cast", 
		default_index=0)
    

# 2. horizontal menu
# selected2 = option_menu(None, ["Home", "Upload", "Tasks", 'Settings'], 
#     icons=['house', 'cloud-upload', "list-task", 'gear'], 
#     menu_icon="cast", default_index=0, orientation="horizontal")
# selected2

# TITRE
st.markdown('<p style="text-align:center; font-size:45px; font-weight:bold;">Analyse du trafic cycliste à Paris</p>', unsafe_allow_html=True)


# 3. CSS style definitions
selected3 = option_menu(None, ["Home", "Upload",  "Tasks", 'Settings'], 
    icons=['house', 'cloud-upload', "list-task", 'gear'], 
    menu_icon="cast", default_index=0, orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "grey"},#fafafa
        "icon": {"color": "orange", "font-size": "25px"}, 
        "nav-link": {"font-size": "25px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "red"},
    }
)

# SIDEBAR
#st.sidebar.markdown("<b>Sommaire", unsafe_allow_html=True)
st.sidebar.markdown("<br><b>Auteurs :</b><br>Cécile ALBET<br>Olivier PELLETEY", unsafe_allow_html=True)
st.sidebar.markdown("Formation Data Analyst<br>Promotion Mars 2023", unsafe_allow_html=True)	
st.sidebar.image("logoDS.png", width=150)




# GESTION DE CHAQUE PAGES
if page == 'Contexte projet' : 
	st.write("Contexte")
	
	
if page == 'JDD' : 
	st.header("Dataset principal")
	
	st.markdown("<u>Source :</u><br>Le jeu de données provient du site : [opendata.paris.fr](https://opendata.paris.fr/explore/dataset/comptage-velo-donnees-compteurs/)", unsafe_allow_html=True)    	
	st.markdown('<p style="text-align: justify;"><br>La Ville de Paris déploie depuis plusieurs années des compteurs vélo permanents  (site ou point de comptage) pour évaluer le développement de la pratique cycliste. Les compteurs sont situés sur des pistes cyclables et dans certains couloirs bus ouverts aux vélos. Les autres véhicules (ex : trottinettes…) ne sont pas comptés.</p>', unsafe_allow_html=True)	
	st.markdown('<p style="text-align: justify;"><u>Remarque :</u><br> Le nombre de compteurs évolue au fur et à mesure des aménagements cyclables. Certains compteurs peuvent être désactivés pour travaux ou subir ponctuellement une panne.</p>', unsafe_allow_html=True)


if page == 'Data Viz' :
	# Créez une mise en page en colonnes avec st.beta_columns()
	col1, col2 = st.columns(2)  # 2 colonnes
	
	# Ajoutez du contenu à chaque colonne
	with col1:
	    st.header("Colonne 1")
	    st.write("Contenu de la colonne 1")
	
	with col2:
	    st.header("Colonne 2")
	    st.write("Contenu de la colonne 2")
	
	# Vous pouvez également ajouter plus de colonnes si nécessaire
	col3, col4 = st.columns(2)
	
	with col3:
	    st.header("Colonne 3")
	    st.write("Contenu de la colonne 3")
	
	with col4:
	    st.header("Colonne 4")
	    st.write("Contenu de la colonne 4")


if page == 'Modélisations' : 	
	st.title("Modélisations")
	st.header("1. Séries temporelles")
	st.header("2. Modèles de ML")
	st.header("3. Prédictions du trafic 2023")

	liste_sites = df_group_par_j_2023.nom_compteur.unique()
	site = st.selectbox('Sélectionnez un site de comptage :', liste_sites)
	
	liste_mois = ['Janvier', 'Février', 'Mars', 'Avril']
	#liste_mois_cap = [calendar.month_name[mois].capitalize() for mois in liste_mois]
	mois = st.selectbox('Sélectionnez le mois à prédir :', liste_mois)	
	numero_mois = liste_mois.index(mois.capitalize()) + 1
	
	plot_site_2023(df_group_par_j_2023, df_predict_2023, mois, numero_mois, site) 
