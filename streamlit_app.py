#!/usr/bin/env python
# coding: utf-8

# tests lib
#import seaborn as sns
#import plotly_express as px
#import numpy as np
#from streamlit_extras.row import row
#from streamlit_extras.grid import grid
#import time
#from sklearn.metrics import mean_squared_error
#from sklearn.metrics import r2_score


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_option_menu import option_menu
import extra_streamlit_components as stx
import joblib


# CHEMINS : DES IMAGES 
#			DES DATASETS CHARGÉS VIA JOBLIB 
path_image_2 = "im/im_2/"
path_image_3 = "im/im_3/"
path_image_4 = "im/im_4/"
path_image_5 = "im/im_5/"
path_joblib  = "joblib/"
path_csv 	 = "csv/"
text_color   = "#f63366"


# CONFIG DE L'APPARENCE DE L'APPLI
st.set_page_config(layout="wide", # affichage par défaut en mode wide
				   page_title="Trafic cycliste parisien", # titre de l'appli dans la barre du navigateur
				   initial_sidebar_state = "collapsed", # apparence de la barre latérale
				   page_icon=":bike:") # icone de l'appli dans la barre du navigateur


# MISE EN CACHE DES RESSOURCES UTILES
@st.cache_data
def load_joblib_and_cache(file_path) :
	try :
		path = path_csv + file_path + ".csv"		
		return pd.read_csv(path)
	except Exception as e :
		st.write("/!\ Exception dans la fonction load_joblib_and_cache : ", e)
		st.write("Chargement de ",file_path)
		return joblib.load(open(path_joblib + file_path, 'rb'))
	
# chargement et mise en cahe des fichiers utiles à la prédictions du trafic
df_group_par_j_2023 = load_joblib_and_cache('df_group_par_jour_2023')
df_predict_2023 = load_joblib_and_cache('df_pred_2023')
# chargement et mise en cahe des fichiers utiles au ML
# X_2020_2022_ohe = load_joblib_and_cache("X_2020_2022_ohe")
# y_2020_2022 = load_joblib_and_cache("y_2020_2022")
# X_2023_ohe = load_joblib_and_cache("X_2023_ohe")
# y_2023 = load_joblib_and_cache("y_2023")


# @st.cache_data
# def load_and_predict(path) :	
# 	try :
# 	 	model = joblib.load(open(path, 'rb'))
# 	 	# Prédit les valeurs sur l'ensemble de train / test
# 	 	y_train_pred = model.predict(X_2020_2022_ohe)
# 	 	y_test_pred = model.predict(X_2023_ohe)
# 	 	# Calcul de l'erreur quadratique moyenne (RMSE)
# 	 	rmse_train = mean_squared_error(y_2020_2022, y_train_pred, squared=False) 
# 	 	rmse_test = mean_squared_error(y_2023, y_test_pred, squared=False)
# 	 	#st.write(rmse_train, rmse_test)
# 	 	# Calcul du coefficient de détermination R²
# 	 	r2_train = r2_score(y_2020_2022, y_train_pred) 
# 	 	r2_test = r2_score(y_2023, y_test_pred) 
# 	 	#st.write(r2_train, r2_test)
# 	 	return rmse_train, rmse_test, r2_train, r2_test
# 	except Exception as e :
# 		st.write("/!\ Exception dans la fonction load_and_predict : ",e)
# 		st.write("Chargement de ",path, " impossible")
# 		return None 
# # chargement et mise en cahe des résultats du ML
# load_and_predict(path_joblib + "model_LR")
# load_and_predict(path_joblib + "model_DTR")
# load_and_predict(path_joblib + "model_GBR")
# load_and_predict(path_joblib + "model_RFR")
		

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
	plt.title(f"Trafic cycliste parisien sur le mois de {mois} 2023\nSite de comptage : {nom_compteur} ");
	plt.grid(True)
	plt.legend()	
	return fig
# chargement et mise en cahe des prédictions de mars 2023, pour le site 132 rue Lecourbe NE-SO
fig = plot_site_2023(df_group_par_j_2023, df_predict_2023, "Mars", 3, "132 rue Lecourbe NE-SO")


# GESTION DE LA SIDEBAR
# permet de figer la taille de la sidebar	
st.markdown("""<style>[data-testid="stSidebar"][aria-expanded="true"]{
           min-width: 180px;   
           max-width: 180px;  }""", unsafe_allow_html=True)  

# contenu de la sidebar
img_src="https://support.datascientest.com/uploads/default/original/1X/6bad50418375cccbef7747460d7e86b457dc4eef.png"
st.sidebar.markdown(f'<a href="https://datascientest.com/"><img src="{img_src}" width="150px" alt="DataScientest"></a>', unsafe_allow_html=True)
#  il faudrait essayer de charger avec l'image en local
#st.sidebar.markdown(f"""<a href="https://datascientest.com/"><img src="logoDS.jpg" width="150px" alt="DataScientest"></a>""", unsafe_allow_html=True)
st.sidebar.divider()
st.sidebar.markdown('Formation continue<br>[Data Analyst](https://datascientest.com/formation-data-analyst)<br>Promotion Mars 2023', unsafe_allow_html=True)
st.sidebar.divider()
st.sidebar.subheader("Auteurs :")
st.sidebar.markdown("[Cécile ALBET](https://fr.linkedin.com/in/c%C3%A9cile-albet-322593143)<br>[Olivier PELLETEY](https://fr.linkedin.com/)", unsafe_allow_html=True)


