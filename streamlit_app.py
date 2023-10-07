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
st.markdown('<p style="text-align:center; font-size:45px; font-weight:bold;">Analyse du trafic cycliste à Paris</p>', unsafe_allow_html=True)


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
				   "container": {"padding": "0!important", "background-color": "grey"},#fafafa
				   "icon": {"color": "white", "font-size": "17px"}, 
				   "nav-link": {"font-size": "17px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
				   "nav-link-selected": {"font-size": "16px","background-color": "red"}
				      })


# GESTION DE CHAQUE PAGE
# PAGE 1
if page == pages[0] : 
	st.title("Contexte du projet")
	st.write("---")
	
	
# PAGE 2
if page == pages[1] : 
	#st.title("Jeux de données")
	#st.write("---")
	
	# SLIDER HORIZONTAL
	chosen_id = stx.tab_bar(data=[
		   stx.TabBarItemData(id=1, title="Dataset principal", description=""),
		   stx.TabBarItemData(id=2, title="Datasets secondaires", description="")
						   		 ], default=1)
	#st.info(f"{chosen_id=}")

	if chosen_id == "1" :
		st.header("Dataset principal")
		
		st.subheader('1. Source')
		st.markdown("Le jeu de données provient du site : [opendata.paris.fr](https://opendata.paris.fr/explore/dataset/comptage-velo-donnees-compteurs/)", unsafe_allow_html=True)    	
		st.markdown('<p style="text-align: justify;"><br>La Ville de Paris déploie depuis plusieurs années des compteurs vélo permanents  (site ou point de comptage) pour évaluer le développement de la pratique cycliste. Les compteurs sont situés sur des pistes cyclables et dans certains couloirs bus ouverts aux vélos. Les autres véhicules (ex : trottinettes…) ne sont pas comptés.</p>', unsafe_allow_html=True)	
		st.markdown('<p style="text-align: justify;"><u>Remarque :</u><br> Le nombre de compteurs évolue au fur et à mesure des aménagements cyclables. Certains compteurs peuvent être désactivés pour travaux ou subir ponctuellement une panne.</p>', unsafe_allow_html=True)

		

	if chosen_id == "2" :
		st.header("Datasets secondaires")
		st.subheader('1. Sources')
		
# PAGE 3
if page == pages[2] : 
	st.title("Explorations / Analyses")
	st.write("---")
		
	# chargement de la carte accidents vélos 2021
	with open("carte_acc_velos_par_arrond_2021.html", 'r', encoding='utf-8') as f:
		   fic_html = f.read()
	st.components.v1.html(fic_html, height=600, width=600)


# PAGE 4
if page == pages[3] : 
	st.title("Data visualization")
	st.write("---")
	
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


# PAGE 5
if page == pages[4] : 	
	#st.title("Modélisations")
	#st.write("---")
	
	# SLIDER HORIZONTAL
	chosen_id = stx.tab_bar(data=[
		   stx.TabBarItemData(id=1, title="Séries temporelles", description=""),
		   stx.TabBarItemData(id=2, title="Modélisations", description=""),
		   stx.TabBarItemData(id=3, title="Prédictions", description="")
		   ], default=1)

	if chosen_id == "1" :
		st.header("Séries temporelles")
		
		
	if chosen_id == "2" :
		st.header("Modèles de Machine Learning")
		
		
	if chosen_id == "3" :
		st.header("Prédictions du trafic 2023")	
	
		liste_sites = df_group_par_j_2023.nom_compteur.unique()
		site = st.selectbox('Sélectionnez un site de comptage :', liste_sites)
		
		liste_mois = ['Janvier', 'Février', 'Mars', 'Avril']
		#liste_mois_cap = [calendar.month_name[mois].capitalize() for mois in liste_mois]
		mois = st.selectbox('Sélectionnez le mois à prédir :', liste_mois)	
		numero_mois = liste_mois.index(mois.capitalize()) + 1
		
		plot_site_2023(df_group_par_j_2023, df_predict_2023, mois, numero_mois, site) 
	
	
# PAGE 6
if page == pages[5] :
	st.title("Perspectives") 
	st.write("---")	
