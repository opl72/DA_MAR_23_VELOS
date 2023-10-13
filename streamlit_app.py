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
import pickle
import joblib


path_image_3 = "im/im_3/"
path_image_4 = "im/im_4/"
path_image_5 = "im/im_5/"
path_pickle = "pickle/"

# CONFIG DE L'APPARENCE DE L'APPLI
st.set_page_config(layout="wide", # affichage par défaut en mode wide
				   page_title="Trafic cycliste parisien", # titre de l'appli dans la barre du navigateur
				   initial_sidebar_state = "collapsed", # apparence de la barre latérale
				   page_icon=":bike:") # icone de l'appli dans la barre du navigateur
#st.markdown('<meta name="viewport" content="width=device-width, initial-scale=1.0">', unsafe_allow_html=True)

# MISE EN CACHE DES RESSOURCES UTILES
@st.cache_data
def load_and_cache(file_path) :
	return pd.read_csv(file_path)
# chargement et mise en cahe des fichiers utiles à la prédictions du trafic
#df_group_par_j_2023 = load_and_cache('df_group_par_jour_2023.csv')
#df_predict_2023 = load_and_cache('df_pred_2023.csv')

@st.cache_data
def load_pickle_and_cache(file_path) :
	return pickle.load(open(path_pickle + file_path, 'rb'))
# chargement et mise en cahe des fichiers utiles à la prédictions du trafic
df_group_par_j_2023 = load_pickle_and_cache('df_group_par_jour_2023')
df_predict_2023 = load_pickle_and_cache('df_pred_2023')
# chargement et mise en cahe des fichiers utiles au ML
X_2020_2022_ohe = load_pickle_and_cache("X_2020_2022_ohe")
y_2020_2022 = load_pickle_and_cache("y_2020_2022")
X_2023_ohe = load_pickle_and_cache("X_2023_ohe")
y_2023 = load_pickle_and_cache("y_2023")


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
           max-width: 180px;}""", unsafe_allow_html=True)  
	
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
				   "nav-link-selected": {"font-size": "16px", "font-family":"Arial, sans-serif", "background-color": "#FF0000"} 
				      })


# GESTION DES PAGES

# PAGE 1 : Contexte
if page == pages[0] : 	
	# SLIDER HORIZONTAL
	stx.tab_bar(data=[stx.TabBarItemData(id=1, title="Contexte du projet", description="")], default=1)
	
	# CONTENU
	texte1="""La ville de Paris a déployé des compteurs vélo permanents au cours des dernières années pour évaluer l'évolution de la pratique cycliste. Dans cette optique, nous avons entrepris une analyse des relevés horaires quotidiens sur la période allant du <font color="red">1er janvier 2020</font> au <font color="red">30 avril 2023</font>. Notre objectif étant de proposer à la ville de Paris des pistes de réflexion concernant cette pratique."""
	texte2="De plus, afin de mieux appréhender les tendances en matière de trafic cycliste, nous avons également examiné les données relatives à un autre mode de transport personnel, à savoir les trottinettes. Parallèlement, nous avons examiné les données relatives aux accidents corporels impliquant à la fois des vélos et des trottinettes dans cette même zone géographique."
	texte3="Enfin, nous nous sommes penchés sur divers modèles de Machine Learning dans le but de prédire l'évolution du trafic cycliste dans la ville."
		
	texte = "<br>" + texte1 + "<br><br>" + texte2 + "<br><br>" + texte3
	st.markdown(f'<p style="text-align: justify;">{texte}</p>', unsafe_allow_html=True)	 
	
	