# TITRE : volontairement décalé vers le haut de la page (margin-top:-80px;)
st.markdown('<p style="text-align:center; font-size:45px; font-weight:bold; margin-top:-80px; margin-bottom:30px">Exploration du trafic cycliste à Paris</p>', unsafe_allow_html=True)

# MASQUER EN-TETE ET PIED DE PAGE : 2 méthodes
# hide_streamlit_style = """
#             <style>
#             #MainMenu {visibility: hidden;}			
#             footer {visibility: hidden;}
# 			header {visibility: hidden;}
#             </style>
#             """
# st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

hide_streamlit_style = """
            <style>
            [data-testid="stToolbar"] {visibility: hidden !important;}
            footer {visibility: hidden !important;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


# MENU HORIZONTAL
icons = ['bicycle', 'database', 'binoculars', 'bar-chart-line', 'cpu', 'question-diamond']
pages = ['Contexte', 'Jeux de données', 'Analyses', 'Data Viz', 'Machine Learning', 'Perspectives']
page = option_menu(
				None, 
				options=pages,
				icons=icons,
				default_index=0, 						
				orientation="horizontal",
				styles={
				   "container": {"padding": "0!important", "background-color": "#0e1117", "margin-left":"10px"},
				   "icon": {"color": "white", "font-size": "18px"}, 
				   "nav-link": {"font-size": "18px", "font-family":"Arial, sans-serif", "text-align": "center", "margin":"0px", "--hover-color": "#c1c0c0"},
				   "nav-link-selected": {"font-size": "16px", "font-family":"Arial, sans-serif", "background-color": "#f63366"} #FF0000
				      })


# GESTION DES PAGES

# PAGE 1 : Contexte
if page == pages[0] : 	
	# SLIDER HORIZONTAL
	stx.tab_bar(data=[stx.TabBarItemData(id=1, title="Contexte du projet", description="")], default=1)
	
	# CONTENU 
	st.markdown("""
				 <p style="text-align: justify;">
				 <br>La ville de Paris a déployé des compteurs vélo permanents au cours des dernières années pour évaluer l'évolution de la pratique cycliste. Dans cette optique, nous avons entrepris une analyse des relevés horaires quotidiens sur la période allant du <span style="color: #f63366;">1er janvier 2020</span> au <span style="color: #f63366;">30 avril 2023</span>. Notre objectif étant de proposer à la ville de Paris des pistes de réflexion concernant cette pratique.
				<br><br>De plus, afin de mieux appréhender les tendances en matière de trafic cycliste, nous avons également examiné les données relatives à un autre mode de transport personnel, à savoir les trottinettes. Parallèlement, nous avons examiné les données relatives aux accidents corporels impliquant à la fois des vélos et des trottinettes dans cette même zone géographique.
				<br><br>Enfin, nous nous sommes penchés sur divers modèles de Machine Learning dans le but de prédire l'évolution du trafic cycliste dans la ville.
				 </p>
				 """, unsafe_allow_html=True)	 

	
# PAGE 2 : JDD
if page == pages[1] : 		
	# SLIDER HORIZONTAL
	tab_bar_id = stx.tab_bar(data=[
		   stx.TabBarItemData(id=1, title="Dataset principal", description=""),
		   stx.TabBarItemData(id=2, title="Datasets secondaires", description="")], default=1)	

	# ONGLET 1 : Dataset principal
	if tab_bar_id == "1" :
		st.markdown('<p style="text-align:left; font-size:18px;font-family:Arial;"><b>Dataset principal : Comptages horaires des vélos</p>', unsafe_allow_html=True)
		
		st.markdown("""<p style="text-align:left; padding-left:15px;">Le jeu de données provient du site : <a href="https://opendata.paris.fr/explore/dataset/comptage-velo-donnees-compteurs/" target="_blank">opendata.paris.fr</a></p>""", unsafe_allow_html=True) 	
		st.markdown('<p style="text-align: justify;padding-left:15px;">La ville de Paris déploie depuis plusieurs années des compteurs vélo permanents  (site ou point de comptage) pour évaluer le développement de la pratique cycliste. Les compteurs sont situés sur des pistes cyclables et dans certains couloirs bus ouverts aux vélos. Les autres véhicules (ex : trottinettes…) ne sont pas comptés.</p>', unsafe_allow_html=True)	
		st.markdown("""<p style="text-align: left;padding-left:15px;"><u>Remarque :</u><br> Le nombre de compteurs évolue au fur et à mesure des aménagements cyclables. Certains compteurs peuvent être désactivés pour travaux ou subir ponctuellement une panne.</p>""", unsafe_allow_html=True)
		
		cols = st.columns([100, 50], gap="large")
		with cols[0] :
			st.image(path_image_2 + "PbTechniqueSiteComptagesParis.jpg", use_column_width=True)
		
	# ONGLET 2 : Datasets secondaires
	if tab_bar_id == "2" :
		st.markdown('<p style="text-align:left; font-size:18px; font-family:Arial;"><b>Datasets secondaires</p>', unsafe_allow_html=True)
		st.markdown('<p style="text-align:left; font-size:16px; font-family:Arial; padding-left:15px;"><b>1. Comptage multimodal</p>', unsafe_allow_html=True)
		st.markdown("""<p style="text-align:left; padding-left: 30px;">Le jeu de données provient du site : <a href="https://opendata.paris.fr/explore/dataset/comptage-multimodal-comptages/information/?disjunctive.label&disjunctive.mode&disjunctive.voie&disjunctive.sens&disjunctive.trajectoire" target="_blank">opendata.paris.fr</a></p>""", unsafe_allow_html=True)	
		st.markdown('<p style="text-align:left; font-size:16px; font-family:Arial; padding-left:15px;"><br><b>2. Accidents corporels de la circulation en 2021</p>', unsafe_allow_html=True)
		st.markdown("""<p style="text-align:left; padding-left: 30px;">Le jeu de données provient du site : <a href="https://www.data.gouv.fr/fr/datasets/base-de-donnees-des-accidents-corporels-de-la-circulation/" target="_blank">data.gouv.fr</a></p>""", unsafe_allow_html=True)
		st.markdown('<p style="text-align:left; font-size:16px; font-family:Arial; padding-left:15px;"><br><b>3. Historique Météo de Paris</p>', unsafe_allow_html=True)
		st.markdown("""<p style="text-align: left; padding-left: 30px;">Le jeu de données provient du site : <a href="https://www.historique-meteo.net/france/ile-de-france/paris/" target="_blank">historique-meteo.net</a></p>""", unsafe_allow_html=True)
				
		
# PAGE 3 : Analyses
if page == pages[2] : 	
	# SLIDER HORIZONTAL
	tab_bar_id = stx.tab_bar(data=[
			stx.TabBarItemData(id=1, title="Outliers", description=""), 
			stx.TabBarItemData(id=2, title="Sites multimodaux", description=""),
			stx.TabBarItemData(id=3, title="Cartes du trafic", description="")], default=1)
	
	# ONGLET 1 : OUTLIERS
	if tab_bar_id == "1" :
		tabs = st.tabs(["Dataset principal", "Dataset multimodal"])
		
		# TAB 1 : Dataset principal
		with tabs[0] :		
			cols = st.columns([200, 100], gap="small")
			with cols[0] :
				st.image(path_image_3+"Outliers_3.png", use_column_width=True)	
				st.write('<style>img {vertical-align: bottom;}</style>', unsafe_allow_html=True)
			with cols[1] :
				st.image(path_image_3+"Outliers_1.png", use_column_width=True)
				st.write('<style>img {vertical-align: bottom;}</style>', unsafe_allow_html=True)
						
		# TAB 2 : Dataset Multimodal
		with tabs[1] :				
			cols = st.columns([157, 100], gap="small")
			with cols[0] : st.image(path_image_3+"Outliers_4.jpg", use_column_width=True)	
			with cols[1] : st.image(path_image_3+"Outliers_2.png", use_column_width=True)
				
	# ONGLET 2 : SITES MULTIMODAUX		
	if tab_bar_id == "2" :
		st.markdown('<p style="text-align:left; font-size:18px; font-family:Arial;"><b>Sites de comptages multimodaux</p>', unsafe_allow_html=True)
		cols = st.columns([125, 1150, 125], gap="small")
		with cols[1] : 
			st.image(path_image_3+"SiteDeComptage_3.png", use_column_width=True)
			st.markdown('<p style="text-align:center;">Sur les <span style="color: #f63366;">9</span> sites enregistrant des passages de vélos ou vélos+trottinettes, seuls <b><span style="color: #f63366;">5</span></b> sites arrivent à distinguer les vélos</p>', unsafe_allow_html=True)
		
	# ONGLET 3 : CARTES DU TRAFIC
	if tab_bar_id == "3" :		
		st.markdown('<p style="text-align:left; font-size:18px; font-family:Arial;"><b>Densité du trafic cycliste en 2023</p>', unsafe_allow_html=True)
		# chargement des cartes folium
		#cols = st.columns([44, 12, 44], gap="large") # on créé 3 colonnes pour gérer le centrage des titres	
		cols = st.columns([590, 150, 590], gap="small") # on créé 3 colonnes pour gérer le centrage des titres
		with cols[0] :
			with st.form("carte1") :					
				st.markdown('<div style="text-align: left;"><b><span style="color: #f63366;">Sans</span></b> clustering</div>', unsafe_allow_html=True)
				with open(path_image_3+"carte_densite_trafic_par_an_par_moy_sans_Clustering_2023.html", 'r', encoding='utf-8') as f1 :				
					st.components.v1.html(f1.read(), height=520)#, width=580, height=530
				st.form_submit_button()			
				
		# la colonne du milieu (invisible) sert juste à centrer les titres au dessus de chaque carte ;)
		with cols[1] : st.markdown("""<style>[data-testid="baseButton-secondaryFormSubmit"]{display:none;}""", unsafe_allow_html=True) 			
		
		with cols[2] :				
			with st.form("carte2") :						
				st.markdown('<div style="text-align: left;"><b><span style="color: #f63366;">Avec</span></b> clustering</div>', unsafe_allow_html=True)
				with open(path_image_3+"carte_densite_trafic_par_an_par_moy_avec_Clustering_2023.html", 'r', encoding='utf-8') as f2 : 					
					st.components.v1.html(f2.read(), height=520)#, width=580, height=530
				st.form_submit_button()
			

		
# PAGE 4 : DataViz
if page == pages[3] : 
	# SLIDER HORIZONTAL
	tab_bar_id = stx.tab_bar(data=[
		stx.TabBarItemData(id=1, title="Trafic cycliste cumulé", description=""),
		stx.TabBarItemData(id=2, title="Trafic vélos vs. trottinettes", description=""),
		stx.TabBarItemData(id=3, title="Evolution des accidents en 2021", description=""),
		stx.TabBarItemData(id=4, title="Cartes des accidents", description="")
		], default=1)	
	
	# ONGLET 1 : Trafic cycliste cumulé	
	if tab_bar_id == "1" :
		cols = st.columns([325, 845, 325], gap="small")
		with cols[1] :
			st.image(path_image_4+"GrapheCumuléVélos.png") 
		
	# ONGLET 2 : Trafic vélos vs. trottinettes
	if tab_bar_id == "2" :
		tabs = st.tabs(["Semaine", "Week-end"])
		# TAB 1 : SEMAINE
		with tabs[0] :	
			cols = st.columns([95, 5], gap="small") 
			with cols[0] : st.image(path_image_4+"TraficVéloParHeureSemaine.png")			
			cols = st.columns([95, 5], gap="small") 
			with cols[0] : st.image(path_image_4+"TraficTrotParHeureSemaine.png")
		# TAB 2 : WE
		with tabs[1] :	
			cols = st.columns([495, 505], gap="medium") 
			with cols[0] : st.image(path_image_4+"TraficVéloParHeureWE.png")
			with cols[1] : st.image(path_image_4+"TraficTrotParHeureWE.png")
		
	# ONGLET 3 : Evolution des accidents en 2021
	if tab_bar_id == "3" :				
		tabs = st.tabs(["Par mois", "Par heure"])
		# TAB 1 : MENSUEL
		with tabs[0] :
			cols = st.columns(2, gap="small")
			with cols[0] : 
				st.markdown('<p style="text-align: left;"><b>Trafic cycliste mensuel</p>', unsafe_allow_html=True)
				st.image(path_image_4+"TraficVélo2021_2.png", use_column_width=True)	
			with cols[1] : 
				st.markdown('<p style="text-align: left;"><b>Nombre de vélos impliqués dans des accidents corporels, par mois</p>', unsafe_allow_html=True)
				st.image(path_image_4+"AccVélos2021_2.png", use_column_width=True)				
		# TAB 2 : HORAIRE
		with tabs[1] :
			cols = st.columns(2, gap="small")
			with cols[0] : 
				st.markdown('<p style="text-align: left;"><b>Trafic cycliste horaire</p>', unsafe_allow_html=True)
				st.image(path_image_4+"TraficVéloParHeureSemaineWE.png", use_column_width=True)	
			with cols[1] : 
				st.markdown('<p style="text-align: left;"><b>Nombre de vélos impliqués dans des accidents corporels, par heure</p>', unsafe_allow_html=True)
				st.image(path_image_4+"TraficVéloAccParHeureSemaineWE.png", use_column_width=True)
						
	# ONGLET 4 : Carte des accidents
	if tab_bar_id == "4" :	
		#cols = st.columns([90, 3, 90], gap="small") # on créé 3 colonnes pour gérer le centrage des titres	
		cols = st.columns([690, 15, 690], gap="small") # on créé 3 colonnes pour gérer le centrage des titres	
		with cols[0] :
			with st.form("carte3") :	
				st.markdown('<p style="text-align: left;"><b>Carte des vélos impliqués dans des accidents corporels en 2021, par arrondissement</p>', unsafe_allow_html=True)
				with open(path_image_4+"carte_acc_velos_par_arrond_2021.html", 'r', encoding='utf-8') as f1 :				
					st.components.v1.html(f1.read(), height=540)	#
				#st.image(path_image_4+"colormap.jpg", use_column_width=True)
				st.form_submit_button()	
			
		with cols[1] : st.markdown("""<style>[data-testid="baseButton-secondaryFormSubmit"]{display:none;}""", unsafe_allow_html=True) 		
		
		with cols[2] :
			with st.form("carte4") :	
				st.markdown('<p style="text-align: left;"><b>Carte des vélos impliqués dans des accidents corporels en 2021, par coordonnées gps</p>', unsafe_allow_html=True)
				with open(path_image_4+"carte_acc_velos_2021.html", 'r', encoding='utf-8') as f2 :			
					st.components.v1.html(f2.read(), height=540)	#, width=690
				#st.image(path_image_4+"colormap_vide.jpg", use_column_width=True)
				st.form_submit_button()		
					
		st.markdown("#  #") # ligne vide
		cols = st.columns([690, 15, 690], gap="small")
		with cols[0] :
			with st.form("carte5") :
				st.markdown('<p style="text-align: left;"><b>Trafic cycliste par site en 2023</p>', unsafe_allow_html=True)
				with open(path_image_4+"carte_densite_trafic_par_an_par_sum_sans_Clustering_2023_2.html", 'r', encoding='utf-8') as f3 :			
					st.components.v1.html(f3.read(), height=540)#, width=590
				st.form_submit_button()		

# PAGE 5 : ML
if page == pages[4] : 	
	# SLIDER HORIZONTAL
	tab_bar_id = stx.tab_bar(data=[
		   stx.TabBarItemData(id=1, title="Séries temporelles", description=""),
		   stx.TabBarItemData(id=2, title="Modélisations", description=""),
		   stx.TabBarItemData(id=3, title="Prédictions", description="")], default=1)

	# ONGLET 1 : Séries temporelles
	if tab_bar_id == "1" :
		tabs = st.tabs(["Analyses", "Prédictions"])
		# TAB 1 : Décomposition
		with tabs[0] :
			st.markdown('<p style="text-align: left;font-size:18px; font-family:Arial;"><b>Décomposition saisonnière avec modèle multiplicatif</p>', unsafe_allow_html=True)
			cols = st.columns(3, gap="small")
			with cols[0] :
				st.markdown('<p style="text-align: left;">Par mois, du 01/01/2020 au 30/04/2023</p>', unsafe_allow_html=True)
				st.image(path_image_5+"TimeSeriesParMois.png", use_column_width=True)
			with cols[1] :
				st.markdown('<p style="text-align: left;">Par semaine, du 01/01/2020 au 30/04/2023</p>', unsafe_allow_html=True)
				st.image(path_image_5+"TimeSeriesParSem2020-2023.png", use_column_width=True)
			with cols[2] :
				st.markdown('<p style="text-align: left;">Par semaine, du 01/01/<span style="color: #f63366;">2021</span> au 30/04/2023</p>', unsafe_allow_html=True)
				st.image(path_image_5+"TimeSeriesParSem2021-2023.png", use_column_width=True)
		# TAB 2 : Prédictions	
		with tabs[1] :
			st.markdown('<span style="font-size:18px;font-family:Arial;"><b>Modèle </span>$$\it SARIMA(𝑝,d,𝑞)(𝑃,D,𝑄)_{k=12}$$', unsafe_allow_html=True)
						
			cols = st.columns(3, gap="small")
			with cols[0] :
				st.markdown('<p style="text-align: left;">Evolutions sur des données mensuelles de 2020 à 2023</p>', unsafe_allow_html=True)
				st.image(path_image_5+"SarimaParMois.png", use_column_width=True)
			with cols[1] :
				st.markdown('<p style="text-align: left;">Evolutions sur des données hebdomadaires de 2020 à 2023</p>', unsafe_allow_html=True)
				st.image(path_image_5+"SarimaParSem2020-2023.png", use_column_width=True)
			with cols[2] :
				st.markdown('<p style="text-align: left;">Evolutions sur des données hebdomadaires de <span style="color: #f63366;">2021</span> à 2023</p>', unsafe_allow_html=True)
				st.image(path_image_5+"SarimaParSem2021-2023.png", use_column_width=True)
	
	# ONGLET 2 : Modélisations
	if tab_bar_id == "2" :
		st.markdown("""<p style="text-align:left; font-size:18px; font-family:Arial;"><b>Modélisations réalisées avec les paramètres suivants :</p>""", unsafe_allow_html=True)					  
		st.markdown("""
					  <ul style="list-style-type:disclosure-closed;padding-left:30px;margin-bottom:-10px;">
						  <li>Ajout de nouvelles variables explicatives (vacances, météo, jours fériés, confinement)</li>
						  <li>Compteurs (nom_compteur) communs entre 2020 et 2023</li>
						  <li>Aggrégation des comptages de chaque site par jour</li>
						  <li>Jeu d'entraînement sur un historique de 3 ans (2020 à 2022)
						  <li>Jeu de test sur 4 mois (01/01 au 30/04/2023)</li>
					  </ul>
				  """, unsafe_allow_html=True)		
		st.divider()
		
		cols = st.columns([3, 45, 3, 50], gap="medium")
		with cols[0] : on_1 = st.toggle(label="collapsed", key="toggle_1", value=True, label_visibility="collapsed")
		with cols[1] : st.markdown('<span style="color:#f63366; text-align:left; font-size:16px; margin-bottom:5px">Dataset source</span>', unsafe_allow_html=True)		
		with cols[2] : on_2 = st.toggle(label="collapsed", key="toggle_2", value=True, label_visibility="collapsed")
		with cols[3] : st.markdown('<span style="color:#f63366; text-align:left; font-size:16px; margin-bottom:5px">Mesures de performance</span>', unsafe_allow_html=True)
		
		cols = st.columns([48, 53], gap="medium")
		with cols[0] :
			if on_1 : st.dataframe(df_group_par_j_2023, 
	 							width=None, 
	 							height=275, 
	 							use_container_width=True, 
	 							hide_index=True, 
	 							column_order=None, 
	 							column_config={"Annee":st.column_config.NumberColumn("Année",format="%d"),
										   "":st.column_config.NumberColumn("",format="%d"),# modif du format d'affichage de la colonne 'index' du df
										   "Jour":st.column_config.NumberColumn("Jr"),
										   "jour_semaine_numero":st.column_config.NumberColumn("no_jr"),
										   "jour_we":st.column_config.NumberColumn("jr_we") })
			with cols[1] :
				if on_2 :
						data = {
						    'Modèle': ['Linear Regression', 'Decision Tree Regressor', 'Gradient Boosting Regressor', 'Random Forest Regressor'],
						    'RMSE train': [628, 253, 698, 117],
							'RMSE test': [616, 670, 818, 607],
						    'R² train': [0.76, 0.96, 0.71, 0.99],
							'R² test': [0.79, 0.76, 0.64, 0.80],
							'Perf': [False, False, False, True]
							#'Perf':['   ++', '   ++', '   +', '   +++']
							}
						st.dataframe(data, 
                                     use_container_width=True, 
                                     column_config={"R² train":st.column_config.ProgressColumn("R² train", min_value=0, max_value=1, format="%.2f"),
                                                    "R² test":st.column_config.ProgressColumn("R² test", min_value=0, max_value=1, format="%.2f"),
                                                    "Perf":st.column_config.CheckboxColumn("Choix", help=None, default=False) })
				
	# ONGLET 3 : Prédictions
	if tab_bar_id == "3" :
		st.markdown('<p style="text-align:left; font-size:18px; font-family:Arial;"><b>Prédictions du trafic 2023</p>', unsafe_allow_html=True)
		cols = st.columns([150, 50], gap="small")
		with cols[0] :
			# traitement de la liste des sites
			def site_format(option):
				return f"site : {option}"
			liste_sites = df_group_par_j_2023.nom_compteur.unique()
			st.markdown('<div style="color:#f63366; text-align:left; font-size:14px; margin-bottom:5px">Sélectionnez un site de comptage :</div>', unsafe_allow_html=True)
			site = st.selectbox(label="je masque le label", label_visibility="collapsed", format_func=site_format, options=liste_sites, index=5)
			# traitement de la liste des mois
			def mois_format(option):
				return f"{option} 2023"
			liste_mois = ['Janvier', 'Février', 'Mars', 'Avril']
			st.markdown('<div style="color:#f63366; text-align:left; font-size:14px; margin-bottom:5px">Sélectionnez le mois à prédir :</div>', unsafe_allow_html=True)
			mois = st.selectbox(label="je masque le label", label_visibility="collapsed", format_func=mois_format, options=liste_mois, index=2)  
			numero_mois = liste_mois.index(mois.capitalize()) + 1			
			# init du graphique
			fig = plot_site_2023(df_group_par_j_2023, df_predict_2023, mois, numero_mois, site)
		# affichage du graphique
		cols = st.columns([150, 50], gap="small")
		with cols[0] :
			st.pyplot(fig, clear_figure=True, use_container_width=True)		
		with cols[1] :
			if numero_mois == 1 :
				st.image(path_image_5+"Greves_202301.jpg") 
			elif numero_mois == 2 :
				st.image(path_image_5+"Greves_202302.jpg") 
			elif numero_mois == 3 :
				st.image(path_image_5+"Greves_202303.jpg") 
			elif numero_mois == 4 :
				st.image(path_image_5+"Greves_202304.jpg")
					
		
# PAGE 6 : Perspectives
if page == pages[5] :
	# SLIDER HORIZONTAL
	stx.tab_bar(data=[stx.TabBarItemData(id=1, title="", description="")], default=0)	# on affiche juste la barre rouge sans item
	
	st.markdown("""<blockquote>
			 <ul style="list-style-type:disclosure-closed;margin-top:20px;">
			    <li style="margin-bottom: 10px;">Le projet a nécessité beaucoup de rigueur...</li>
				<li style="margin-bottom: 10px;">Des contraintes rencontrées au niveau de la qualité des données, rendant les explorations chronophages.</li>
				<li style="margin-bottom: 10px;">Quelques pistes pour améliorer les prédictions :</li>
				<ul style="list-style-type:disc;padding-left:40px;">
					<li style="margin-bottom: 10px;">Approfondir la sélection des compteurs et leur granularité temporelle,</li>
					<li style="margin-bottom: 10px;">Intégrer l'influence de la période 2020 et des grèves de 2023,</li>							   
					<li style="margin-bottom: 10px;">Créer de nouvelles variables explicatives,</li>	
                    <li style="margin-bottom: 10px;">Tester d'autres modèles de ML et leurs hyperparamètres...</li>
				</ul>							
                <li>Meilleure prise de décisions opérationnelles et budgétaires.</li>
                <li>Optimisation de la gestion des infrastructures de transport parisien.</li>
			</ul>
				  </blockquote>""", unsafe_allow_html=True)	
			  
	
	
	# st.divider()
	# with st.expander("A ajouter si on a le temps !"):
		# "- La pratique nous permettra sans doute d’être xxx à l’avenir. Il faudra toutefois rester vigilant sur le fait qu’il convient de garder un oeil neuf et sans a priori sur les données (cas outliers)."
		# "- Le gain en efficacité vient sans doute du fait que nous saurons plus vite changer notre fusil d’épaule face aux problématiques rencontrées."
		# "- Nous avons été ambitieux en introduisant de nouvelles thématiques dans notre projet et n’avons pas pu rendre un travail aussi parfait que nous l’aurions souhaité mais fait le choix de nous laisser guider par les données et d’accepter l’imperfection."
		# "- Nous n’avons qu’une envie, explorer de nouveaux datasets pour progresser encore..."
	
	# with st.expander("A l'oral"):
            # "1.Le projet a nécessité beaucoup de rigueur..."
            # "2.Des contraintes rencontrées au niveau de la qualité des données, rendant les explorations chronophages."
            # "   En raison de :"
            # "       a-l'absence de méta-données," 
            # "		b-des caractéristiques internes des compteurs non permanente dans le temps (nom des sites, id des compteurs),"
            # "		c-la répartition hétérogène des sites (flagrant par arrondissement)."
            # "3.Il faudrait envisager des pistes pour améliorer les prédictions actuelles qui ne sont pas à la hauteur de nos espérances :"
            # "       a-En combinant une sélection judicieuse des compteurs avec la granularité temporelle adaptée"
            # "       b-les modèles de prédiction du trafic seraient en mesure de mieux capter les tendances et les variations du trafic."
            # "       (Une sélection + approfondie des compteurs et de leur granularité temporelle : elle a un impact sur la performance des modèles)"
            # "       c-Intégrer dans nos futures modélisations l'influence de la période 2020 et des grèves de 2023 : en commencant par prendre un historique complet de 2023"
            # "		d-Mettre en place de nouvelles variables explicatives comme les jours de grèves"
            # "		e-Tester l'effet d'un découpage des variables à l’aide de la méthode des moyennes mobiles"		
            # "4.Améliorations permettant ainsi une meilleure prise de décisions opérationnelles et budgétaires."
            # "5.Ce qui optimiserait la gestion des infrastructures de transport parisien."
		 
         
	# with st.expander("Conclusion du rapport"):
		# """Pour conclure ces différents travaux d’analyses et de visualisations de données, il nous semble pertinent
	# d’évoquer les contraintes rencontrées durant le projet . Nous ferons d’abord un focus sur la qualité des
	# données du dataset principal puis aborderons les difficultés rencontrées lors des travaux relatifs au
	# Machine Learning."""
	
		# """Tout d’abord, les différentes analyses réalisées nous ont permis de constater différentes difficultés relatives
		# à la qualité des données du Dataset « Comptage vélos-Compteurs » impactant ainsi leur pertinence.
		# Concernant les jeux de données, nous avons déploré l’absence de description des métadonnées et la
		# présence dans les datasets de variables différentes selon les années."""
		
		# """Concernant les sites de comptage, nous avons relevé un défaut de permanence dans le temps de leurs
		# caractéristiques avec des changements de dénomination, de coordonnées géographiques…
		# Afin de disposer de comptage vélos horaires représentatifs du trafic sur l’ensemble de son territoire, il
		# serait pertinent que la Ville de Paris installe des sites de comptage dans chacun des arrondissements en
		# veillant à équilibrer le nombre de compteurs par arrondissement."""
		
		# """Un travail plus approfondi sur la sélection des sites de comptage pour alimenter nos modèles de ML aurait
		# été nécessaire. En effet, nous avons vu que la granularité des données avait un impact direct sur les
		# résultats obtenus (agrégation par jour), aussi bien en termes de performance qu'en terme de temps de
		# traitement, voire de puissance de calculs."""
		
		# """Nous sommes persuadés que prendre en compte les compteurs ayant enregistré le même nombre de
		# relevés sur une période de 3 ans et 4 mois (période utilisée pour notre jeu d'entrainement et de test) aurait
		# permis d'avoir des résultats plus concluant lors de nos tests avec les time series.
		# Les prédictions obtenues à l’issue de nos travaux ne sont pas à la hauteur de nos espérances. En cause,
		# une année 2020 très particulière en raison du confinement du 1er trimestre, au même titre que les
		# épisodes de grèves rencontrées sur le 1er trimestre 2023.
		# Il serait donc tout à fait légitime de se demander s’il n’aurait pas été préférable de retirer ces données de
		# notre modèle d’apprentissage ? La réponse est simplement « Non » !
		# Le modèle a besoin de se nourrir d’une certaine quantité (masse) de données pour pouvoir améliorer son
		# apprentissage, et ses prédictions, afin d’être plus performant."""
		
		# """Tout porte à croire que la récupération d’un historique plus important sur l’année 2023 (de mai à octobre
		# par exemple) nous aurait permis d'améliorer la performance de nos modèles.
		# Nous aurions également aimé avoir le temps de travailler sur une autre utilisation des variables
		# temporelles sur nos différents modèles de ML. Par exemple, voir l'effet d'un découpage des variables à
		# l’aide de la méthode des moyennes roulantes."""
		
		# """L'utilisation de nouvelles variables explicatives, comme les jours de grève, aurait pu être une nouvelle piste
		# intéressante à explorer en ce qui concerne le travail de modélisation.
		# Les suites à donner à ce projet, dans le but principal de pouvoir aider au mieux la mairie de Paris dans
		# d’éventuelles améliorations à apporter sur les différents endroits cyclables de la ville, serait sans aucun
		# doute de poursuivre nos travaux de modélisation. Dans l’intérêt principal de pouvoir améliorer les
		# prédictions du trafic.
		# En effet, le développement de projets avec une stratégie data driven devient de plus en plus important
		# avec un impact direct sur la prise de décisions opérationnelles et budgétaires."""
		
		# """Nous tenions à terminer ce rapport en mentionnant notre satisfaction à avoir pu mettre en application, tout
		# au long de ce projet, toutes les connaissances acquises durant notre cursus de formation. Cela a rendu
		# encore plus enrichissant et captivant notre approche de la Data Analyse au cours de ces 8 derniers mois."""




