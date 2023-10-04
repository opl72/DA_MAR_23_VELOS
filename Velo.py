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
	df_group_par_j_2023 = pd.read_csv('df_group_par_jour_2023.csv')
	df_predict_2023 = pd.read_csv('df_pred_2023.csv')
    	choix = ['Random Forest', 'SVC', 'Logistic Regression']
	option = st.selectbox('Choix du modèle', choix)