# PAGE 2 : JDD
if page == pages[1] : 		
	# SLIDER HORIZONTAL
	tab_bar_id = stx.tab_bar(data=[
		   stx.TabBarItemData(id=1, title="Dataset principal", description=""),
		   stx.TabBarItemData(id=2, title="Datasets secondaires", description="")], default=1)	

	# ONGLET 1 : Dataset principal
	if tab_bar_id == "1" :
		st.markdown('<p style="text-align:left; font-size:18px;font-family:Arial;"><b>Dataset principal : Comptages horaires des vélos</p>', unsafe_allow_html=True)
		
		#st.subheader('Source')
		st.markdown("""<p style="text-align:left; padding-left:15px;">Le jeu de données provient du site : <a href="https://opendata.paris.fr/explore/dataset/comptage-velo-donnees-compteurs/" target="_blank">opendata.paris.fr</a></p>""", unsafe_allow_html=True) 	
		st.markdown('<p style="text-align: justify;padding-left:15px;"><br>La Ville de Paris déploie depuis plusieurs années des compteurs vélo permanents  (site ou point de comptage) pour évaluer le développement de la pratique cycliste. Les compteurs sont situés sur des pistes cyclables et dans certains couloirs bus ouverts aux vélos. Les autres véhicules (ex : trottinettes…) ne sont pas comptés.</p>', unsafe_allow_html=True)	
		st.markdown("""<p style="text-align: left;padding-left:15px;"><u>Remarque :</u><br> Le nombre de compteurs évolue au fur et à mesure des aménagements cyclables. Certains compteurs peuvent être désactivés pour travaux ou subir ponctuellement une panne.</p>""", unsafe_allow_html=True)

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
			cols = st.columns([175, 100], gap="small")
			with cols[0] : st.image(path_image_3+"Outliers_4.jpg", use_column_width=True)	
			with cols[1] : st.image(path_image_3+"Outliers_2.png", use_column_width=True)
				
	# ONGLET 2 : SITES MULTIMODAUX		
	if tab_bar_id == "2" :
		st.markdown('<p style="text-align:left; font-size:18px; font-family:Arial;"><b>Sites de comptages multimodaux</p>', unsafe_allow_html=True)
		cols = st.columns([125, 1150, 125], gap="small")
		with cols[1] : 
			st.image(path_image_3+"SiteDeComptage_3.png", use_column_width=True)
			st.markdown('<p style="text-align:center;">Sur les <font color="red">9</font> sites enregistrant des passages de vélos ou vélos+trottinettes, seuls <b><font color="red">5</font></b> sites arrivent à distinguer les vélos</p>', unsafe_allow_html=True)
		
	# ONGLET 3 : CARTES DU TRAFIC
	if tab_bar_id == "3" :
		st.markdown('<p style="text-align:left; font-size:18px; font-family:Arial;"><b>Densité du trafic à vélo en 2023</p>', unsafe_allow_html=True)
		# chargement des cartes folium
		cols = st.columns([44, 12, 44], gap="large") # on créé 3 colonnes pour gérer le centrage des titres	
		with cols[0] :
			st.markdown('<p style="text-align: left;"><b><font color="red">Sans</font></b> clustering :</p>', unsafe_allow_html=True)
			with open(path_image_3+"carte_densite_trafic_par_an_par_moy_sans_Clustering_2023.html", 'r', encoding='utf-8') as f1 :				
				st.components.v1.html(f1.read(), width=580, height=530)		
		
		# la colonne du milieu (invisible) sert juste à centrer les titres au dessus de chaque carte ;)
				
		with cols[2] :			
			st.markdown('<p style="text-align: left;"><b><font color="red">Avec</font></b> clustering :</p>', unsafe_allow_html=True)
			with open(path_image_3+"carte_densite_trafic_par_an_par_moy_avec_Clustering_2023.html", 'r', encoding='utf-8') as f2 : 					
				st.components.v1.html(f2.read(), width=580, height=530)

		
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
			#st.markdown('<p style="text-align: left;"><b>Semaine :</p>', unsafe_allow_html=True)
			st.image(path_image_4+"TraficVéloParHeureSemaine.png", width=1300)
			st.image(path_image_4+"TraficTrotParHeureSemaine.png", width=1300)			
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
				st.markdown('<p style="text-align: left;"><b>Trafic cycliste mensuel :</p>', unsafe_allow_html=True)
				st.image(path_image_4+"TraficVélo2021_2.png", use_column_width=True)	
			with cols[1] : 
				st.markdown('<p style="text-align: left;"><b>Nombre de vélos impliqués dans des accidents corporels, par mois :</p>', unsafe_allow_html=True)
				st.image(path_image_4+"AccVélos2021_2.png", use_column_width=True)				
		# TAB 2 : HORAIRE
		with tabs[1] :
			cols = st.columns(2, gap="small")
			with cols[0] : 
				st.markdown('<p style="text-align: left;"><b>Trafic cycliste horaire :</p>', unsafe_allow_html=True)
				st.image(path_image_4+"TraficVéloParHeureSemaineWE.png", use_column_width=True)	
			with cols[1] : 
				st.markdown('<p style="text-align: left;"><b>Nombre de vélos impliqués dans des accidents corporels, par heure :</p>', unsafe_allow_html=True)
				st.image(path_image_4+"TraficVéloAccParHeureSemaineWE.png", use_column_width=True)
						
	# ONGLET 4 : Carte des accidents
	if tab_bar_id == "4" :	
		cols = st.columns([90, 3, 90], gap="small") # on créé 3 colonnes pour gérer le centrage des titres	
		with cols[0] :
			st.markdown('<p style="text-align: left;"><b>Carte des vélos impliqués dans des accidents corporels en 2021, par arrondissement</p>', unsafe_allow_html=True)
			with open(path_image_4+"carte_acc_velos_par_arrond_2021_2.html", 'r', encoding='utf-8') as f1 :				
				st.components.v1.html(f1.read(), height=570, width=690)	
				st.image(path_image_4+"colormap.jpg", width=690)
		with cols[2] :
			st.markdown('<p style="text-align: left;"><b>Carte des vélos impliqués dans des accidents corporels en 2021, par coordonnées gps</p>', unsafe_allow_html=True)
			with open(path_image_4+"carte_acc_velos_2021.html", 'r', encoding='utf-8') as f2 :			
				st.components.v1.html(f2.read(), height=570, width=690)	
		
		st.divider()
		cols = st.columns(1, gap="small") 
		with cols[0] :
			st.markdown('<p style="text-align: left;"><b>Comptage des vélos par site en 2023</p>', unsafe_allow_html=True)
			with open(path_image_4+"carte_densite_trafic_par_an_par_sum_sans_Clustering_2023.html", 'r', encoding='utf-8') as f3 :			
				st.components.v1.html(f3.read(), height=590, width=590)