if page == 'Test' :
# 	st.title("ZONE DE TESTS :)") 
# 	st.write("---")	
# 	st.info(f"{chosen_id=}")
# 	
# 	Créer un slider horizontal
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


# placeholder = st.empty()
# # Replace the placeholder with some text:
# placeholder.text("Hello")
# # Replace the text with a chart:
# placeholder.line_chart({"data": [1, 5, 2, 6]})
# # Replace the chart with several elements:
# with placeholder.container():
#     st.write("This is one element")
#     st.write("This is another")
# # Clear all those elements:
# placeholder.empty()


# with st.container():
#    st.write("This is inside the container")
#    # You can call any Streamlit command, including custom components:
#    st.bar_chart(np.random.randn(50, 3))
# st.write("This is outside the container")


# 		progress_text = "Operation in progress. Please wait."
# 		my_bar = st.progress(0, text=progress_text)		
# 		for percent_complete in range(100):
# 		    time.sleep(0.01)
# 		    my_bar.progress(percent_complete + 1, text=progress_text)
# 		time.sleep(1)
# 		my_bar.empty()		
# 		st.button("Rerun")


# 		options = st.multiselect(
# 			   'What are your favorite colors',
# 			      ['Green', 'Yellow', 'Red', 'Blue'],
# 					     ['Yellow', 'Red'])
# 		st.write('You selected:', options)

		
# 		with st.spinner("Predict en cours ..."):
# 			time.sleep(2)   


