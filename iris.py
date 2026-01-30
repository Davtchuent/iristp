#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════╗
║               TP N°1: Classification des Fleurs Iris                     ║
║              Analyse des Données et Machine Learning                     ║
║                                                                          ║
║  Université de Yaoundé 1 - École Normale Supérieure                      ║
║  Département d'Informatique et des Technologies Éducatives               ║
║  Module: Introduction à l'IA (INFO4111)                                  ║
║  Sous la supervisionde : Stéphane C.K. TEKOUAB (PhD & Ing.)              ║
╚══════════════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report, f1_score, precision_score, recall_score
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# ═══════════════════════════════════════════════════════════════════════════
#                           CONFIGURATION DE LA PAGE
# ═══════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="TP Iris - Machine Learning",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════════════════════════
#                              STYLES CSS PROFESSIONNELS
# ═══════════════════════════════════════════════════════════════════════════

st.markdown("""
    <style>
    /* Thème principal */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* En-tête principal stylisé */
    .main-title {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        margin-bottom: 2rem;
        animation: fadeIn 1s ease-in;
    }
    
    .main-title h1 {
        font-size: 2.8rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-title p {
        font-size: 1.1rem;
        margin-top: 0.5rem;
        opacity: 0.95;
    }
    
    /* Carte de section */
    .section-card {
        background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
        border-left: 5px solid #667eea;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .section-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
    }
    
    /* Titre de section */
    .section-title {
        color: #667eea;
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        border-bottom: 3px solid #667eea;
        padding-bottom: 0.5rem;
    }
    
    /* Cartes métriques personnalisées */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Cartes d'information colorées */
    .info-card {
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        border-left: 5px solid;
        box-shadow: 0 3px 10px rgba(0,0,0,0.1);
    }
    
    .info-card.purple {
        background: linear-gradient(135deg, #f5f3ff 0%, #ede9fe 100%);
        border-left-color: #8b5cf6;
    }
    
    .info-card.blue {
        background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
        border-left-color: #3b82f6;
    }
    
    .info-card.green {
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
        border-left-color: #22c55e;
    }
    
    .info-card.orange {
        background: linear-gradient(135deg, #fff7ed 0%, #ffedd5 100%);
        border-left-color: #f97316;
    }
    
    /* Boutons stylisés */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Sidebar personnalisée */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Tabs stylisés */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #f8f9fa;
        border-radius: 10px 10px 0 0;
        padding: 12px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    /* Tableaux améliorés */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 3px 10px rgba(0,0,0,0.1);
    }
    
    /* Badge de statut */
    .status-badge {
        display: inline-block;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
        margin: 0.2rem;
    }
    
    .status-badge.success {
        background: #dcfce7;
        color: #166534;
    }
    
    .status-badge.warning {
        background: #fef3c7;
        color: #92400e;
    }
    
    .status-badge.info {
        background: #dbeafe;
        color: #1e40af;
    }
    
    /* Divider élégant */
    .elegant-divider {
        height: 3px;
        background: linear-gradient(90deg, transparent, #667eea, transparent);
        margin: 2rem 0;
        border-radius: 2px;
    }
    
    /* Footer stylisé */
    .footer {
        text-align: center;
        padding: 2rem;
        margin-top: 3rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 15px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.2);
    }
    
    /* Indicateurs de progression */
    .progress-container {
        background: #e5e7eb;
        border-radius: 10px;
        overflow: hidden;
        height: 10px;
        margin: 1rem 0;
    }
    
    .progress-bar {
        height: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        transition: width 0.3s ease;
    }
    </style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════
#                         CONFIGURATION DES COULEURS
# ═══════════════════════════════════════════════════════════════════════════

COLOR_PALETTE = {
    'setosa': '#FF6B6B',      # Rouge corail
    'versicolor': '#4ECDC4',  # Turquoise
    'virginica': '#45B7D1',   # Bleu ciel
    'primary': '#667eea',     # Violet
    'secondary': '#764ba2',   # Violet foncé
    'accent': '#f093fb',      # Rose
    'success': '#22c55e',     # Vert
    'warning': '#f97316',     # Orange
    'info': '#3b82f6'         # Bleu
}

PLOTLY_THEME = {
    'template': 'plotly_white',
    'color_discrete_sequence': [COLOR_PALETTE['setosa'], COLOR_PALETTE['versicolor'], COLOR_PALETTE['virginica']]
}

# Configuration matplotlib
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette([COLOR_PALETTE['setosa'], COLOR_PALETTE['versicolor'], COLOR_PALETTE['virginica']])

# ═══════════════════════════════════════════════════════════════════════════
#                            CHARGEMENT DES DONNÉES
# ═══════════════════════════════════════════════════════════════════════════

@st.cache_data
def load_data():
    """Charge le dataset Iris avec mise en cache"""
    try:
        df = pd.read_csv('Iris.csv', sep=';')
    except:
        df = pd.read_csv('/mnt/user-data/uploads/Iris.csv', sep=';')
    return df

# Charger les données
df = load_data()

# ═══════════════════════════════════════════════════════════════════════════
#                         EN-TÊTE PRINCIPAL STYLISÉ
# ═══════════════════════════════════════════════════════════════════════════

st.markdown("""
    <div class="main-title">
        <h1>🌸 TP N°1: Classification des Fleurs Iris 🌸</h1>
        <p>Introduction à l'IA</p>
        <p style="font-size: 0.9rem; margin-top: 1rem;">
            <strong>Université de Yaoundé 1</strong> | École Normale Supérieure<br>
            Module INFO4111 | sous la supervision de: Stéphane C.K. TEKOUAB (PhD & Ing.)
        </p>
    </div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════
#                            SIDEBAR NAVIGATION
# ═══════════════════════════════════════════════════════════════════════════

st.sidebar.markdown("""
    <div style='text-align: center; padding: 1rem; background: white; border-radius: 10px; margin-bottom: 1rem;'>
        <h2 style='color: #667eea; margin: 0;'>📚 Navigation</h2>
    </div>
""", unsafe_allow_html=True)

menu_option = st.sidebar.radio(
    "",
    [
        "🏠 Accueil",
        "📊 Exercice 1 - Analyse qualitative",
        "📏 Exercice 2 - Variables quantitatives",
        "🔗 Exercice 3 - Analyse bivariée",
        "📦 Exercice 4 - Boxplots",
        "🎨 Exercice 5 - Visualisations avancées",
        "🤖 Modélisation KNN",
        "📈 Optimisation & Comparaison"
    ],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")

# Informations sur le dataset
st.sidebar.markdown("""
    <div style='background: white; padding: 1rem; border-radius: 10px; margin-top: 1rem;'>
        <h3 style='color: #667eea; margin-top: 0;'>📊 Dataset Info</h3>
        <p><strong>Observations:</strong> 150</p>
        <p><strong>Variables:</strong> 5</p>
        <p><strong>Espèces:</strong> 3</p>
        <p><strong>Classes équilibrées:</strong> ✅</p>
    </div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════
#                              PAGE: ACCUEIL
# ═══════════════════════════════════════════════════════════════════════════

if menu_option == "🏠 Accueil":
    
    # Métriques principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-label">Observations</div>
                <div class="metric-value">150</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="metric-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
                <div class="metric-label">Variables</div>
                <div class="metric-value">5</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="metric-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
                <div class="metric-label">Espèces</div>
                <div class="metric-value">3</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
            <div class="metric-card" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);">
                <div class="metric-label">Classes équilibrées</div>
                <div class="metric-value">✓</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div class='elegant-divider'></div>", unsafe_allow_html=True)
    
    # Introduction
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
            <div class="info-card purple">
                <h3 style='color: #8b5cf6; margin-top: 0;'>📖 Contexte Historique</h3>
                <p style='font-size: 1rem; line-height: 1.8;'>
                    Le dataset <strong>Iris</strong> est l'un des plus célèbres dans le domaine du Machine Learning.
                    Collecté par <strong>Edgar Anderson</strong> en 1935 et rendu célèbre par 
                    <strong>Sir R.A. Fisher</strong> en 1936, il contient des mesures morphologiques de 
                    trois espèces d'iris.
                </p>
                <p style='font-size: 1rem; line-height: 1.8;'>
                    Ce dataset a été utilisé pour développer l'<strong>analyse discriminante linéaire</strong>, 
                    une technique fondamentale en apprentissage automatique.
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="info-card blue">
                <h3 style='color: #3b82f6; margin-top: 0;'>🎯 Objectifs du TP</h3>
                <ul style='font-size: 0.95rem; line-height: 1.8;'>
                    <li>Explorer les données</li>
                    <li>Visualiser les distributions</li>
                    <li>Analyser les corrélations</li>
                    <li>Construire des modèles ML</li>
                    <li>Évaluer les performances</li>
                    <li>Optimiser les paramètres</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    
    # Les 3 espèces d'Iris
    st.markdown("<h2 style='text-align: center; color: #667eea; margin: 2rem 0;'>🌺 Les Trois Espèces d'Iris 🌺</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class="info-card green">
                <h3 style='color: #22c55e; text-align: center;'>🌸 Iris Setosa</h3>
                <p style='text-align: center; font-size: 1.5rem; margin: 1rem 0;'>50 observations</p>
                <p style='text-align: center;'>
                    <span class='status-badge success'>Facilement séparable</span>
                </p>
                <p style='margin-top: 1rem;'>
                    Caractérisée par des pétales courts et larges. 
                    C'est l'espèce la plus distinctive des trois.
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="info-card blue">
                <h3 style='color: #3b82f6; text-align: center;'>🌸 Iris Versicolor</h3>
                <p style='text-align: center; font-size: 1.5rem; margin: 1rem 0;'>50 observations</p>
                <p style='text-align: center;'>
                    <span class='status-badge info'>Moyennement séparable</span>
                </p>
                <p style='margin-top: 1rem;'>
                    Espèce intermédiaire avec des caractéristiques 
                    qui peuvent chevaucher avec Virginica.
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="info-card purple">
                <h3 style='color: #8b5cf6; text-align: center;'>🌸 Iris Virginica</h3>
                <p style='text-align: center; font-size: 1.5rem; margin: 1rem 0;'>50 observations</p>
                <p style='text-align: center;'>
                    <span class='status-badge warning'>Chevauche Versicolor</span>
                </p>
                <p style='margin-top: 1rem;'>
                    Caractérisée par des pétales longs et larges. 
                    Partage certaines caractéristiques avec Versicolor.
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div class='elegant-divider'></div>", unsafe_allow_html=True)
    
    # Aperçu des données avec style
    st.markdown("<h2 style='color: #667eea;'>👀 Aperçu des Données</h2>", unsafe_allow_html=True)
    
    st.dataframe(
        df.head(10).style.background_gradient(cmap='RdYlGn', subset=['SepalLength', 'SepalWidth', 'PetalLength', 'PetalWidth']),
        use_container_width=True,
        height=400
    )
    
    # Variables du dataset
    st.markdown("<div class='elegant-divider'></div>", unsafe_allow_html=True)
    st.markdown("<h2 style='color: #667eea;'>📐 Variables du Dataset</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class="info-card orange">
                <h3 style='color: #f97316;'>🌿 Variables du Sépale</h3>
                <ul style='font-size: 1rem; line-height: 2;'>
                    <li><strong>SepalLength:</strong> Longueur du sépale (cm)</li>
                    <li><strong>SepalWidth:</strong> Largeur du sépale (cm)</li>
                </ul>
                <p style='margin-top: 1rem; font-size: 0.9rem; color: #666;'>
                    Le sépale est la partie externe de la fleur qui protège le bouton floral.
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="info-card green">
                <h3 style='color: #22c55e;'>🌺 Variables du Pétale</h3>
                <ul style='font-size: 1rem; line-height: 2;'>
                    <li><strong>PetalLength:</strong> Longueur du pétale (cm)</li>
                    <li><strong>PetalWidth:</strong> Largeur du pétale (cm)</li>
                </ul>
                <p style='margin-top: 1rem; font-size: 0.9rem; color: #666;'>
                    Le pétale est la partie colorée et visible de la fleur.
                </p>
            </div>
        """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════
#                    EXERCICE 1: ANALYSE QUALITATIVE
# ═══════════════════════════════════════════════════════════════════════════

elif menu_option == "📊 Exercice 1 - Analyse qualitative":
    
    st.markdown("""
        <div class="section-card">
            <h1 class="section-title">📊 Exercice 1: Analyse de la Variable Qualitative (Species)</h1>
            <p style='font-size: 1.1rem; color: #666;'>
                Étude de la répartition des trois espèces d'Iris à travers différentes représentations graphiques.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Effectifs
    effectifs = df['Species'].value_counts()
    
    # Métriques
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Setosa</div>
                <div class="metric-value">{effectifs['setosa']}</div>
                <div style="margin-top: 0.5rem;">33.33%</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="metric-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
                <div class="metric-label">Versicolor</div>
                <div class="metric-value">{effectifs['versicolor']}</div>
                <div style="margin-top: 0.5rem;">33.33%</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class="metric-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
                <div class="metric-label">Virginica</div>
                <div class="metric-value">{effectifs['virginica']}</div>
                <div style="margin-top: 0.5rem;">33.33%</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
            <div class="metric-card" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);">
                <div class="metric-label">Total</div>
                <div class="metric-value">{len(df)}</div>
                <div style="margin-top: 0.5rem;">100%</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div class='elegant-divider'></div>", unsafe_allow_html=True)
    
    # Graphiques
    st.markdown("<h2 style='color: #667eea;'>📈 Représentations Graphiques</h2>", unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Histogramme", "🥧 Diagramme Circulaire", "📶 Barres Horizontales", "🎨 Graphique Interactif"])
    
    with tab1:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            fig = go.Figure(data=[
                go.Bar(
                    x=effectifs.index,
                    y=effectifs.values,
                    marker=dict(
                        color=[COLOR_PALETTE['setosa'], COLOR_PALETTE['versicolor'], COLOR_PALETTE['virginica']],
                        line=dict(color='white', width=2)
                    ),
                    text=effectifs.values,
                    textposition='outside',
                    textfont=dict(size=16, color='black', family='Poppins')
                )
            ])
            
            fig.update_layout(
                title={
                    'text': '📊 Distribution des Espèces d\'Iris',
                    'font': {'size': 24, 'family': 'Poppins', 'color': '#667eea'}
                },
                xaxis_title='Espèce',
                yaxis_title='Nombre d\'observations',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family='Poppins', size=14),
                height=500,
                showlegend=False,
                xaxis=dict(
                    showgrid=False,
                    tickfont=dict(size=14, family='Poppins')
                ),
                yaxis=dict(
                    showgrid=True,
                    gridcolor='rgba(0,0,0,0.1)',
                    tickfont=dict(size=14, family='Poppins')
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("""
                <div class="info-card purple">
                    <h3 style='color: #8b5cf6;'>💡 Observations</h3>
                    <ul style='line-height: 2;'>
                        <li>Distribution parfaitement équilibrée</li>
                        <li>50 observations par espèce</li>
                        <li>Aucun biais de classe</li>
                        <li>Idéal pour le ML</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            fig = go.Figure(data=[
                go.Pie(
                    labels=effectifs.index,
                    values=effectifs.values,
                    marker=dict(
                        colors=[COLOR_PALETTE['setosa'], COLOR_PALETTE['versicolor'], COLOR_PALETTE['virginica']],
                        line=dict(color='white', width=3)
                    ),
                    textfont=dict(size=16, family='Poppins', color='white'),
                    hole=0.4,
                    pull=[0.05, 0.05, 0.05]
                )
            ])
            
            fig.update_layout(
                title={
                    'text': '🥧 Répartition en Pourcentage',
                    'font': {'size': 24, 'family': 'Poppins', 'color': '#667eea'}
                },
                annotations=[dict(text='150<br>Total', x=0.5, y=0.5, font_size=20, showarrow=False, font_family='Poppins')],
                height=500,
                font=dict(family='Poppins', size=14),
                showlegend=True,
                legend=dict(
                    orientation="v",
                    yanchor="middle",
                    y=0.5,
                    xanchor="right",
                    x=1.2,
                    font=dict(size=14, family='Poppins')
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("""
                <div class="info-card green">
                    <h3 style='color: #22c55e;'>✅ Points Clés</h3>
                    <ul style='line-height: 2;'>
                        <li>Chaque espèce: <strong>33.33%</strong></li>
                        <li>Répartition tripartite égale</li>
                        <li>Dataset bien construit</li>
                        <li>Pas de sur-représentation</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)
    
    with tab3:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            fig = go.Figure(data=[
                go.Bar(
                    y=effectifs.index,
                    x=effectifs.values,
                    orientation='h',
                    marker=dict(
                        color=[COLOR_PALETTE['setosa'], COLOR_PALETTE['versicolor'], COLOR_PALETTE['virginica']],
                        line=dict(color='white', width=2)
                    ),
                    text=effectifs.values,
                    textposition='outside',
                    textfont=dict(size=16, color='black', family='Poppins')
                )
            ])
            
            fig.update_layout(
                title={
                    'text': '📶 Barres Horizontales par Espèce',
                    'font': {'size': 24, 'family': 'Poppins', 'color': '#667eea'}
                },
                xaxis_title='Nombre d\'observations',
                yaxis_title='Espèce',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family='Poppins', size=14),
                height=400,
                showlegend=False,
                xaxis=dict(
                    showgrid=True,
                    gridcolor='rgba(0,0,0,0.1)',
                    tickfont=dict(size=14, family='Poppins')
                ),
                yaxis=dict(
                    showgrid=False,
                    tickfont=dict(size=14, family='Poppins')
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("""
                <div class="info-card blue">
                    <h3 style='color: #3b82f6;'>📊 Statistiques</h3>
                    <p><strong>Moyenne:</strong> 50.0</p>
                    <p><strong>Médiane:</strong> 50.0</p>
                    <p><strong>Écart-type:</strong> 0.0</p>
                    <p><strong>Variance:</strong> 0.0</p>
                    <div style='margin-top: 1rem; padding: 0.5rem; background: #dbeafe; border-radius: 5px;'>
                        <strong>Parfaitement équilibré!</strong>
                    </div>
                </div>
            """, unsafe_allow_html=True)
    
    with tab4:
        chart_type = st.selectbox(
            "Choisir le type de graphique:",
            ["Barres", "Circulaire", "Donut", "Barres empilées"]
        )
        
        if chart_type == "Barres":
            fig = px.bar(
                x=effectifs.index,
                y=effectifs.values,
                color=effectifs.index,
                color_discrete_sequence=[COLOR_PALETTE['setosa'], COLOR_PALETTE['versicolor'], COLOR_PALETTE['virginica']],
                labels={'x': 'Espèce', 'y': 'Nombre'},
                title='Distribution Interactive des Espèces'
            )
        elif chart_type == "Circulaire":
            fig = px.pie(
                values=effectifs.values,
                names=effectifs.index,
                color=effectifs.index,
                color_discrete_map={'setosa': COLOR_PALETTE['setosa'], 'versicolor': COLOR_PALETTE['versicolor'], 'virginica': COLOR_PALETTE['virginica']},
                title='Répartition en Camembert'
            )
        elif chart_type == "Donut":
            fig = px.pie(
                values=effectifs.values,
                names=effectifs.index,
                color=effectifs.index,
                color_discrete_map={'setosa': COLOR_PALETTE['setosa'], 'versicolor': COLOR_PALETTE['versicolor'], 'virginica': COLOR_PALETTE['virginica']},
                title='Répartition en Donut',
                hole=0.5
            )
        else:
            fig = px.bar(
                x=effectifs.index,
                y=effectifs.values,
                color=effectifs.index,
                color_discrete_sequence=[COLOR_PALETTE['setosa'], COLOR_PALETTE['versicolor'], COLOR_PALETTE['virginica']],
                title='Barres Empilées'
            )
        
        fig.update_layout(
            height=500,
            font=dict(family='Poppins', size=14),
            title_font=dict(size=24, family='Poppins', color='#667eea')
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Conclusion
    st.markdown("<div class='elegant-divider'></div>", unsafe_allow_html=True)
    st.markdown("""
        <div class="info-card green">
            <h3 style='color: #22c55e;'>✅ Conclusion de l'Exercice 1</h3>
            <p style='font-size: 1.1rem; line-height: 1.8;'>
                Le dataset Iris présente une <strong>distribution parfaitement équilibrée</strong> avec 
                <strong>50 observations</strong> pour chacune des trois espèces. Cette répartition idéale 
                évite tout biais de classe et garantit que nos modèles de machine learning ne seront pas 
                influencés par un déséquilibre dans les données. Les représentations graphiques montrent 
                clairement cette équité, avec chaque espèce représentant exactement <strong>33.33%</strong> 
                du dataset total.
            </p>
        </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════
#                EXERCICE 2: VARIABLES QUANTITATIVES
# ═══════════════════════════════════════════════════════════════════════════

elif menu_option == "📏 Exercice 2 - Variables quantitatives":
    
    st.markdown("""
        <div class="section-card">
            <h1 class="section-title">📏 Exercice 2: Analyse des Variables Quantitatives</h1>
            <p style='font-size: 1.1rem; color: #666;'>
                Étude approfondie des quatre variables morphologiques: longueur et largeur des sépales et pétales.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Sélection de variable
    variables = ['SepalLength', 'SepalWidth', 'PetalLength', 'PetalWidth']
    variable_names = {
        'SepalLength': '🌿 Longueur du Sépale',
        'SepalWidth': '🌿 Largeur du Sépale',
        'PetalLength': '🌺 Longueur du Pétale',
        'PetalWidth': '🌺 Largeur du Pétale'
    }
    
    selected_var = st.selectbox(
        "Sélectionner une variable à analyser:",
        variables,
        format_func=lambda x: variable_names[x]
    )
    
    # Statistiques descriptives
    st.markdown(f"<h2 style='color: #667eea;'>{variable_names[selected_var]}</h2>", unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Moyenne</div>
                <div class="metric-value">{df[selected_var].mean():.2f}</div>
                <div>cm</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="metric-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
                <div class="metric-label">Médiane</div>
                <div class="metric-value">{df[selected_var].median():.2f}</div>
                <div>cm</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class="metric-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
                <div class="metric-label">Écart-type</div>
                <div class="metric-value">{df[selected_var].std():.2f}</div>
                <div>cm</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
            <div class="metric-card" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);">
                <div class="metric-label">Minimum</div>
                <div class="metric-value">{df[selected_var].min():.2f}</div>
                <div>cm</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown(f"""
            <div class="metric-card" style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);">
                <div class="metric-label">Maximum</div>
                <div class="metric-value">{df[selected_var].max():.2f}</div>
                <div>cm</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div class='elegant-divider'></div>", unsafe_allow_html=True)
    
    # Visualisations
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Histogramme", "📦 Boxplot", "📈 Distribution", "📊 Comparaison Multi-variables"])
    
    with tab1:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            fig = go.Figure()
            
            fig.add_trace(go.Histogram(
                x=df[selected_var],
                nbinsx=20,
                marker=dict(
                    color=COLOR_PALETTE['primary'],
                    line=dict(color='white', width=1.5)
                ),
                opacity=0.8,
                name='Distribution'
            ))
            
            # Ajouter ligne de moyenne
            fig.add_vline(
                x=df[selected_var].mean(),
                line_dash="dash",
                line_color="red",
                annotation_text=f"Moyenne: {df[selected_var].mean():.2f} cm",
                annotation_position="top"
            )
            
            fig.update_layout(
                title={
                    'text': f'📊 Distribution de {variable_names[selected_var]}',
                    'font': {'size': 24, 'family': 'Poppins', 'color': '#667eea'}
                },
                xaxis_title=f'{variable_names[selected_var]} (cm)',
                yaxis_title='Fréquence',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family='Poppins', size=14),
                height=500,
                showlegend=False,
                xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)'),
                yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)')
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("""
                <div class="info-card purple">
                    <h3 style='color: #8b5cf6;'>📊 Statistiques</h3>
                """, unsafe_allow_html=True)
            
            stats_df = df[selected_var].describe()
            for stat, value in stats_df.items():
                st.markdown(f"<p><strong>{stat}:</strong> {value:.3f} cm</p>", unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
    
    with tab2:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            fig = go.Figure()
            
            fig.add_trace(go.Box(
                y=df[selected_var],
                name=variable_names[selected_var],
                marker=dict(color=COLOR_PALETTE['primary']),
                boxmean='sd',
                fillcolor='rgba(102, 126, 234, 0.3)',
                line=dict(width=2)
            ))
            
            fig.update_layout(
                title={
                    'text': f'📦 Boxplot de {variable_names[selected_var]}',
                    'font': {'size': 24, 'family': 'Poppins', 'color': '#667eea'}
                },
                yaxis_title=f'{variable_names[selected_var]} (cm)',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family='Poppins', size=14),
                height=500,
                showlegend=False,
                yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)')
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("""
                <div class="info-card blue">
                    <h3 style='color: #3b82f6;'>💡 Interprétation</h3>
                    <ul style='line-height: 2;'>
                        <li><strong>Boîte:</strong> Q1 à Q3 (50% des données)</li>
                        <li><strong>Ligne médiane:</strong> Valeur centrale</li>
                        <li><strong>Moustaches:</strong> Min et Max (hors outliers)</li>
                        <li><strong>Points:</strong> Valeurs aberrantes potentielles</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)
            
            # Calcul IQR
            Q1 = df[selected_var].quantile(0.25)
            Q3 = df[selected_var].quantile(0.75)
            IQR = Q3 - Q1
            
            st.markdown(f"""
                <div class="info-card green" style="margin-top: 1rem;">
                    <h4 style='color: #22c55e;'>📐 Quartiles</h4>
                    <p><strong>Q1:</strong> {Q1:.2f} cm</p>
                    <p><strong>Q2 (Médiane):</strong> {df[selected_var].median():.2f} cm</p>
                    <p><strong>Q3:</strong> {Q3:.2f} cm</p>
                    <p><strong>IQR:</strong> {IQR:.2f} cm</p>
                </div>
            """, unsafe_allow_html=True)
    
    with tab3:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Courbe de densité avec Plotly
            fig = go.Figure()
            
            # Histogramme
            fig.add_trace(go.Histogram(
                x=df[selected_var],
                histnorm='probability density',
                marker=dict(
                    color=COLOR_PALETTE['primary'],
                    opacity=0.6,
                    line=dict(color='white', width=1)
                ),
                name='Histogramme',
                nbinsx=25
            ))
            
            # Ajouter statistiques
            fig.add_vline(x=df[selected_var].mean(), line_dash="dash", line_color="red",
                         annotation_text=f"μ = {df[selected_var].mean():.2f}")
            fig.add_vline(x=df[selected_var].median(), line_dash="dot", line_color="green",
                         annotation_text=f"Médiane = {df[selected_var].median():.2f}")
            
            fig.update_layout(
                title={
                    'text': f'📈 Distribution de Probabilité - {variable_names[selected_var]}',
                    'font': {'size': 22, 'family': 'Poppins', 'color': '#667eea'}
                },
                xaxis_title=f'{variable_names[selected_var]} (cm)',
                yaxis_title='Densité de probabilité',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family='Poppins', size=13),
                height=500,
                showlegend=True,
                xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)'),
                yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)')
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Test de normalité visuel
            st.markdown("""
                <div class="info-card orange">
                    <h3 style='color: #f97316;'>📊 Analyse de Distribution</h3>
                """, unsafe_allow_html=True)
            
            skewness = df[selected_var].skew()
            kurtosis = df[selected_var].kurtosis()
            
            st.markdown(f"""
                    <p><strong>Asymétrie (Skewness):</strong> {skewness:.3f}</p>
                    <p><strong>Aplatissement (Kurtosis):</strong> {kurtosis:.3f}</p>
                """, unsafe_allow_html=True)
            
            if abs(skewness) < 0.5:
                st.markdown("<p>✅ <strong>Distribution quasi-symétrique</strong></p>", unsafe_allow_html=True)
            elif skewness > 0:
                st.markdown("<p>↗️ <strong>Distribution asymétrique à droite</strong></p>", unsafe_allow_html=True)
            else:
                st.markdown("<p>↙️ <strong>Distribution asymétrique à gauche</strong></p>", unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
    
    with tab4:
        st.markdown("<h3 style='color: #667eea;'>📊 Comparaison de Toutes les Variables</h3>", unsafe_allow_html=True)
        
        # Créer un dataframe pour comparaison
        comparison_data = []
        for var in variables:
            comparison_data.append({
                'Variable': variable_names[var],
                'Moyenne': df[var].mean(),
                'Médiane': df[var].median(),
                'Écart-type': df[var].std(),
                'Min': df[var].min(),
                'Max': df[var].max(),
                'Étendue': df[var].max() - df[var].min()
            })
        
        comparison_df = pd.DataFrame(comparison_data)
        
        # Tableau stylisé
        st.dataframe(
            comparison_df.style.background_gradient(cmap='RdYlGn', subset=['Moyenne', 'Médiane', 'Écart-type'])
                               .format(precision=2),
            use_container_width=True,
            height=250
        )
        
        # Graphique comparatif
        col1, col2 = st.columns(2)
        
        with col1:
            fig = go.Figure()
            
            for var in variables:
                fig.add_trace(go.Box(
                    y=df[var],
                    name=variable_names[var].split()[1],
                    marker=dict(color=COLOR_PALETTE[['setosa', 'versicolor', 'virginica', 'primary'][variables.index(var) % 4]]),
                    boxmean='sd'
                ))
            
            fig.update_layout(
                title='📦 Comparaison des Boxplots',
                yaxis_title='Valeur (cm)',
                height=400,
                font=dict(family='Poppins'),
                plot_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Graphique radar des moyennes
            categories = [variable_names[var].split()[1] for var in variables]
            values = [df[var].mean() for var in variables]
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself',
                marker=dict(color=COLOR_PALETTE['primary']),
                line=dict(color=COLOR_PALETTE['primary'], width=2)
            ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, max(values) * 1.2]
                    )
                ),
                title='🎯 Graphique Radar des Moyennes',
                height=400,
                font=dict(family='Poppins')
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    # Conclusion
    st.markdown("<div class='elegant-divider'></div>", unsafe_allow_html=True)
    st.markdown("""
        <div class="info-card green">
            <h3 style='color: #22c55e;'>✅ Conclusion de l'Exercice 2</h3>
            <p style='font-size: 1.1rem; line-height: 1.8;'>
                L'analyse des variables quantitatives révèle que les <strong>mesures des pétales</strong> 
                présentent une <strong>plus grande variabilité</strong> que celles des sépales. La longueur 
                des pétales varie de 1.0 à 6.9 cm (étendue de 5.9 cm), tandis que la largeur des sépales 
                varie seulement de 2.0 à 4.4 cm (étendue de 2.4 cm). Cette variabilité suggère que les 
                caractéristiques des pétales pourraient être plus <strong>discriminantes</strong> pour 
                différencier les espèces d'Iris.
            </p>
        </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════
#                    EXERCICE 3: ANALYSE BIVARIÉE
# ═══════════════════════════════════════════════════════════════════════════

elif menu_option == "🔗 Exercice 3 - Analyse bivariée":
    
    st.markdown("""
        <div class="section-card">
            <h1 class="section-title">🔗 Exercice 3: Analyse Bivariée (Nuages de Points)</h1>
            <p style='font-size: 1.1rem; color: #666;'>
                Étude des relations entre deux variables quantitatives et identification des patterns par espèce.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Sélection des variables
    col1, col2 = st.columns(2)
    
    variables = ['SepalLength', 'SepalWidth', 'PetalLength', 'PetalWidth']
    variable_names = {
        'SepalLength': 'Longueur du Sépale',
        'SepalWidth': 'Largeur du Sépale',
        'PetalLength': 'Longueur du Pétale',
        'PetalWidth': 'Largeur du Pétale'
    }
    
    with col1:
        x_var = st.selectbox("Variable X (axe horizontal):", variables, index=2, format_func=lambda x: variable_names[x])
    
    with col2:
        y_var = st.selectbox("Variable Y (axe vertical):", variables, index=3, format_func=lambda x: variable_names[x])
    
    # Calcul de la corrélation
    correlation = df[x_var].corr(df[y_var])
    
    # Afficher la corrélation
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        corr_color = COLOR_PALETTE['success'] if abs(correlation) > 0.7 else (COLOR_PALETTE['warning'] if abs(correlation) > 0.4 else COLOR_PALETTE['info'])
        st.markdown(f"""
            <div class="metric-card" style="background: {corr_color};">
                <div class="metric-label">Corrélation de Pearson</div>
                <div class="metric-value">{correlation:.3f}</div>
                <div style="margin-top: 0.5rem;">
                    {'💪 Forte' if abs(correlation) > 0.7 else ('👍 Modérée' if abs(correlation) > 0.4 else '👌 Faible')}
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div class='elegant-divider'></div>", unsafe_allow_html=True)
    
    # Tabs pour différentes visualisations
    tab1, tab2, tab3, tab4 = st.tabs(["🎨 Nuage de Points Standard", "🌈 Par Espèce", "📊 Avec Régression", "🔥 Heatmap de Densité"])
    
    with tab1:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            fig = px.scatter(
                df, x=x_var, y=y_var,
                color='Species',
                color_discrete_map={'setosa': COLOR_PALETTE['setosa'], 
                                  'versicolor': COLOR_PALETTE['versicolor'], 
                                  'virginica': COLOR_PALETTE['virginica']},
                size_max=15,
                template='plotly_white',
                title=f'🎨 {variable_names[x_var]} vs {variable_names[y_var]}',
                labels={x_var: f'{variable_names[x_var]} (cm)', 
                       y_var: f'{variable_names[y_var]} (cm)'}
            )
            
            fig.update_traces(marker=dict(size=10, line=dict(width=1, color='white')))
            
            fig.update_layout(
                height=550,
                font=dict(family='Poppins', size=14),
                title_font=dict(size=24, family='Poppins', color='#667eea'),
                legend=dict(
                    title='Espèce',
                    orientation="v",
                    yanchor="top",
                    y=1,
                    xanchor="right",
                    x=1.15,
                    bgcolor='rgba(255,255,255,0.8)',
                    bordercolor='#667eea',
                    borderwidth=2
                ),
                xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)'),
                yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)')
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("""
                <div class="info-card purple">
                    <h3 style='color: #8b5cf6;'>📊 Analyse de Corrélation</h3>
                """, unsafe_allow_html=True)
            
            if abs(correlation) > 0.7:
                st.markdown(f"""
                    <p style='color: green; font-weight: bold;'>✅ Corrélation FORTE ({correlation:.3f})</p>
                    <p>Les variables évoluent fortement ensemble. Une relation linéaire claire existe.</p>
                """, unsafe_allow_html=True)
            elif abs(correlation) > 0.4:
                st.markdown(f"""
                    <p style='color: orange; font-weight: bold;'>⚠️ Corrélation MODÉRÉE ({correlation:.3f})</p>
                    <p>Il existe une relation, mais elle n'est pas parfaitement linéaire.</p>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <p style='color: blue; font-weight: bold;'>ℹ️ Corrélation FAIBLE ({correlation:.3f})</p>
                    <p>Peu de relation linéaire entre ces variables.</p>
                """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Statistiques par espèce
            st.markdown("""
                <div class="info-card blue" style="margin-top: 1rem;">
                    <h3 style='color: #3b82f6;'>📈 Moyennes par Espèce</h3>
                """, unsafe_allow_html=True)
            
            for species in df['Species'].unique():
                subset = df[df['Species'] == species]
                mean_x = subset[x_var].mean()
                mean_y = subset[y_var].mean()
                st.markdown(f"""
                    <p><strong>{species}:</strong><br>
                    • X: {mean_x:.2f} cm<br>
                    • Y: {mean_y:.2f} cm</p>
                """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
    
    with tab2:
        # Graphique avec facettes par espèce
        fig = px.scatter(
            df, x=x_var, y=y_var,
            color='Species',
            facet_col='Species',
            color_discrete_map={'setosa': COLOR_PALETTE['setosa'], 
                              'versicolor': COLOR_PALETTE['versicolor'], 
                              'virginica': COLOR_PALETTE['virginica']},
            trendline="ols",
            template='plotly_white',
            title=f'🌈 Analyse par Espèce: {variable_names[x_var]} vs {variable_names[y_var]}',
            labels={x_var: f'{variable_names[x_var]} (cm)', 
                   y_var: f'{variable_names[y_var]} (cm)'}
        )
        
        fig.update_traces(marker=dict(size=8, line=dict(width=1, color='white')))
        
        fig.update_layout(
            height=400,
            font=dict(family='Poppins', size=12),
            title_font=dict(size=22, family='Poppins', color='#667eea'),
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Matrice de corrélation par espèce
        st.markdown("<h3 style='color: #667eea;'>📊 Corrélations par Espèce</h3>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        for i, (col, species) in enumerate(zip([col1, col2, col3], df['Species'].unique())):
            subset = df[df['Species'] == species]
            corr = subset[x_var].corr(subset[y_var])
            color = ['#FF6B6B', '#4ECDC4', '#45B7D1'][i]
            
            with col:
                st.markdown(f"""
                    <div class="metric-card" style="background: {color};">
                        <div class="metric-label">{species}</div>
                        <div class="metric-value">{corr:.3f}</div>
                    </div>
                """, unsafe_allow_html=True)
    
    with tab3:
        # Nuage de points avec ligne de régression
        fig = px.scatter(
            df, x=x_var, y=y_var,
            color='Species',
            color_discrete_map={'setosa': COLOR_PALETTE['setosa'], 
                              'versicolor': COLOR_PALETTE['versicolor'], 
                              'virginica': COLOR_PALETTE['virginica']},
            trendline="ols",
            template='plotly_white',
            title=f'📊 Avec Ligne de Régression: {variable_names[x_var]} vs {variable_names[y_var]}',
            labels={x_var: f'{variable_names[x_var]} (cm)', 
                   y_var: f'{variable_names[y_var]} (cm)'}
        )
        
        fig.update_traces(marker=dict(size=10, line=dict(width=1, color='white')))
        
        fig.update_layout(
            height=550,
            font=dict(family='Poppins', size=14),
            title_font=dict(size=24, family='Poppins', color='#667eea'),
            legend=dict(
                title='Espèce',
                bgcolor='rgba(255,255,255,0.8)',
                bordercolor='#667eea',
                borderwidth=2
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Équation de régression
        from sklearn.linear_model import LinearRegression
        
        X = df[x_var].values.reshape(-1, 1)
        y = df[y_var].values
        model = LinearRegression()
        model.fit(X, y)
        
        slope = model.coef_[0]
        intercept = model.intercept_
        r_squared = model.score(X, y)
        
        st.markdown(f"""
            <div class="info-card green">
                <h3 style='color: #22c55e;'>📐 Équation de Régression Linéaire</h3>
                <p style='font-size: 1.2rem; text-align: center; font-family: monospace; background: #f0fdf4; padding: 1rem; border-radius: 8px; margin: 1rem 0;'>
                    <strong>y = {slope:.4f}x + {intercept:.4f}</strong>
                </p>
                <p><strong>Coefficient de détermination (R²):</strong> {r_squared:.4f}</p>
                <p><strong>Interprétation:</strong> {r_squared*100:.2f}% de la variance de {variable_names[y_var]} 
                est expliquée par {variable_names[x_var]}.</p>
            </div>
        """, unsafe_allow_html=True)
    
    with tab4:
        # Heatmap de densité 2D
        fig = go.Figure()
        
        fig.add_trace(go.Histogram2dContour(
            x=df[x_var],
            y=df[y_var],
            colorscale='Viridis',
            showscale=True,
            contours=dict(
                showlabels=True,
                labelfont=dict(size=12, color='white')
            )
        ))
        
        # Ajouter les points
        for species in df['Species'].unique():
            subset = df[df['Species'] == species]
            fig.add_trace(go.Scatter(
                x=subset[x_var],
                y=subset[y_var],
                mode='markers',
                name=species,
                marker=dict(
                    size=6,
                    color={'setosa': COLOR_PALETTE['setosa'], 
                          'versicolor': COLOR_PALETTE['versicolor'], 
                          'virginica': COLOR_PALETTE['virginica']}[species],
                    line=dict(width=1, color='white')
                )
            ))
        
        fig.update_layout(
            title={
                'text': f'🔥 Carte de Densité: {variable_names[x_var]} vs {variable_names[y_var]}',
                'font': {'size': 24, 'family': 'Poppins', 'color': '#667eea'}
            },
            xaxis_title=f'{variable_names[x_var]} (cm)',
            yaxis_title=f'{variable_names[y_var]} (cm)',
            height=550,
            font=dict(family='Poppins', size=14),
            legend=dict(
                title='Espèce',
                bgcolor='rgba(255,255,255,0.8)',
                bordercolor='#667eea',
                borderwidth=2
            ),
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
            <div class="info-card blue">
                <h3 style='color: #3b82f6;'>💡 Interprétation de la Carte de Densité</h3>
                <p>Les zones plus sombres indiquent une <strong>concentration élevée</strong> de points. 
                Cette visualisation permet d'identifier les régions où les observations sont les plus denses 
                et de détecter les <strong>clusters naturels</strong> dans les données.</p>
            </div>
        """, unsafe_allow_html=True)
    
    # Matrice de corrélation complète
    st.markdown("<div class='elegant-divider'></div>", unsafe_allow_html=True)
    st.markdown("<h2 style='color: #667eea;'>🔗 Matrice de Corrélation Complète</h2>", unsafe_allow_html=True)
    
    corr_matrix = df[variables].corr()
    
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=[variable_names[v] for v in corr_matrix.columns],
        y=[variable_names[v] for v in corr_matrix.index],
        colorscale='RdBu_r',
        zmid=0,
        text=corr_matrix.values.round(3),
        texttemplate='%{text}',
        textfont={"size": 14},
        colorbar=dict(title="Corrélation")
    ))
    
    fig.update_layout(
        title={
            'text': '🔗 Matrice de Corrélation de Pearson',
            'font': {'size': 24, 'family': 'Poppins', 'color': '#667eea'}
        },
        height=500,
        font=dict(family='Poppins', size=12),
        xaxis=dict(side='bottom'),
        yaxis=dict(side='left')
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Top corrélations
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class="info-card green">
                <h3 style='color: #22c55e;'>💪 Corrélations Fortes (> 0.7)</h3>
            """, unsafe_allow_html=True)
        
        strong_corr = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr_val = corr_matrix.iloc[i, j]
                if abs(corr_val) > 0.7:
                    strong_corr.append({
                        'Var1': variable_names[corr_matrix.columns[i]],
                        'Var2': variable_names[corr_matrix.columns[j]],
                        'Corrélation': corr_val
                    })
        
        if strong_corr:
            for item in sorted(strong_corr, key=lambda x: abs(x['Corrélation']), reverse=True):
                st.markdown(f"<p>• <strong>{item['Var1']}</strong> ↔ <strong>{item['Var2']}</strong>: {item['Corrélation']:.3f}</p>", unsafe_allow_html=True)
        else:
            st.markdown("<p>Aucune corrélation forte détectée.</p>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="info-card orange">
                <h3 style='color: #f97316;'>👌 Corrélations Faibles (< 0.3)</h3>
            """, unsafe_allow_html=True)
        
        weak_corr = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr_val = corr_matrix.iloc[i, j]
                if abs(corr_val) < 0.3:
                    weak_corr.append({
                        'Var1': variable_names[corr_matrix.columns[i]],
                        'Var2': variable_names[corr_matrix.columns[j]],
                        'Corrélation': corr_val
                    })
        
        if weak_corr:
            for item in sorted(weak_corr, key=lambda x: abs(x['Corrélation'])):
                st.markdown(f"<p>• <strong>{item['Var1']}</strong> ↔ <strong>{item['Var2']}</strong>: {item['Corrélation']:.3f}</p>", unsafe_allow_html=True)
        else:
            st.markdown("<p>Aucune corrélation faible détectée.</p>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Conclusion
    st.markdown("<div class='elegant-divider'></div>", unsafe_allow_html=True)
    st.markdown("""
        <div class="info-card green">
            <h3 style='color: #22c55e;'>✅ Conclusion de l'Exercice 3</h3>
            <p style='font-size: 1.1rem; line-height: 1.8;'>
                L'analyse bivariée révèle des <strong>corrélations très fortes</strong> entre certaines variables, 
                notamment entre la <strong>longueur et la largeur des pétales (r = 0.96)</strong>. Les nuages de points 
                montrent également que l'espèce <strong>Setosa</strong> est clairement séparable des deux autres espèces 
                dans l'espace des pétales, tandis que <strong>Versicolor et Virginica</strong> présentent un certain 
                chevauchement. Ces observations suggèrent que les caractéristiques des pétales seront particulièrement 
                <strong>discriminantes</strong> pour nos modèles de classification.
            </p>
        </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════
#                       EXERCICE 4: BOXPLOTS
# ═══════════════════════════════════════════════════════════════════════════

elif menu_option == "📦 Exercice 4 - Boxplots":
    
    st.markdown("""
        <div class="section-card">
            <h1 class="section-title">📦 Exercice 4: Boxplots - Variable Qualitative vs Quantitative</h1>
            <p style='font-size: 1.1rem; color: #666;'>
                Visualisation de la distribution des variables quantitatives en fonction de l'espèce.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Sélection de variable
    variables = ['SepalLength', 'SepalWidth', 'PetalLength', 'PetalWidth']
    variable_names = {
        'SepalLength': '🌿 Longueur du Sépale',
        'SepalWidth': '🌿 Largeur du Sépale',
        'PetalLength': '🌺 Longueur du Pétale',
        'PetalWidth': '🌺 Largeur du Pétale'
    }
    
    selected_var = st.selectbox(
        "Choisir une variable à analyser:",
        variables,
        format_func=lambda x: variable_names[x]
    )
    
    st.markdown("<div class='elegant-divider'></div>", unsafe_allow_html=True)
    
    # Statistiques par espèce
    st.markdown(f"<h2 style='color: #667eea;'>📊 Statistiques de {variable_names[selected_var]} par Espèce</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    for i, (col, species) in enumerate(zip([col1, col2, col3], df['Species'].unique())):
        subset = df[df['Species'] == species]
        color = [COLOR_PALETTE['setosa'], COLOR_PALETTE['versicolor'], COLOR_PALETTE['virginica']][i]
        
        with col:
            st.markdown(f"""
                <div class="metric-card" style="background: {color};">
                    <h3 style="margin: 0; color: white;">{species.capitalize()}</h3>
                    <div style="margin-top: 1rem;">
                        <p><strong>Moyenne:</strong> {subset[selected_var].mean():.2f} cm</p>
                        <p><strong>Médiane:</strong> {subset[selected_var].median():.2f} cm</p>
                        <p><strong>Écart-type:</strong> {subset[selected_var].std():.2f} cm</p>
                        <p><strong>Min-Max:</strong> {subset[selected_var].min():.2f} - {subset[selected_var].max():.2f} cm</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<div class='elegant-divider'></div>", unsafe_allow_html=True)
    
    # Visualisations
    tab1, tab2, tab3, tab4 = st.tabs(["📦 Boxplot Standard", "🎻 Violin Plot", "📊 Box + Points", "📈 Comparaison Multiple"])
    
    with tab1:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            fig = go.Figure()
            
            for species in df['Species'].unique():
                subset = df[df['Species'] == species]
                color = {'setosa': COLOR_PALETTE['setosa'], 
                        'versicolor': COLOR_PALETTE['versicolor'], 
                        'virginica': COLOR_PALETTE['virginica']}[species]
                
                fig.add_trace(go.Box(
                    y=subset[selected_var],
                    name=species.capitalize(),
                    marker=dict(color=color),
                    boxmean='sd',
                    fillcolor=f"rgba{tuple(list(int(color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)) + [0.3])}",
                    line=dict(width=2)
                ))
            
            fig.update_layout(
                title={
                    'text': f'📦 Distribution de {variable_names[selected_var]} par Espèce',
                    'font': {'size': 24, 'family': 'Poppins', 'color': '#667eea'}
                },
                yaxis_title=f'{variable_names[selected_var]} (cm)',
                xaxis_title='Espèce',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family='Poppins', size=14),
                height=550,
                showlegend=True,
                legend=dict(
                    title='Espèce',
                    bgcolor='rgba(255,255,255,0.8)',
                    bordercolor='#667eea',
                    borderwidth=2
                ),
                yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)')
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("""
                <div class="info-card purple">
                    <h3 style='color: #8b5cf6;'>💡 Guide de Lecture</h3>
                    <ul style='line-height: 2;'>
                        <li><strong>Boîte:</strong> 50% des données (IQR)</li>
                        <li><strong>Ligne médiane:</strong> Valeur centrale</li>
                        <li><strong>Moustaches:</strong> Étendue des données</li>
                        <li><strong>Diamant:</strong> Moyenne ± écart-type</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)
            
            # Comparaison des médianes
            st.markdown("""
                <div class="info-card green" style="margin-top: 1rem;">
                    <h3 style='color: #22c55e;'>📊 Comparaison</h3>
                """, unsafe_allow_html=True)
            
            for species in df['Species'].unique():
                subset = df[df['Species'] == species]
                median_val = subset[selected_var].median()
                st.markdown(f"<p><strong>{species}:</strong> {median_val:.2f} cm</p>", unsafe_allow_html=True)
            
            # Différence max
            medians = [df[df['Species'] == s][selected_var].median() for s in df['Species'].unique()]
            diff = max(medians) - min(medians)
            st.markdown(f"<p style='margin-top: 1rem; padding: 0.5rem; background: #dcfce7; border-radius: 5px;'><strong>Différence max:</strong> {diff:.2f} cm</p>", unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
    
    with tab2:
        # Violin plot
        fig = go.Figure()
        
        for species in df['Species'].unique():
            subset = df[df['Species'] == species]
            color = {'setosa': COLOR_PALETTE['setosa'], 
                    'versicolor': COLOR_PALETTE['versicolor'], 
                    'virginica': COLOR_PALETTE['virginica']}[species]
            
            fig.add_trace(go.Violin(
                y=subset[selected_var],
                name=species.capitalize(),
                box_visible=True,
                meanline_visible=True,
                fillcolor=color,
                opacity=0.6,
                line_color=color
            ))
        
        fig.update_layout(
            title={
                'text': f'🎻 Violin Plot de {variable_names[selected_var]} par Espèce',
                'font': {'size': 24, 'family': 'Poppins', 'color': '#667eea'}
            },
            yaxis_title=f'{variable_names[selected_var]} (cm)',
            xaxis_title='Espèce',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Poppins', size=14),
            height=550,
            showlegend=True,
            yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)')
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
            <div class="info-card blue">
                <h3 style='color: #3b82f6;'>💡 Avantage du Violin Plot</h3>
                <p style='font-size: 1rem; line-height: 1.8;'>
                    Le violin plot combine les avantages du boxplot et de la courbe de densité. 
                    La <strong>largeur</strong> du "violon" indique la <strong>densité de probabilité</strong> 
                    à chaque niveau de valeur, permettant de visualiser la forme complète de la distribution.
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with tab3:
        # Boxplot avec points superposés
        fig = go.Figure()
        
        for species in df['Species'].unique():
            subset = df[df['Species'] == species]
            color = {'setosa': COLOR_PALETTE['setosa'], 
                    'versicolor': COLOR_PALETTE['versicolor'], 
                    'virginica': COLOR_PALETTE['virginica']}[species]
            
            # Boxplot
            fig.add_trace(go.Box(
                y=subset[selected_var],
                name=species.capitalize(),
                marker=dict(color=color),
                boxmean='sd',
                showlegend=True
            ))
            
            # Points
            fig.add_trace(go.Scatter(
                y=subset[selected_var],
                x=[species] * len(subset),
                mode='markers',
                name=f'{species} (points)',
                marker=dict(
                    color=color,
                    size=6,
                    opacity=0.4,
                    line=dict(width=1, color='white')
                ),
                showlegend=False
            ))
        
        fig.update_layout(
            title={
                'text': f'📊 Boxplot + Points: {variable_names[selected_var]}',
                'font': {'size': 24, 'family': 'Poppins', 'color': '#667eea'}
            },
            yaxis_title=f'{variable_names[selected_var]} (cm)',
            xaxis_title='Espèce',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Poppins', size=14),
            height=550,
            yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)')
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        # Comparaison de toutes les variables
        st.markdown("<h3 style='color: #667eea;'>📊 Comparaison de Toutes les Variables</h3>", unsafe_allow_html=True)
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=[variable_names[v] for v in variables],
            vertical_spacing=0.12,
            horizontal_spacing=0.1
        )
        
        for idx, var in enumerate(variables):
            row = idx // 2 + 1
            col = idx % 2 + 1
            
            for species_idx, species in enumerate(df['Species'].unique()):
                subset = df[df['Species'] == species]
                color = [COLOR_PALETTE['setosa'], COLOR_PALETTE['versicolor'], COLOR_PALETTE['virginica']][species_idx]
                
                fig.add_trace(
                    go.Box(
                        y=subset[var],
                        name=species if idx == 0 else None,
                        marker=dict(color=color),
                        legendgroup=species,
                        showlegend=(idx == 0),
                        boxmean='sd'
                    ),
                    row=row, col=col
                )
        
        fig.update_layout(
            height=700,
            title={
                'text': '📈 Comparaison Multi-variables par Espèce',
                'font': {'size': 22, 'family': 'Poppins', 'color': '#667eea'}
            },
            font=dict(family='Poppins', size=12),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=True,
            legend=dict(
                title='Espèce',
                bgcolor='rgba(255,255,255,0.8)',
                bordercolor='#667eea',
                borderwidth=2
            )
        )
        
        fig.update_yaxes(title_text="Valeur (cm)", showgrid=True, gridcolor='rgba(0,0,0,0.1)')
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Test statistique ANOVA
    st.markdown("<div class='elegant-divider'></div>", unsafe_allow_html=True)
    st.markdown("<h2 style='color: #667eea;'>📊 Test ANOVA (Analyse de Variance)</h2>", unsafe_allow_html=True)
    
    from scipy import stats
    
    groups = [df[df['Species'] == species][selected_var] for species in df['Species'].unique()]
    f_stat, p_value = stats.f_oneway(*groups)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Statistique F</div>
                <div class="metric-value">{f_stat:.2f}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="metric-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
                <div class="metric-label">p-value</div>
                <div class="metric-value">{p_value:.2e}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        significance = "✅ Significatif" if p_value < 0.05 else "❌ Non significatif"
        color = COLOR_PALETTE['success'] if p_value < 0.05 else COLOR_PALETTE['warning']
        st.markdown(f"""
            <div class="metric-card" style="background: {color};">
                <div class="metric-label">Résultat (α=0.05)</div>
                <div class="metric-value" style="font-size: 1.5rem;">{significance}</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="info-card {'green' if p_value < 0.05 else 'orange'}">
            <h3 style='color: {'#22c55e' if p_value < 0.05 else '#f97316'};'>💡 Interprétation du Test ANOVA</h3>
            <p style='font-size: 1.1rem; line-height: 1.8;'>
                {'<strong>Les moyennes sont significativement différentes</strong> entre les trois espèces pour cette variable (p < 0.05). Cela signifie que cette caractéristique morphologique peut aider à <strong>discriminer</strong> les espèces.' if p_value < 0.05 else 'Les moyennes ne sont <strong>pas significativement différentes</strong> entre les trois espèces pour cette variable (p ≥ 0.05). Cette caractéristique est moins discriminante.'}
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Conclusion
    st.markdown("<div class='elegant-divider'></div>", unsafe_allow_html=True)
    st.markdown("""
        <div class="info-card green">
            <h3 style='color: #22c55e;'>✅ Conclusion de l'Exercice 4</h3>
            <p style='font-size: 1.1rem; line-height: 1.8;'>
                Les boxplots révèlent des <strong>différences marquées</strong> dans les distributions des variables 
                morphologiques entre les trois espèces. L'espèce <strong>Setosa</strong> se distingue clairement par 
                des pétales significativement plus courts et plus étroits. Les tests ANOVA confirment que ces différences 
                sont <strong>statistiquement significatives</strong>, validant l'utilité de ces variables pour la 
                classification. Les violons plots montrent également des distributions souvent <strong>bimodales ou 
                asymétriques</strong>, suggérant des sous-groupes au sein de certaines espèces.
            </p>
        </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════
#                  EXERCICE 5: VISUALISATIONS AVANCÉES
# ═══════════════════════════════════════════════════════════════════════════

elif menu_option == "🎨 Exercice 5 - Visualisations avancées":
    
    st.markdown("""
        <div class="section-card">
            <h1 class="section-title">🎨 Exercice 5: Visualisations Avancées et Corrélations</h1>
            <p style='font-size: 1.1rem; color: #666;'>
                Exploration approfondie des relations multivariées avec des visualisations sophistiquées.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🎯 Pairplot Complet", 
        "🔗 Matrice de Corrélation",
        "🌐 Visualisation 3D",
        "📊 Parallel Coordinates",
        "🎨 Graphiques Avancés"
    ])
    
    with tab1:
        st.markdown("<h2 style='color: #667eea;'>🎯 Pairplot - Relations entre Toutes les Variables</h2>", unsafe_allow_html=True)
        
        st.markdown("""
            <div class="info-card blue">
                <h3 style='color: #3b82f6;'>💡 À propos du Pairplot</h3>
                <p>Le pairplot affiche les relations deux à deux entre toutes les variables numériques. 
                Sur la diagonale, les histogrammes montrent la distribution de chaque variable. 
                Hors diagonale, les nuages de points révèlent les corrélations.</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Créer un pairplot personnalisé avec Plotly
        variables = ['SepalLength', 'SepalWidth', 'PetalLength', 'PetalWidth']
        n_vars = len(variables)
        
        fig = make_subplots(
            rows=n_vars, cols=n_vars,
            subplot_titles=[f"{v.replace('Sepal', 'Sep.').replace('Petal', 'Pet.').replace('Length', 'L').replace('Width', 'W')}" 
                           for _ in range(n_vars) for v in variables],
            vertical_spacing=0.05,
            horizontal_spacing=0.05
        )
        
        for i, var_y in enumerate(variables):
            for j, var_x in enumerate(variables):
                row, col = i + 1, j + 1
                
                if i == j:
                    # Diagonale: histogrammes par espèce
                    for species in df['Species'].unique():
                        subset = df[df['Species'] == species]
                        color = {'setosa': COLOR_PALETTE['setosa'], 
                                'versicolor': COLOR_PALETTE['versicolor'], 
                                'virginica': COLOR_PALETTE['virginica']}[species]
                        
                        fig.add_trace(
                            go.Histogram(
                                x=subset[var_x],
                                name=species if i == 0 and j == 0 else None,
                                marker=dict(color=color, opacity=0.6),
                                legendgroup=species,
                                showlegend=(i == 0 and j == 0),
                                nbinsx=15
                            ),
                            row=row, col=col
                        )
                else:
                    # Hors diagonale: scatter plots
                    for species in df['Species'].unique():
                        subset = df[df['Species'] == species]
                        color = {'setosa': COLOR_PALETTE['setosa'], 
                                'versicolor': COLOR_PALETTE['versicolor'], 
                                'virginica': COLOR_PALETTE['virginica']}[species]
                        
                        fig.add_trace(
                            go.Scatter(
                                x=subset[var_x],
                                y=subset[var_y],
                                mode='markers',
                                name=species if i == 0 and j == 1 else None,
                                marker=dict(color=color, size=4, opacity=0.6),
                                legendgroup=species,
                                showlegend=False
                            ),
                            row=row, col=col
                        )
        
        fig.update_layout(
            height=900,
            title={
                'text': '🎯 Pairplot Complet des Variables Iris',
                'font': {'size': 24, 'family': 'Poppins', 'color': '#667eea'}
            },
            showlegend=True,
            legend=dict(
                title='Espèce',
                bgcolor='rgba(255,255,255,0.9)',
                bordercolor='#667eea',
                borderwidth=2,
                x=1.02,
                y=0.5
            ),
            font=dict(family='Poppins', size=10),
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        # Supprimer les titres des axes répétitifs
        fig.update_xaxes(showticklabels=False)
        fig.update_yaxes(showticklabels=False)
        
        # Ajouter les labels uniquement sur les bords
        for i in range(n_vars):
            fig.update_xaxes(title_text=variables[i].replace('Sepal', 'Sep.').replace('Petal', 'Pet.'), 
                           row=n_vars, col=i+1, showticklabels=True)
            fig.update_yaxes(title_text=variables[i].replace('Sepal', 'Sep.').replace('Petal', 'Pet.'), 
                           row=i+1, col=1, showticklabels=True)
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Observations clés
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
                <div class="info-card green">
                    <h3 style='color: #22c55e;'>✅ Observations Clés</h3>
                    <ul style='line-height: 2;'>
                        <li>Setosa clairement séparée</li>
                        <li>Forte corrélation pétales</li>
                        <li>Versicolor-Virginica se chevauchent</li>
                        <li>Sépales moins discriminants</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
                <div class="info-card purple">
                    <h3 style='color: #8b5cf6;'>🎯 Pour le ML</h3>
                    <ul style='line-height: 2;'>
                        <li>Pétales = features importantes</li>
                        <li>Setosa facilement classifiable</li>
                        <li>Challenge: séparer les 2 autres</li>
                        <li>Pas de transformation nécessaire</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("<h2 style='color: #667eea;'>🔗 Analyse Complète des Corrélations</h2>", unsafe_allow_html=True)
        
        # Matrice de corrélation
        corr_matrix = df[['SepalLength', 'SepalWidth', 'PetalLength', 'PetalWidth']].corr()
        
        # Heatmap
        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=['Sep. Length', 'Sep. Width', 'Pet. Length', 'Pet. Width'],
            y=['Sep. Length', 'Sep. Width', 'Pet. Length', 'Pet. Width'],
            colorscale='RdBu_r',
            zmid=0,
            text=corr_matrix.values.round(3),
            texttemplate='<b>%{text}</b>',
            textfont={"size": 16, "color": "white"},
            colorbar=dict(
                title="Corrélation",
                titleside="right",
                tickmode="linear",
                tick0=-1,
                dtick=0.5
            ),
            hovertemplate='%{x} vs %{y}<br>Corrélation: %{z:.3f}<extra></extra>'
        ))
        
        fig.update_layout(
            title={
                'text': '🔗 Matrice de Corrélation de Pearson',
                'font': {'size': 24, 'family': 'Poppins', 'color': '#667eea'}
            },
            height=600,
            font=dict(family='Poppins', size=14),
            xaxis=dict(side='bottom'),
            yaxis=dict(side='left')
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Tableau des corrélations
        st.markdown("<h3 style='color: #667eea;'>📊 Tableau Détaillé des Corrélations</h3>", unsafe_allow_html=True)
        
        corr_list = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr_list.append({
                    'Variable 1': corr_matrix.columns[i],
                    'Variable 2': corr_matrix.columns[j],
                    'Corrélation': corr_matrix.iloc[i, j],
                    'Force': 'Forte (>0.7)' if abs(corr_matrix.iloc[i, j]) > 0.7 else 
                            ('Modérée (0.4-0.7)' if abs(corr_matrix.iloc[i, j]) > 0.4 else 'Faible (<0.4)')
                })
        
        corr_df = pd.DataFrame(corr_list).sort_values('Corrélation', key=abs, ascending=False)
        
        st.dataframe(
            corr_df.style.background_gradient(cmap='RdYlGn', subset=['Corrélation'], vmin=-1, vmax=1)
                        .format({'Corrélation': '{:.3f}'}),
            use_container_width=True,
            height=300
        )
        
        # Graphique des corrélations
        fig = px.bar(
            corr_df,
            x='Variable 1',
            y='Corrélation',
            color='Force',
            color_discrete_map={
                'Forte (>0.7)': COLOR_PALETTE['success'],
                'Modérée (0.4-0.7)': COLOR_PALETTE['warning'],
                'Faible (<0.4)': COLOR_PALETTE['info']
            },
            title='📊 Force des Corrélations',
            labels={'Corrélation': 'Coefficient de Corrélation'},
            hover_data=['Variable 2']
        )
        
        fig.update_layout(
            height=400,
            font=dict(family='Poppins'),
            title_font=dict(size=20, color='#667eea')
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Corrélations par espèce
        st.markdown("<h3 style='color: #667eea;'>🔬 Corrélations par Espèce</h3>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        for i, (col, species) in enumerate(zip([col1, col2, col3], df['Species'].unique())):
            subset = df[df['Species'] == species]
            corr_species = subset[['SepalLength', 'SepalWidth', 'PetalLength', 'PetalWidth']].corr()
            
            with col:
                st.markdown(f"<h4 style='text-align: center; color: {[COLOR_PALETTE['setosa'], COLOR_PALETTE['versicolor'], COLOR_PALETTE['virginica']][i]};'>{species.capitalize()}</h4>", unsafe_allow_html=True)
                
                fig = go.Figure(data=go.Heatmap(
                    z=corr_species.values,
                    x=['SL', 'SW', 'PL', 'PW'],
                    y=['SL', 'SW', 'PL', 'PW'],
                    colorscale='RdBu_r',
                    zmid=0,
                    text=corr_species.values.round(2),
                    texttemplate='%{text}',
                    textfont={"size": 10},
                    showscale=False
                ))
                
                fig.update_layout(
                    height=300,
                    margin=dict(l=20, r=20, t=20, b=20),
                    xaxis=dict(side='bottom'),
                    yaxis=dict(side='left')
                )
                
                st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.markdown("<h2 style='color: #667eea;'>🌐 Visualisation 3D Interactive</h2>", unsafe_allow_html=True)
        
        # Sélection des axes
        col1, col2, col3 = st.columns(3)
        
        variables = ['SepalLength', 'SepalWidth', 'PetalLength', 'PetalWidth']
        var_names = {
            'SepalLength': 'Longueur Sépale',
            'SepalWidth': 'Largeur Sépale',
            'PetalLength': 'Longueur Pétale',
            'PetalWidth': 'Largeur Pétale'
        }
        
        with col1:
            x_axis = st.selectbox("Axe X:", variables, index=0, format_func=lambda x: var_names[x])
        with col2:
            y_axis = st.selectbox("Axe Y:", variables, index=2, format_func=lambda x: var_names[x])
        with col3:
            z_axis = st.selectbox("Axe Z:", variables, index=3, format_func=lambda x: var_names[x])
        
        # Graphique 3D
        fig = px.scatter_3d(
            df, x=x_axis, y=y_axis, z=z_axis,
            color='Species',
            color_discrete_map={
                'setosa': COLOR_PALETTE['setosa'],
                'versicolor': COLOR_PALETTE['versicolor'],
                'virginica': COLOR_PALETTE['virginica']
            },
            symbol='Species',
            size_max=10,
            opacity=0.8,
            title=f'🌐 Espace 3D: {var_names[x_axis]} × {var_names[y_axis]} × {var_names[z_axis]}',
            labels={
                x_axis: f'{var_names[x_axis]} (cm)',
                y_axis: f'{var_names[y_axis]} (cm)',
                z_axis: f'{var_names[z_axis]} (cm)'
            }
        )
        
        fig.update_traces(marker=dict(size=6, line=dict(width=0.5, color='white')))
        
        fig.update_layout(
            height=700,
            font=dict(family='Poppins', size=12),
            title_font=dict(size=24, color='#667eea'),
            legend=dict(
                title='Espèce',
                bgcolor='rgba(255,255,255,0.9)',
                bordercolor='#667eea',
                borderwidth=2
            ),
            scene=dict(
                xaxis=dict(backgroundcolor='rgba(0,0,0,0.02)', gridcolor='rgba(0,0,0,0.1)'),
                yaxis=dict(backgroundcolor='rgba(0,0,0,0.02)', gridcolor='rgba(0,0,0,0.1)'),
                zaxis=dict(backgroundcolor='rgba(0,0,0,0.02)', gridcolor='rgba(0,0,0,0.1)')
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
            <div class="info-card purple">
                <h3 style='color: #8b5cf6;'>💡 Manipulation du Graphique 3D</h3>
                <ul style='line-height: 2;'>
                    <li><strong>Rotation:</strong> Cliquez et glissez pour faire pivoter</li>
                    <li><strong>Zoom:</strong> Utilisez la molette de la souris</li>
                    <li><strong>Pan:</strong> Clic droit + glisser</li>
                    <li><strong>Reset:</strong> Double-clic pour réinitialiser</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    
    with tab4:
        st.markdown("<h2 style='color: #667eea;'>📊 Parallel Coordinates Plot</h2>", unsafe_allow_html=True)
        
        st.markdown("""
            <div class="info-card blue">
                <h3 style='color: #3b82f6;'>💡 À propos de ce graphique</h3>
                <p>Le Parallel Coordinates Plot permet de visualiser des données multidimensionnelles. 
                Chaque axe vertical représente une variable, et chaque ligne colorée représente une observation 
                traversant toutes les variables.</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Préparer les données pour parallel coordinates
        df_plot = df.copy()
        df_plot['Species_num'] = df_plot['Species'].map({'setosa': 0, 'versicolor': 1, 'virginica': 2})
        
        fig = go.Figure(data=
            go.Parcoords(
                line=dict(
                    color=df_plot['Species_num'],
                    colorscale=[
                        [0, COLOR_PALETTE['setosa']],
                        [0.5, COLOR_PALETTE['versicolor']],
                        [1, COLOR_PALETTE['virginica']]
                    ],
                    showscale=True,
                    cmin=0,
                    cmax=2,
                    colorbar=dict(
                        title="Espèce",
                        tickvals=[0, 1, 2],
                        ticktext=['Setosa', 'Versicolor', 'Virginica']
                    )
                ),
                dimensions=[
                    dict(range=[df['SepalLength'].min(), df['SepalLength'].max()],
                         label='Longueur Sépale', values=df['SepalLength']),
                    dict(range=[df['SepalWidth'].min(), df['SepalWidth'].max()],
                         label='Largeur Sépale', values=df['SepalWidth']),
                    dict(range=[df['PetalLength'].min(), df['PetalLength'].max()],
                         label='Longueur Pétale', values=df['PetalLength']),
                    dict(range=[df['PetalWidth'].min(), df['PetalWidth'].max()],
                         label='Largeur Pétale', values=df['PetalWidth'])
                ]
            )
        )
        
        fig.update_layout(
            title={
                'text': '📊 Parallel Coordinates - Toutes les Variables',
                'font': {'size': 24, 'family': 'Poppins', 'color': '#667eea'}
            },
            height=600,
            font=dict(family='Poppins', size=14),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
            <div class="info-card green">
                <h3 style='color: #22c55e;'>✅ Observations</h3>
                <p style='line-height: 1.8;'>
                    Ce graphique permet de voir que:
                    <ul>
                        <li>Les lignes <strong style='color: #FF6B6B;'>rouges (Setosa)</strong> se regroupent dans la partie inférieure des axes des pétales</li>
                        <li>Les lignes <strong style='color: #4ECDC4;'>turquoise (Versicolor)</strong> occupent une position intermédiaire</li>
                        <li>Les lignes <strong style='color: #45B7D1;'>bleues (Virginica)</strong> atteignent les valeurs supérieures pour les pétales</li>
                        <li>Il y a un <strong>chevauchement</strong> entre Versicolor et Virginica sur certaines variables</li>
                    </ul>
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with tab5:
        st.markdown("<h2 style='color: #667eea;'>🎨 Autres Visualisations Avancées</h2>", unsafe_allow_html=True)
        
        viz_type = st.selectbox(
            "Choisir un type de visualisation:",
            ["Radar Chart", "Bubble Chart", "Sunburst Chart", "Treemap"]
        )
        
        if viz_type == "Radar Chart":
            # Moyennes par espèce
            means_by_species = df.groupby('Species')[['SepalLength', 'SepalWidth', 'PetalLength', 'PetalWidth']].mean()
            
            fig = go.Figure()
            
            categories = ['Longueur<br>Sépale', 'Largeur<br>Sépale', 'Longueur<br>Pétale', 'Largeur<br>Pétale']
            
            for species in means_by_species.index:
                fig.add_trace(go.Scatterpolar(
                    r=means_by_species.loc[species].values,
                    theta=categories,
                    fill='toself',
                    name=species.capitalize(),
                    marker=dict(
                        color={'setosa': COLOR_PALETTE['setosa'], 
                              'versicolor': COLOR_PALETTE['versicolor'], 
                              'virginica': COLOR_PALETTE['virginica']}[species]
                    ),
                    line=dict(width=2)
                ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, means_by_species.values.max() * 1.1]
                    )
                ),
                title={
                    'text': '🎯 Radar Chart - Moyennes par Espèce',
                    'font': {'size': 24, 'family': 'Poppins', 'color': '#667eea'}
                },
                showlegend=True,
                height=600,
                font=dict(family='Poppins', size=14)
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        elif viz_type == "Bubble Chart":
            # Bubble chart avec taille basée sur une 4e dimension
            fig = px.scatter(
                df, x='PetalLength', y='PetalWidth',
                size='SepalLength', color='Species',
                size_max=30,
                color_discrete_map={
                    'setosa': COLOR_PALETTE['setosa'],
                    'versicolor': COLOR_PALETTE['versicolor'],
                    'virginica': COLOR_PALETTE['virginica']
                },
                hover_data=['SepalWidth'],
                title='🫧 Bubble Chart - Pétales (taille = longueur sépale)',
                labels={
                    'PetalLength': 'Longueur Pétale (cm)',
                    'PetalWidth': 'Largeur Pétale (cm)',
                    'SepalLength': 'Longueur Sépale (cm)'
                }
            )
            
            fig.update_traces(marker=dict(line=dict(width=2, color='white')))
            
            fig.update_layout(
                height=600,
                font=dict(family='Poppins', size=14),
                title_font=dict(size=24, color='#667eea')
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        elif viz_type == "Sunburst Chart":
            # Créer des catégories de taille pour le sunburst
            df_sunburst = df.copy()
            df_sunburst['PetalSize'] = pd.cut(df_sunburst['PetalLength'], 
                                             bins=[0, 2, 4, 7], 
                                             labels=['Petit', 'Moyen', 'Grand'])
            
            fig = px.sunburst(
                df_sunburst,
                path=['Species', 'PetalSize'],
                title='☀️ Sunburst - Distribution par Espèce et Taille de Pétale',
                color='Species',
                color_discrete_map={
                    'setosa': COLOR_PALETTE['setosa'],
                    'versicolor': COLOR_PALETTE['versicolor'],
                    'virginica': COLOR_PALETTE['virginica']
                }
            )
            
            fig.update_layout(
                height=600,
                font=dict(family='Poppins', size=14),
                title_font=dict(size=24, color='#667eea')
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        else:  # Treemap
            # Treemap avec effectifs
            species_counts = df['Species'].value_counts().reset_index()
            species_counts.columns = ['Species', 'Count']
            
            fig = px.treemap(
                species_counts,
                path=['Species'],
                values='Count',
                title='🗺️ Treemap - Répartition des Espèces',
                color='Species',
                color_discrete_map={
                    'setosa': COLOR_PALETTE['setosa'],
                    'versicolor': COLOR_PALETTE['versicolor'],
                    'virginica': COLOR_PALETTE['virginica']
                }
            )
            
            fig.update_traces(
                textinfo='label+value+percent parent',
                textfont=dict(size=20, family='Poppins', color='white')
            )
            
            fig.update_layout(
                height=500,
                font=dict(family='Poppins', size=14),
                title_font=dict(size=24, color='#667eea')
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    # Conclusion
    st.markdown("<div class='elegant-divider'></div>", unsafe_allow_html=True)
    st.markdown("""
        <div class="info-card green">
            <h3 style='color: #22c55e;'>✅ Conclusion de l'Exercice 5</h3>
            <p style='font-size: 1.1rem; line-height: 1.8;'>
                Les visualisations avancées confirment et enrichissent nos observations précédentes:
                <ul>
                    <li>Le <strong>pairplot</strong> montre une séparation nette de Setosa dans l'espace des pétales</li>
                    <li>La <strong>matrice de corrélation</strong> révèle une très forte corrélation (0.96) entre longueur et largeur des pétales</li>
                    <li>La visualisation <strong>3D</strong> démontre que les trois espèces occupent des régions distinctes de l'espace multidimensionnel</li>
                    <li>Le <strong>parallel coordinates plot</strong> illustre les patterns de séparation à travers toutes les dimensions simultanément</li>
                </ul>
                Ces insights visuels guideront la sélection des features et la stratégie de modélisation pour le machine learning.
            </p>
        </div>
    """, unsafe_allow_html=True)

# Le code continue dans le prochain message avec les Exercices 6 et 7...

# ═══════════════════════════════════════════════════════════════════════════
#                              FOOTER
# ═══════════════════════════════════════════════════════════════════════════

st.markdown("""
    <div class="footer">
        <h3 style='margin: 0;'>🌸 TP Iris - IA 🌸</h3>
        <p>Module INFO4111 | Année 2025-2026</p>
        <p style='margin-top: 1rem; font-size: 0.9rem;'>
           Par TCHUENTEU GUETCHUENG David - 20U2891
        </p>
    </div>
""", unsafe_allow_html=True)