# PAGE 5 : ML
if page == pages[4] : 	
	# SLIDER HORIZONTAL
	tab_bar_id = stx.tab_bar(data=[
		   stx.TabBarItemData(id=1, title="Séries temporelles", description=""),
		   stx.TabBarItemData(id=2, title="Modélisations", description=""),
		   stx.TabBarItemData(id=3, title="Prédictions", description="")], default=1)

	# ONGLET 1 : Séries temporelles
	if tab_bar_id == "1" :
		st.header("Séries temporelles")
		st.write("A compléter")
		
	# ONGLET 2 : Modélisations
	if tab_bar_id == "2" :
		st.header("Modèles de Machine Learning")
		st.write("afficher le dataset avec les variables explicatives supplémentaires")
		
		on = st.toggle('Afficher le dataset source')
		if on :
			st.dataframe(df_group_par_j_2023, 
 							width=None, 
 							height=275, 
 							use_container_width=True, 
 							hide_index=None, 
 							column_order=None, 
 							column_config={"Annee":st.column_config.NumberColumn("Annee",format="%d")}
						)
			
		on = st.toggle('Sélection du modèle LR')	
		if on :
			with st.spinner("Chargement LR en cours ...") :
				model_LR = joblib.load(open(path_pickle + "model_LR", 'rb'))
				st.success('Chargement LR terminé !', icon="✅")

		
		on = st.toggle('Sélection du modèle DTR')	
		if on :
			with st.spinner("Chargement DTR en cours ...") :
				model_DTR = joblib.load(open(path_pickle + "model_DTR", 'rb'))
				st.success('Chargement DTR terminé !', icon="✅")
				
				
		on = st.toggle('Sélection du modèle GBR')	
		if on :
			with st.spinner("Chargement GBR en cours ...") :
				model_GBR = joblib.load(open(path_pickle + "model_GBR", 'rb'))
				st.success('Chargement GBR terminé !', icon="✅")
				
		on = st.toggle('Sélection du modèle RFR')	
		if on :
			with st.spinner("Chargement RFR en cours ...") :
				model_RFR = joblib.load(open(path_pickle + "model_RFR", 'rb'))
				st.success('Chargement RFR terminé !', icon="✅")
 		


		options = st.multiselect(
			   'What are your favorite colors',
			      ['Green', 'Yellow', 'Red', 'Blue'],
					     ['Yellow', 'Red'])

		st.write('You selected:', options)
		
# 		with st.spinner("Predict en cours ..."):
# 			time.sleep(2)
			
	# ONGLET 3 : Prédictions
	if tab_bar_id == "3" :
		st.markdown('<p style="text-align:left; font-size:18px; font-family:Arial;"><b>Prédictions du trafic 2023</p>', unsafe_allow_html=True)
		
		liste_sites = df_group_par_j_2023.nom_compteur.unique()
		site = st.selectbox('Sélectionnez un site de comptage :', liste_sites, index=5)
		
		liste_mois = ['Janvier', 'Février', 'Mars', 'Avril']
		#liste_mois_cap = [calendar.month_name[mois].capitalize() for mois in liste_mois]
		mois = st.selectbox('Sélectionnez le mois à prédir :', liste_mois, index=2)
		numero_mois = liste_mois.index(mois.capitalize()) + 1
		
		#st.markdown("<br>", unsafe_allow_html=True)
		fig = plot_site_2023(df_group_par_j_2023, df_predict_2023, mois, numero_mois, site)
		
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
	
	

	    