# 		st.divider()
# 		
# 		on = st.toggle('Mesures du modèle LR')	
# 		if on :
# 			with st.spinner("Chargement LR en cours ...") :
# 				rmse_train, rmse_test, r2_train, r2_test = load_and_predict(path_joblib + "model_LR")
# 				
# 				col1, col2, col3 = st.columns([30, 30, 40])
# 				with col2 :	
# 					st.write("Train")
# 					st.write("RMSE :", rmse_train)
# 					st.write("R² :", r2_train)
# 				with col3 :	
# 					st.write("Test")
# 					st.write("RMSE :", rmse_test)
# 					st.write("R² :", r2_test)
# 				#st.write("RMSE (train / test) :", rmse_train, "/", rmse_test)
# 				#st.write("R² (train / test) :", r2_train, r2_test)
# 			#st.success('Chargement LR terminé !', icon="✅")

# 		on = st.toggle('Mesures du modèle DTR')	
# 		if on :
# 			with st.spinner("Chargement DTR en cours ...") :
# 				rmse_train, rmse_test, r2_train, r2_test = load_and_predict(path_joblib + "model_DTR")
# 				st.write("RMSE :", rmse_train, rmse_test)
# 				st.write("R² :", r2_train, r2_test)
# 			#st.success('Chargement DTR terminé !', icon="✅")
# 				
# 		on = st.toggle('Mesures du modèle GBR')	
# 		if on :
# 			with st.spinner("Chargement GBR en cours ...") :
# 				rmse_train, rmse_test, r2_train, r2_test = load_and_predict(path_joblib + "model_GBR")
# 				st.write("RMSE :", rmse_train, rmse_test)
# 				st.write("R² :", r2_train, r2_test)
# 			#st.success('Chargement GBR terminé !', icon="✅")
# 				
# 		on = st.toggle('Mesures du modèle RFR')	
# 		if on :
# 			with st.spinner("Chargement RFR en cours ...") :
# 				rmse_train, rmse_test, r2_train, r2_test = load_and_predict(path_joblib + "model_RFR")
# 				st.write("RMSE :", rmse_train, rmse_test)
# 				st.write("R² :", r2_train, r2_test)
# 				#model_RFR = joblib.load(open(path_joblib + "model_RFR", 'rb'))
# 			#st.success('Chargement RFR terminé !', icon="✅")


