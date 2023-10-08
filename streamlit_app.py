#!/usr/bin/env python
# coding: utf-8

# tests lib
#import seaborn as sns
#import plotly_express as px
#import numpy as np
#from streamlit_extras.row import row
#from streamlit_extras.grid import grid
import time

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_option_menu import option_menu
import extra_streamlit_components as stx

# CONFIG DE L'APPARENCE DE L'APPLI
st.set_page_config(layout="wide", # affichage par défaut en mode wide
				   page_title="Trafic cycliste parisien", # titre de l'appli dans la barre du navigateur
				   initial_sidebar_state = "collapsed", # apparence de la barre latérale
				   page_icon=":bike:") # icone de l'appli dans la barre du navigateur


# MISE EN CACHE DES RESSOURCES UTILES
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


# BARRE LATERALE
image = "logoDS.png"
st.sidebar.markdown("Formation continue<br>Data Analyst<br>Promotion Mars 2023", unsafe_allow_html=True)	
st.sidebar.image(image, width=150)
st.sidebar.markdown("<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)	
st.sidebar.markdown("<b>Auteurs :</b><br>[Cécile ALBET](https://fr.linkedin.com/in/c%C3%A9cile-albet-322593143)<br>Olivier PELLETEY", unsafe_allow_html=True)


# TITRE
st.markdown('<p style="text-align:center; font-size:45px; font-weight:bold;">Exploration du trafic cycliste à Paris</p>', unsafe_allow_html=True)


# MENU HORIZONTAL
icons = ['bicycle', 'database', 'binoculars', 'bar-chart-line', 'cpu', 'question-diamond']
pages = ['Contexte', 'Jeux de données', 'Explorations', 'DataViz', 'Machine Learning', 'Perspectives']
page = option_menu(
				None, 
				options=pages,
				icons=icons,
				default_index=0, 						
				orientation="horizontal",
				styles={
				   "container": {"padding": "0!important", "background-color": "#0e1117"},##
				   "icon": {"color": "white", "font-size": "17px"}, 
				   "nav-link": {"font-size": "17px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},#
				   "nav-link-selected": {"font-size": "16px", "background-color": "#FF0000"} #
				      })


# GESTION DES PAGES

# PAGE 1 : Contexte
if page == pages[0] : 	
	# SLIDER HORIZONTAL
	stx.tab_bar(data=[stx.TabBarItemData(id=1, title="Contexte du projet", description="")], default=1)
	
	# CONTENU
	texte1="La ville de Paris a déployé des compteurs vélo permanents au cours des dernières années pour évaluer l'évolution de la pratique cycliste. Dans cette optique, nous avons entrepris une analyse des relevés horaires quotidiens sur la période allant du 1er janvier 2020 au 30 avril 2023. Notre objectif étant de proposer à la ville de Paris des pistes de réflexion concernant cette pratique."
	texte2="De plus, afin de mieux appréhender les tendances en matière de trafic cycliste, nous avons également examiné les données relatives à un autre mode de transport personnel, à savoir les trottinettes. Parallèlement, nous avons examiné les données relatives aux accidents corporels impliquant à la fois des vélos et des trottinettes dans cette même zone géographique."
	texte3="Enfin, nous nous sommes penchés sur divers modèles de Machine Learning dans le but de prédire l'évolution du trafic cycliste dans la ville."
		
	texte = texte1 + "<br><br>" + texte2 + "<br><br>" + texte3
	st.markdown(f'<p style="text-align: justify;">{texte}</p>', unsafe_allow_html=True)	 
	
	
# PAGE 2 : JDD
if page == pages[1] : 		
	# SLIDER HORIZONTAL
	tab_bar_id = stx.tab_bar(data=[
		   stx.TabBarItemData(id=1, title="Dataset principal", description=""),
		   stx.TabBarItemData(id=2, title="Datasets secondaires", description="")], default=1)	

	# CONTENU
	if tab_bar_id == "1" :
		#st.header("Dataset principal : trafic cycliste")
		st.header("Dataset principal : Comptages horaires de vélos")
		
		st.subheader('Source')
		st.markdown("Le jeu de données provient du site : [opendata.paris.fr](https://opendata.paris.fr/explore/dataset/comptage-velo-donnees-compteurs/)", unsafe_allow_html=True)    	
		st.markdown('<p style="text-align: justify;"><br>La Ville de Paris déploie depuis plusieurs années des compteurs vélo permanents  (site ou point de comptage) pour évaluer le développement de la pratique cycliste. Les compteurs sont situés sur des pistes cyclables et dans certains couloirs bus ouverts aux vélos. Les autres véhicules (ex : trottinettes…) ne sont pas comptés.</p>', unsafe_allow_html=True)	
		st.markdown('<p style="text-align: justify;"><u>Remarque :</u><br> Le nombre de compteurs évolue au fur et à mesure des aménagements cyclables. Certains compteurs peuvent être désactivés pour travaux ou subir ponctuellement une panne.</p>', unsafe_allow_html=True)

		
	if tab_bar_id == "2" :
		st.header("Datasets secondaires")
		st.subheader('1. Comptage multimodal')
		st.markdown("Le jeu de données provient du site : [opendata.paris.fr](https://opendata.paris.fr/explore/dataset/comptage-multimodal-comptages/information/?disjunctive.label&disjunctive.mode&disjunctive.voie&disjunctive.sens&disjunctive.trajectoire)", unsafe_allow_html=True)
	
		st.subheader('2. Accidents corporels de la circulation')
		st.markdown("Le jeu de données provient du site : [data.gouv.fr](https://www.data.gouv.fr/fr/datasets/base-de-donnees-des-accidents-corporels-de-la-circulation/)", unsafe_allow_html=True)
		
		st.subheader('3. Historique Météo de Paris')
		st.markdown("Le jeu de données provient du site : [historique-meteo.net](https://www.historique-meteo.net/france/ile-de-france/paris/)", unsafe_allow_html=True)
		
		
# PAGE 3 : Explorations
if page == pages[2] : 	
	# SLIDER HORIZONTAL
	tab_bar_id = stx.tab_bar(data=[
			stx.TabBarItemData(id=1, title="Outliers", description=""), 
			stx.TabBarItemData(id=2, title="Sites Multimodal", description=""),
			stx.TabBarItemData(id=3, title="Cartes du trafic", description="")], default=1)
	
	# CONTENU
	if tab_bar_id == "1" :
		tabs = st.tabs(["Dataset principal", "Dataset Multimodal"])
		# ONGLET 1
		with tabs[0] :		
			cols = st.columns([0.7505, 0.2495], gap="large")
			with cols[0] :
				st.image("Outliers_3.png")			
			with cols[1] :
				st.image("Outliers_1.png")
		# ONGLET 2
		with tabs[1] :	
			cols = st.columns([0.585, 0.415], gap="large")
			with cols[0] :
				st.image("Outliers_4.png")			
			with cols[1] :
				st.image("Outliers_2.png") 
				
			
	if tab_bar_id == "2" :
		st.header("Sites de comptage multimodal")		
		st.markdown('<p style="text-align: center;"><b>Sur les <font color="red">9</font> sites enregistrant des passages de vélos ou vélos+trottinettes, seuls <font color="red">5</font> sites arrivent à distinguer les vélos :</p>', unsafe_allow_html=True)
		st.image("SiteDeComptage_3.png", use_column_width="auto")			
		
		
	if tab_bar_id == "3" :
		st.header("Densité du trafic en 2023")		
		# chargement des cartes folium
		cols = st.columns([2, 0.5, 2], gap="large") # on créé 3 colonnes pour gérer le centrage des titres
		with open("carte_densite_trafic_par_an_par_moy_sans_Clustering_2023.html", 'r', encoding='utf-8') as f :
			with cols[0] :
				st.markdown('<p style="text-align: center;"><b>Sans clustering</p>', unsafe_allow_html=True)
				st.components.v1.html(f.read(), height=590, width=590)		
		# la colonne du milieu (invisible) sert juste à centrer les titres au dessus de chaque carte ;)
		with open("carte_densite_trafic_par_an_par_moy_avec_Clustering_2023.html", 'r', encoding='utf-8') as f : 
			with cols[2] :
				st.markdown('<p style="text-align: center;"><b>Avec clustering</p>', unsafe_allow_html=True)
				st.components.v1.html(f.read(), height=590, width=590)
		
		
# PAGE 4 : DataViz
if page == pages[3] : 
	# SLIDER HORIZONTAL
	tab_bar_id = stx.tab_bar(data=[stx.TabBarItemData(id=1, title="Data visualisations", description="")], default=1)	
	
	st.write("A compléter")


# PAGE 5 : ML
if page == pages[4] : 	
	# SLIDER HORIZONTAL
	tab_bar_id = stx.tab_bar(data=[
		   stx.TabBarItemData(id=1, title="Séries temporelles", description=""),
		   stx.TabBarItemData(id=2, title="Modélisations", description=""),
		   stx.TabBarItemData(id=3, title="Prédictions", description="")], default=1)

	# CONTENU
	if tab_bar_id == "1" :
		st.header("Séries temporelles")
		st.write("A compléter")
		
	if tab_bar_id == "2" :
		st.header("Modèles de Machine Learning")
		st.write("A compléter")
		
		options = st.multiselect(
			   'What are your favorite colors',
			      ['Green', 'Yellow', 'Red', 'Blue'],
					     ['Yellow', 'Red'])

		st.write('You selected:', options)
		
		with st.spinner("Predict en cours ..."):
			time.sleep(5)
			
		
	if tab_bar_id == "3" :
		st.header("Prédictions du trafic 2023")	
	
		liste_sites = df_group_par_j_2023.nom_compteur.unique()
		site = st.selectbox('Sélectionnez un site de comptage :', liste_sites)
		
		liste_mois = ['Janvier', 'Février', 'Mars', 'Avril']
		#liste_mois_cap = [calendar.month_name[mois].capitalize() for mois in liste_mois]
		mois = st.selectbox('Sélectionnez le mois à prédir :', liste_mois)	
		numero_mois = liste_mois.index(mois.capitalize()) + 1
		
		plot_site_2023(df_group_par_j_2023, df_predict_2023, mois, numero_mois, site) 
	
	
# PAGE 6 : Perspectives
if page == pages[5] :
	# SLIDER HORIZONTAL
	stx.tab_bar(data=[stx.TabBarItemData(id=1, title="Perspectives", description="")], default=1)	
	st.write("A compléter")	
	
	
if page == 'Test' :
	st.title("ZONE DE TESTS :)") 
	#st.write("---")	
	#st.info(f"{chosen_id=}")
	
	# Créer un slider horizontal
# 	valeur_slider = st.slider('Sélectionnez une valeur', min_value=0, max_value=100, value=50, step=1)
# 	st.write(f"Vous avez sélectionné : {valeur_slider}")
# 	
# 	mois = st.select_slider("", ['Janvier', 'Février', 'Mars', 'Avril'])
# 	st.write(f"Vous avez sélectionné : {mois}")
	
# 	random_df = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
# 	row1 = row(2, vertical_align="center")
# 	row1.dataframe(random_df, use_container_width=True)
# 	#row1.line_chart(random_df, use_container_width=True)
# 	row2 = row([2, 4, 1], vertical_align="bottom")
# 	row2.selectbox("Select Country", ["Germany", "Italy", "Japan", "USA"])
# 	row2.text_input("Your name")
# 	row2.button("Send", use_container_width=True)
	
	
# 	random_df = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
# 	my_grid = grid(2, [2, 4, 1], 1, 4, vertical_align="bottom")
# 	# Row 1:
# 	my_grid.dataframe(random_df, use_container_width=True)
# 	my_grid.line_chart(random_df, use_container_width=True)
# 	# Row 2:
# 	my_grid.selectbox("Select Country", ["Germany", "Italy", "Japan", "USA"])
# 	my_grid.text_input("Your name")
# 	my_grid.button("Send", use_container_width=True)
# 	# Row 3:
# 	my_grid.text_area("Your message", height=40)
# 	# Row 4:
# 	my_grid.button("Example 1", use_container_width=True)
# 	my_grid.button("Example 2", use_container_width=True)
# 	my_grid.button("Example 3", use_container_width=True)
# 	my_grid.button("Example 4", use_container_width=True)
# 	# Row 5 (uses the spec from row 1):
# 	with my_grid.expander("Show Filters", expanded=True):
# 	    st.slider("Filter by Age", 0, 100, 50)
# 	    st.slider("Filter by Height", 0.0, 2.0, 1.0)
# 	    st.slider("Filter by Weight", 0.0, 100.0, 50.0)
# 	my_grid.dataframe(random_df, use_container_width=True)
	
# 		my_grid = grid([0.438, 0.562], gap="medium")
# 		my_grid.image("SiteDeComptage_1.png")
# 		my_grid.image("SiteDeComptage_2.png")

	
		
	
# 	tab1, tab2 = st.tabs(["📈 Chart", "🗃 Data"])
# 	data = np.random.randn(10, 1)	
# 	tab1.subheader("A tab with a chart")
# 	tab1.line_chart(data)	
# 	tab2.subheader("A tab with the data")
# 	tab2.write(data)
# 	
# 	
# 	st.balloons()
# 	st.snow()
	
	
	
# 	progress_text = "Operation in progress. Please wait."
# 	my_bar = st.progress(0, text=progress_text)	
# 	for percent_complete in range(100):
# 	    time.sleep(0.01)
# 	    my_bar.progress(percent_complete + 1, text=progress_text)
# 	time.sleep(1)
# 	my_bar.empty()
# 	st.button("Rerun BAR PROGRESS")
	
	

	    