# 		if st.button("Run") :		
# 			plot_site_2023(df_group_par_j_2023, df_predict_2023, mois, numero_mois, site) 
# 		if 'clicked' not in st.session_state:
# 			   st.session_state.clicked = False
# 		def click_button():
# 		    st.session_state.clicked = True
# 		if st.button('Run', on_click=click_button):
# 			plot_site_2023(df_group_par_j_2023, df_predict_2023, mois, numero_mois, site)
# 			if numero_mois == 1 :
# 				st.image("Greves_202301.jpg") 
# 			elif numero_mois == 3 :
# 				st.image("Greves_202303.jpg") 
# 			elif numero_mois == 4 :
# 					st.image("Greves_202304.jpg")
# 		if st.session_state.clicked:
	
	
# texte1="""La ville de Paris a déployé des compteurs vélo permanents au cours des dernières années pour évaluer l'évolution de la pratique cycliste. Dans cette optique, nous avons entrepris une analyse des relevés horaires quotidiens sur la période allant du <font color="red">1er janvier 2020</font> au <font color="red">30 avril 2023</font>. Notre objectif étant de proposer à la ville de Paris des pistes de réflexion concernant cette pratique."""
# texte2="De plus, afin de mieux appréhender les tendances en matière de trafic cycliste, nous avons également examiné les données relatives à un autre mode de transport personnel, à savoir les trottinettes. Parallèlement, nous avons examiné les données relatives aux accidents corporels impliquant à la fois des vélos et des trottinettes dans cette même zone géographique."
# texte3="Enfin, nous nous sommes penchés sur divers modèles de Machine Learning dans le but de prédire l'évolution du trafic cycliste dans la ville."
# 	
# texte = "<br>" + texte1 + "<br><br>" + texte2 + "<br><br>" + texte3
# st.markdown(f'<p style="text-align: justify;">{texte}</p>', unsafe_allow_html=True)


# st.write("$$\Pi\Delta$$")
# st.write("$$\def\sqr#1{#1^2} \sqr{y}$$")
# st.write("$$\displaystyle\sum_0^n$$")
	st.write('Zone de tests')
