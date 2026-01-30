<<<<<<< HEAD
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
=======
import os
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from matplotlib import cm
from matplotlib.colors import LinearSegmentedColormap

# ============================================================================
# CONFIGURATION DE LA PAGE
# ============================================================================

st.set_page_config(
    page_title="TP1 - Classification des Iris",
>>>>>>> a9cc1fa4cdb8ee150b9179b7ade5923cb663abd5
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

<<<<<<< HEAD
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
=======
# ============================================================================
# FONCTIONS UTILITAIRES
# ============================================================================

@st.cache_data
def load_data():
    # Utilisez le chemin relatif correct
    data_path = 'iris.csv'  # ou './iris.csv'
    
    # Vérifiez si le fichier existe
    if not os.path.exists(data_path):
        st.error(f"Fichier non trouvé : {data_path}")
        st.info("Vérifiez que le fichier est bien dans le même répertoire que iris.py")
        return None
    
    # Chargez les données
    df = pd.read_csv(data_path, sep=';')
    return df

def linear_regression(x, y):
    """Calcule la régression linéaire simple y = mx + b"""
    n = len(x)
    sum_x = np.sum(x)
    sum_y = np.sum(y)
    sum_xy = np.sum(x * y)
    sum_x2 = np.sum(x ** 2)
    
    m = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
    b = (sum_y - m * sum_x) / n
    
    return m, b

# ============================================================================
# PALETTES DE COULEURS AMÉLIORÉES
# ============================================================================

# Palette principale pour les espèces
species_palette = {
    'setosa': '#FF6B6B',      # Rouge corail
    'versicolor': '#4ECDC4',   # Turquoise
    'virginica': '#FFD166'     # Jaune doré
}

# Palette pour les variables quantitatives
variable_palette = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFD166', '#9D4EDD']

# Palette dégradée pour les heatmaps
heatmap_cmap = LinearSegmentedColormap.from_list('custom_heatmap', 
                                                 ['#2E86AB', '#A23B72', '#F18F01'])

# ============================================================================
# MENU LATÉRAL
# ============================================================================

with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/4/41/Iris_versicolor_3.jpg", 
             width=200, caption="Fleur Iris")
    
    st.title("🌸 TP1 - Classification des Iris")
    st.markdown("**TCHUENTEU GUETCHUENG DAVID**")
    st.markdown("**20U2891**")
    
    st.markdown("---")
    
    menu_option = st.radio(
        "📚 Navigation",
        [
            "🏠 Accueil",
            "📊 Exercice 1 - Analyse qualitative",
            "📏 Exercice 2 - Variables quantitatives",
            "🔗 Exercice 3 - Analyse bivariée",
            "📦 Exercice 4 - Boxplots",
            "🎨 Exercice 5 - Visualisations avancées",
            "🤖 Modélisation KNN",
            "📈 Optimisation & Comparaison"
        ]
    )
    
    st.markdown("---")
    st.markdown("### Paramètres d'affichage")
    
    # Options d'affichage
    use_plotly = st.checkbox("Utiliser Plotly (graphiques interactifs)", value=True)
    dark_mode = st.checkbox("Mode sombre", value=False)
    
    if dark_mode:
        plt.style.use('dark_background')
        st.markdown("*Mode somme activé*")
    else:
        plt.style.use('default')
    
    st.markdown("---")
    st.markdown("### Export des données")
    
    if st.button("📥 Exporter tout le rapport"):
        st.info("Fonction d'export à implémenter")

# ============================================================================
# CHARGEMENT DES DONNÉES
# ============================================================================

df = load_data()

# Noms français des variables
french_names = {
    'SepalLength': 'Longueur du sépale',
    'SepalWidth': 'Largeur du sépale',
    'PetalLength': 'Longueur du pétale',
    'PetalWidth': 'Largeur du pétale',
    'species': 'Espèce'
}

# Variables quantitatives
quantitative_vars = ['SepalLength', 'SepalWidth', 'PetalLength', 'PetalWidth']

# ============================================================================
# PAGE D'ACCUEIL
# ============================================================================

if menu_option == "🏠 Accueil":
    st.title("TP N°1: Classification des fleurs Iris")
    
>>>>>>> a9cc1fa4cdb8ee150b9179b7ade5923cb663abd5
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
<<<<<<< HEAD
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
=======
        ### 🌺 Contexte du TP
        
        Ce TP utilise le célèbre dataset **Iris** collecté par Edgar Anderson, contenant les mesures morphologiques 
        de trois espèces de fleurs Iris :
        
        - **Iris setosa** 🌸
        - **Iris versicolor** 🌺  
        - **Iris virginica** 💮
        
        ### 📋 Objectifs pédagogiques
        
        1. **Familiarisation** avec Python pour la Data Science
        2. **Manipulation** des librairies pandas, numpy, matplotlib, seaborn
        3. **Chargement et exploration** des données Iris
        4. **Visualisation** avancée des données
        5. **Préparation** des données pour le Machine Learning
        6. **Création et entraînement** d'un modèle KNN
        7. **Évaluation et optimisation** du modèle
        8. **Déploiement** d'une application interactive
        
        ### 📊 Structure du dataset
        
        Le dataset contient 150 observations avec 5 variables :
        """)
        
        info_df = pd.DataFrame({
            'Variable': ['SepalLength', 'SepalWidth', 'PetalLength', 'PetalWidth', 'species'],
            'Description': ['Longueur du sépale (cm)', 'Largeur du sépale (cm)', 
                          'Longueur du pétale (cm)', 'Largeur du pétale (cm)', 'Espèce'],
            'Type': ['Quantitative continue', 'Quantitative continue', 
                    'Quantitative continue', 'Quantitative continue', 'Qualitative nominale']
        })
        st.dataframe(info_df, use_container_width=True)
    
    with col2:
        # Aperçu des données
        st.markdown("### 👁️ Aperçu des données")
        st.dataframe(df.head(10), use_container_width=True)
        
        st.markdown("### 📈 Statistiques rapides")
        st.metric("Nombre total d'échantillons", len(df))
        st.metric("Nombre d'espèces", df['species'].nunique())
        
        for species in df['species'].unique():
            count = len(df[df['species'] == species])
            st.metric(f"Nombre de {species}", count)
    
    # Visualisation d'introduction
    st.markdown("---")
    st.markdown("### 🎨 Vue d'ensemble des espèces")
    
    fig_intro, axes_intro = plt.subplots(1, 3, figsize=(15, 5))
    
    # 1. Distribution des espèces
    species_counts = df['species'].value_counts()
    axes_intro[0].bar(species_counts.index, species_counts.values, 
                     color=[species_palette[s] for s in species_counts.index])
    axes_intro[0].set_title('Distribution des espèces', fontweight='bold')
    axes_intro[0].set_xlabel('Espèce')
    axes_intro[0].set_ylabel('Nombre')
    axes_intro[0].grid(alpha=0.3)
    
    # Ajouter les valeurs sur les barres
    for i, (species, count) in enumerate(species_counts.items()):
        axes_intro[0].text(i, count + 1, str(count), ha='center', fontweight='bold')
    
    # 2. Boxplot de PetalLength
    box_data = [df[df['species'] == s]['PetalLength'].values for s in df['species'].unique()]
    bp = axes_intro[1].boxplot(box_data, patch_artist=True, 
                              labels=df['species'].unique())
    
    # Colorier les boxplots
    for patch, species in zip(bp['boxes'], df['species'].unique()):
        patch.set_facecolor(species_palette[species])
    
    axes_intro[1].set_title('Longueur des pétales par espèce', fontweight='bold')
    axes_intro[1].set_ylabel('Longueur (cm)')
    axes_intro[1].grid(alpha=0.3)
    
    # 3. Scatter plot PetalLength vs PetalWidth
    for species in df['species'].unique():
        subset = df[df['species'] == species]
        axes_intro[2].scatter(subset['PetalLength'], subset['PetalWidth'],
                            color=species_palette[species], label=species, alpha=0.7)
    
    axes_intro[2].set_title('Relation Longueur/Largeur des pétales', fontweight='bold')
    axes_intro[2].set_xlabel('Longueur pétale (cm)')
    axes_intro[2].set_ylabel('Largeur pétale (cm)')
    axes_intro[2].legend()
    axes_intro[2].grid(alpha=0.3)
    
    plt.tight_layout()
    st.pyplot(fig_intro)

# ============================================================================
# EXERCICE 1 - ANALYSE QUALITATIVE
# ============================================================================

elif menu_option == "📊 Exercice 1 - Analyse qualitative":
    st.title("📊 Exercice 1 : Analyse de la variable qualitative 'Espèce'")
    
    st.markdown("""
    ### Objectif
    Analyser la variable qualitative **species** (espèce) qui comporte 3 modalités :
    - **setosa** 🌸
    - **versicolor** 🌺
    - **virginica** 💮
    """)
    
    # 1. Effectif des modalités
    st.subheader("1. Effectif des 3 modalités")
    
    species_counts = df['species'].value_counts().reset_index()
    species_counts.columns = ['Espèce', 'Effectif']
    species_counts['Pourcentage'] = (species_counts['Effectif'] / len(df) * 100).round(1)
    
    col_stats, col_table = st.columns([1, 2])
    
    with col_stats:
        st.markdown("**Statistiques :**")
        for idx, row in species_counts.iterrows():
            st.metric(
                label=row['Espèce'],
                value=f"{row['Effectif']} échantillons",
                delta=f"{row['Pourcentage']}%"
            )
    
    with col_table:
        st.dataframe(species_counts.style
                    .background_gradient(subset=['Effectif'], cmap='YlOrRd')
                    .format({'Pourcentage': '{:.1f}%'}),
                    use_container_width=True)
    
    st.markdown("---")
    
    # 2. Diagrammes des effectifs
    st.subheader("2. Diagrammes des effectifs")
    
    viz_option = st.radio(
        "Choisir le type de visualisation :",
        ["Histogramme", "Diagramme en secteurs", "Barres groupées", "Diagramme en cascade"],
        horizontal=True
    )
    
    if viz_option == "Histogramme":
        fig1, ax1 = plt.subplots(figsize=(10, 6))
        bars = ax1.bar(species_counts['Espèce'], species_counts['Effectif'],
                      color=[species_palette[s] for s in species_counts['Espèce']],
                      edgecolor='black', linewidth=2)
        
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                    f'{int(height)}\n({height/len(df)*100:.1f}%)',
                    ha='center', va='bottom', fontweight='bold')
        
        ax1.set_xlabel('Espèce', fontweight='bold')
        ax1.set_ylabel('Effectif', fontweight='bold')
        ax1.set_title('Distribution des espèces - Histogramme', fontweight='bold')
        ax1.grid(axis='y', alpha=0.3)
        
        st.pyplot(fig1)
        
    elif viz_option == "Diagramme en secteurs":
        fig2, ax2 = plt.subplots(figsize=(8, 8))
        
        colors_pie = [species_palette[s] for s in species_counts['Espèce']]
        explode = (0.05, 0.05, 0.05)
        
        wedges, texts, autotexts = ax2.pie(
            species_counts['Effectif'],
            labels=species_counts['Espèce'],
            colors=colors_pie,
            autopct='%1.1f%%',
            startangle=90,
            explode=explode,
            shadow=True,
            textprops={'fontsize': 11, 'fontweight': 'bold'}
        )
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        ax2.set_title('Répartition des espèces - Diagramme en secteurs', 
                     fontweight='bold', pad=20)
        
        st.pyplot(fig2)
        
    elif viz_option == "Barres groupées":
        # Données supplémentaires pour les barres groupées
        years = ['2022', '2023', '2024']
        data_grouped = pd.DataFrame({
            'setosa': [45, 48, 50],
            'versicolor': [48, 50, 50],
            'virginica': [47, 49, 50]
        }, index=years)
        
        fig3, ax3 = plt.subplots(figsize=(10, 6))
        
        x = np.arange(len(years))
        width = 0.25
        
        for i, species in enumerate(df['species'].unique()):
            offset = width * (i - 1)
            ax3.bar(x + offset, data_grouped[species], width,
                   label=species, color=species_palette[species],
                   edgecolor='black')
        
        ax3.set_xlabel('Année', fontweight='bold')
        ax3.set_ylabel('Nombre d\'échantillons', fontweight='bold')
        ax3.set_title('Évolution des effectifs par espèce (exemple)', fontweight='bold')
        ax3.set_xticks(x)
        ax3.set_xticklabels(years)
        ax3.legend()
        ax3.grid(axis='y', alpha=0.3)
        
        st.pyplot(fig3)
        
    else:  # Diagramme en cascade
        fig4 = go.Figure(go.Waterfall(
            name="Cumul des effectifs",
            orientation="v",
            measure=["relative", "relative", "relative", "total"],
            x=["setosa", "versicolor", "virginica", "Total"],
            y=species_counts['Effectif'].tolist() + [len(df)],
            text=[f"+{val}" for val in species_counts['Effectif'].tolist()] + [f"Total: {len(df)}"],
            textposition="outside",
            increasing={"marker": {"color": species_palette['setosa']}},
            decreasing={"marker": {"color": species_palette['versicolor']}},
            totals={"marker": {"color": species_palette['virginica']}}
        ))
        
        fig4.update_layout(
            title="Diagramme en cascade - Cumul des effectifs",
            showlegend=False,
            xaxis_title="Espèce",
            yaxis_title="Effectif cumulé"
        )
        
        st.plotly_chart(fig4, use_container_width=True)
    
    st.markdown("---")
    
    # 3. Meilleure coloration et étiquetage
    st.subheader("3. Recommandations pour la coloration et l'étiquetage")
    
    col_rec1, col_rec2 = st.columns(2)
    
    with col_rec1:
        st.markdown("""
        **🎨 Recommandations de coloration :**
        
        1. **Contraste suffisant** : Utiliser des couleurs bien distinctes
        2. **Accessibilité** : Palette adaptée aux daltoniens
        3. **Cohérence** : Mêmes couleurs pour chaque espèce
        4. **Harmonie** : Palette complémentaire
        
        **Palette recommandée :**
        - setosa : Rouge corail (#FF6B6B)
        - versicolor : Turquoise (#4ECDC4)
        - virginica : Jaune doré (#FFD166)
        """)
    
    with col_rec2:
        st.markdown("""
        **📝 Recommandations d'étiquetage :**
        
        1. **Lisibilité** : Police claire et taille adéquate
        2. **Précision** : Valeurs exactes + pourcentages
        3. **Position** : Étiquettes sans chevauchement
        4. **Concision** : Informations essentielles uniquement
        
        **Format recommandé :**
        ```
        Espèce: X échantillons (Y%)
        ```
        """)
    
    st.markdown("""
    **🎯 4 Recommandation finale : Histogramme avec étiquettes**
    
    **Pourquoi ?**
    a. **Précision** : Lecture exacte des effectifs
    b. **Comparaison** : Hauteur des barres facile à comparer
    c. **Universalité** : Graphique compris par tous
    d. **Flexibilité** : Peut inclure valeurs et pourcentages
    """)

# ============================================================================
# EXERCICE 2 - VARIABLES QUANTITATIVES
# ============================================================================

elif menu_option == "📏 Exercice 2 - Variables quantitatives":
    st.title("📏 Exercice 2 : Analyse des variables quantitatives")
    
    st.markdown("""
    ### Objectif
    Analyse les 4 variables quantitatives mesurées sur les fleurs Iris :
    1. **SepalLength** : Longueur du sépale (cm)
    2. **SepalWidth** : Largeur du sépale (cm)
    3. **PetalLength** : Longueur du pétale (cm)
    4. **PetalWidth** : Largeur du pétale (cm)
    """)
    
    # Sélection de la variable à analyser
    selected_var = st.selectbox(
        "Choisir une variable à analyser en détail :",
        quantitative_vars,
        format_func=lambda x: french_names[x]
    )
    
    st.markdown("---")
    
    # 1. Résumé statistique
    st.subheader(f"1. Résumé statistique de {french_names[selected_var]}")
    
    stats = df[selected_var].describe()
    stats_df = pd.DataFrame({
        'Statistique': ['Nombre', 'Moyenne', 'Écart-type', 'Minimum', 
                       '25% (Q1)', '50% (Médiane)', '75% (Q3)', 'Maximum'],
        'Valeur': [stats['count'], f"{stats['mean']:.2f} cm", 
                  f"{stats['std']:.2f} cm", f"{stats['min']:.2f} cm",
                  f"{stats['25%']:.2f} cm", f"{stats['50%']:.2f} cm",
                  f"{stats['75%']:.2f} cm", f"{stats['max']:.2f} cm"]
    })
    
    col_stats_summary, col_metrics = st.columns([2, 1])
    
    with col_stats_summary:
        st.dataframe(stats_df, use_container_width=True, hide_index=True)
    
    with col_metrics:
        st.metric("Étendue", f"{stats['max'] - stats['min']:.2f} cm")
        st.metric("Intervalle interquartile", f"{stats['75%'] - stats['25%']:.2f} cm")
        st.metric("Coefficient de variation", f"{(stats['std']/stats['mean']*100):.1f}%")
        st.metric("Asymétrie", f"{df[selected_var].skew():.2f}")
    
    st.markdown("---")
    
    # 2. Histogramme
    st.subheader(f"2. Histogramme de {french_names[selected_var]}")
    
    # Options d'affichage
    col_bins, col_overlay = st.columns(2)
    
    with col_bins:
        bins = st.slider("Nombre de classes (bins) :", 5, 30, 15)
    
    with col_overlay:
        show_kde = st.checkbox("Afficher la courbe de densité (KDE)", value=True)
        show_norm = st.checkbox("Afficher la distribution normale", value=False)
    
    # Création de l'histogramme
    fig_hist, ax_hist = plt.subplots(figsize=(10, 6))
    
    # Histogramme avec KDE
    if show_kde:
        sns.histplot(df[selected_var], bins=bins, kde=True, ax=ax_hist,
                    color=variable_palette[quantitative_vars.index(selected_var)],
                    alpha=0.7, edgecolor='black')
    else:
        ax_hist.hist(df[selected_var], bins=bins,
                    color=variable_palette[quantitative_vars.index(selected_var)],
                    alpha=0.7, edgecolor='black')
    
    # Lignes statistiques
    mean_val = df[selected_var].mean()
    median_val = df[selected_var].median()
    
    ax_hist.axvline(mean_val, color='red', linestyle='--', linewidth=2,
                   label=f'Moyenne: {mean_val:.2f} cm')
    ax_hist.axvline(median_val, color='green', linestyle=':', linewidth=2,
                   label=f'Médiane: {median_val:.2f} cm')
    
    # Distribution normale théorique (optionnelle)
    if show_norm:
        from scipy.stats import norm
        x = np.linspace(df[selected_var].min(), df[selected_var].max(), 100)
        y = norm.pdf(x, mean_val, df[selected_var].std()) * len(df) * (stats['max']-stats['min'])/bins
        ax_hist.plot(x, y, 'k-', alpha=0.5, label='Distribution normale')
    
    ax_hist.set_xlabel(french_names[selected_var] + ' (cm)', fontweight='bold')
    ax_hist.set_ylabel('Fréquence', fontweight='bold')
    ax_hist.set_title(f'Distribution de {french_names[selected_var].lower()}', fontweight='bold')
    ax_hist.legend()
    ax_hist.grid(alpha=0.3)
    
    st.pyplot(fig_hist)
    
    st.markdown("---")
    
    # 3. Analyse comparative des 4 variables
    st.subheader("3. Analyse comparative des 4 variables quantitatives")
    
    # Création de la vue comparative
    fig_compare, axes_compare = plt.subplots(2, 2, figsize=(14, 10))
    axes_compare = axes_compare.flatten()
    
    for idx, var in enumerate(quantitative_vars):
        ax = axes_compare[idx]
        
        # Histogramme avec KDE
        sns.histplot(df[var], kde=True, ax=ax, bins=15,
                    color=variable_palette[idx], alpha=0.7)
        
        # Lignes statistiques
        ax.axvline(df[var].mean(), color='red', linestyle='--', linewidth=1.5)
        ax.axvline(df[var].median(), color='green', linestyle=':', linewidth=1.5)
        
        ax.set_xlabel(french_names[var] + ' (cm)', fontweight='bold')
        ax.set_ylabel('Fréquence', fontweight='bold')
        ax.set_title(french_names[var], fontweight='bold')
        ax.grid(alpha=0.3)
        
        # Ajouter la moyenne et médiane dans le coin
        ax.text(0.02, 0.95, f'μ={df[var].mean():.2f}\nM={df[var].median():.2f}',
               transform=ax.transAxes, fontsize=9,
               bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    plt.suptitle('Distribution des 4 variables quantitatives', fontweight='bold', fontsize=16, y=1.02)
    plt.tight_layout()
    st.pyplot(fig_compare)
    
    # Tableau récapitulatif
    st.subheader("4. Synthèse des statistiques descriptives")
    
    summary_stats = pd.DataFrame()
    for var in quantitative_vars:
        summary_stats[french_names[var]] = [
            f"{df[var].mean():.2f}",
            f"{df[var].std():.2f}",
            f"{df[var].min():.2f}",
            f"{df[var].max():.2f}",
            f"{df[var].max() - df[var].min():.2f}",
            f"{(df[var].std()/df[var].mean()*100):.1f}%",
            f"{df[var].skew():.2f}"
        ]
    
    summary_stats.index = ['Moyenne (cm)', 'Écart-type (cm)', 'Min (cm)', 'Max (cm)',
                          'Étendue (cm)', 'CV (%)', 'Asymétrie']
    
    st.dataframe(summary_stats.style
                .background_gradient(cmap='YlOrRd', axis=1),
                use_container_width=True)
    
    st.markdown("---")
    
    # 5. Interprétation
    st.subheader("5. Interprétation des résultats")
    
    st.markdown(f"""
    **📊 Analyse de {french_names[selected_var]} :**
    
    1. **Distribution** : {'Distribution multimodale (suggère des sous-groupes correspondant aux espèces)' 
                         if selected_var in ['PetalLength', 'PetalWidth'] else 'Distribution plutôt normale'}
    2. **Variabilité** : CV = {(df[selected_var].std()/df[selected_var].mean()*100):.1f}% 
       ({'Forte variabilité' if (df[selected_var].std()/df[selected_var].mean()*100) > 20 else 'Variabilité modérée'})
    3. **Asymétrie** : {df[selected_var].skew():.2f} 
       ({'Asymétrie positive' if df[selected_var].skew() > 0 else 'Asymétrie négative' if df[selected_var].skew() < 0 else 'Distribution symétrique'})
    4. **Valeurs extrêmes** : Aucune valeur aberrante évidente
    
    **🔍 Observations générales :**
    - **PetalLength** et **PetalWidth** montrent une séparation claire des espèces
    - **SepalLength** et **SepalWidth** ont des distributions plus superposées
    - Les variables des pétales sont plus discriminantes que celles des sépales
    """)
# ============================================================================
# EXERCICE 3 - ANALYSE BIVARIÉE (CORRIGÉ)
# ============================================================================

elif menu_option == "🔗 Exercice 3 - Analyse bivariée":
    st.title("🔗 Exercice 3 : Analyse bivariée des variables")
    
    st.markdown("""
    ### Objectif
    Étudier les relations entre deux variables quantitatives à l'aide de nuages de points.
    """)
    
    # Sélection des variables - CORRECTION ICI
    col_var1, col_var2 = st.columns(2)
    
    with col_var1:
        var_x = st.selectbox(
            "Variable X (axe horizontal) :",
            quantitative_vars,
            index=2,  # PetalLength par défaut
            format_func=lambda x: french_names[x],
            key="var_x_select"
        )
    
    with col_var2:
        # Créer la liste des options pour Y (exclure X)
        y_options = [v for v in quantitative_vars if v != var_x]
        
        # Déterminer l'index par défaut intelligemment
        default_index = 0
        # Si X est PetalLength, alors Y par défaut = PetalWidth
        if var_x == 'PetalLength' and 'PetalWidth' in y_options:
            default_index = y_options.index('PetalWidth')
        # Si X est PetalWidth, alors Y par défaut = PetalLength
        elif var_x == 'PetalWidth' and 'PetalLength' in y_options:
            default_index = y_options.index('PetalLength')
        # Si X est SepalLength, alors Y par défaut = SepalWidth
        elif var_x == 'SepalLength' and 'SepalWidth' in y_options:
            default_index = y_options.index('SepalWidth')
        # Si X est SepalWidth, alors Y par défaut = SepalLength
        elif var_x == 'SepalWidth' and 'SepalLength' in y_options:
            default_index = y_options.index('SepalLength')
        
        var_y = st.selectbox(
            "Variable Y (axe vertical) :",
            y_options,
            index=default_index,
            format_func=lambda x: french_names[x],
            key="var_y_select"
        )
    
    st.markdown("---")
    
    # 1. Nuage de points
    st.subheader(f"1. Nuage de points : {french_names[var_x]} vs {french_names[var_y]}")
    
    # Options de visualisation
    col_options1, col_options2 = st.columns(2)
    
    with col_options1:
        color_by_species = st.checkbox("Colorer par espèce", value=True)
        show_regression = st.checkbox("Afficher la droite de régression", value=True)
    
    with col_options2:
        point_size = st.slider("Taille des points :", 10, 100, 50)
        alpha_value = st.slider("Transparence :", 0.1, 1.0, 0.7)
    
    # Création du scatter plot
    if use_plotly and color_by_species:
        # Version interactive avec Plotly
        try:
            fig_scatter = px.scatter(df, x=var_x, y=var_y, color='species',
                                   color_discrete_map=species_palette,
                                   title=f'Relation {french_names[var_x]} - {french_names[var_y]}',
                                   labels={var_x: french_names[var_x] + ' (cm)',
                                          var_y: french_names[var_y] + ' (cm)'},
                                   hover_data=['species'],
                                   opacity=alpha_value)
            
            if show_regression:
                # Ajouter la ligne de régression
                m, b = linear_regression(df[var_x].values, df[var_y].values)
                x_range = [df[var_x].min(), df[var_x].max()]
                y_range = [m * x + b for x in x_range]
                
                fig_scatter.add_trace(
                    go.Scatter(x=x_range, y=y_range, mode='lines',
                              name=f'Régression: y = {m:.2f}x + {b:.2f}',
                              line=dict(color='red', width=2))
                )
            
            fig_scatter.update_layout(
                hovermode='closest',
                showlegend=True,
                legend_title_text='Espèce'
            )
            
            st.plotly_chart(fig_scatter, use_container_width=True)
        except:
            # Fallback to matplotlib if plotly fails
            color_by_species = True
            use_plotly = False
    
    if not use_plotly or not color_by_species:
        # Version Matplotlib
        fig_scatter, ax_scatter = plt.subplots(figsize=(10, 7))
        
        if color_by_species:
            for species in df['species'].unique():
                subset = df[df['species'] == species]
                ax_scatter.scatter(subset[var_x], subset[var_y],
                                 color=species_palette[species],
                                 label=species, s=point_size, alpha=alpha_value,
                                 edgecolor='black', linewidth=0.5)
        else:
            ax_scatter.scatter(df[var_x], df[var_y],
                             color='#6A5ACD', s=point_size, alpha=alpha_value)
        
        if show_regression:
            m, b = linear_regression(df[var_x].values, df[var_y].values)
            x_range = np.array([df[var_x].min(), df[var_x].max()])
            ax_scatter.plot(x_range, m * x_range + b,
                          'r-', linewidth=2,
                          label=f'Régression: y = {m:.2f}x + {b:.2f}')
        
        ax_scatter.set_xlabel(french_names[var_x] + ' (cm)', fontweight='bold')
        ax_scatter.set_ylabel(french_names[var_y] + ' (cm)', fontweight='bold')
        ax_scatter.set_title(f'Relation {french_names[var_x]} - {french_names[var_y]}',
                           fontweight='bold')
        if color_by_species or show_regression:
            ax_scatter.legend()
        ax_scatter.grid(alpha=0.3)
        
        st.pyplot(fig_scatter)
    
    st.markdown("---")
    
    # 2. Analyse statistique de la relation
    st.subheader("2. Analyse statistique de la relation")
    
    # Calcul des métriques
    correlation = df[var_x].corr(df[var_y])
    covariance = df[var_x].cov(df[var_y])
    
    # Régression linéaire
    m, b = linear_regression(df[var_x].values, df[var_y].values)
    
    # Calcul R²
    y_pred = m * df[var_x].values + b
    ss_res = np.sum((df[var_y].values - y_pred) ** 2)
    ss_tot = np.sum((df[var_y].values - np.mean(df[var_y].values)) ** 2)
    r_squared = 1 - (ss_res / ss_tot)
    
    # Affichage des métriques
    col_corr, col_reg, col_r2 = st.columns(3)
    
    with col_corr:
        st.metric("Corrélation (r)", f"{correlation:.4f}")
        st.write("Force de la relation :")
        if abs(correlation) > 0.7:
            st.success("Très forte")
        elif abs(correlation) > 0.4:
            st.info("Modérée")
        else:
            st.warning("Faible")
    
    with col_reg:
        st.metric("Équation de régression", f"y = {m:.3f}x + {b:.3f}")
        st.metric("Covariance", f"{covariance:.4f}")
    
    with col_r2:
        st.metric("Coefficient de détermination (R²)", f"{r_squared:.4f}")
        st.write(f"Explique {r_squared*100:.1f}% de la variance")
    
    st.markdown("---")
    
    # 3. Analyse spécifique PetalLength vs PetalWidth
    if var_x == 'PetalLength' and var_y == 'PetalWidth':
        st.subheader("3. Analyse spécifique : Longueur vs Largeur du pétale")
        
        st.markdown(f"""
        **📊 Observations :**
        
        1. **Relation très forte** (r = {correlation:.3f}) :
           - Quand la longueur du pétale augmente, sa largeur augmente proportionnellement
           - Relation quasi linéaire parfaite
        
        2. **Regroupement par espèces :**
           - **Setosa** : Petits pétales (1.0-2.0 cm de long, 0.1-0.6 cm de large)
           - **Versicolor** : Pétales moyens (3.0-5.5 cm de long, 1.0-1.8 cm de large)
           - **Virginica** : Grands pétales (4.5-7.0 cm de long, 1.2-2.5 cm de large)
        
        3. **Signification biologique :**
           - Contrôle génétique strict de la forme des pétales
           - Croissance proportionnelle conservée quelle que soit la taille
           - Excellente variable discriminante pour la classification
        """)
    
    st.markdown("---")
    
    # 4. Matrice de corrélation
    st.subheader("4. Matrice de corrélation complète")
    
    # Calcul de la matrice de corrélation
    corr_matrix = df[quantitative_vars].corr()
    
    fig_corr, ax_corr = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm',
                center=0, square=True, ax=ax_corr,
                cbar_kws={'label': 'Coefficient de corrélation'})
    
    ax_corr.set_title('Matrice de corrélation des variables quantitatives', fontweight='bold')
    
    st.pyplot(fig_corr)
    
    st.markdown("""
    **🔍 Interprétation de la matrice de corrélation :**
    
    1. **Forte corrélation positive** (> 0.8) :
       - PetalLength ↔ PetalWidth (0.96) : croissance proportionnelle
    
    2. **Corrélations modérées** (0.4-0.8) :
       - PetalLength ↔ SepalLength (0.87)
       - PetalWidth ↔ SepalLength (0.82)
    
    3. **Faible corrélation** (< 0.4) :
       - SepalWidth ↔ autres variables (corrélations faibles ou négatives)
    """)

# ============================================================================
# EXERCICE 4 - BOXPLOTS (CORRIGÉ)
# ============================================================================

elif menu_option == "📦 Exercice 4 - Boxplots":
    st.title("📦 Exercice 4 : Boxplots (Variable qualitative vs quantitative)")
    
    st.markdown("""
    ### Objectif
    Utiliser les boîtes à moustaches pour analyser la relation entre :
    - Variable qualitative : **Espèce** (3 modalités)
    - Variable quantitative : Mesures morphologiques
    """)
    
    # Sélection de la variable quantitative
    selected_var_box = st.selectbox(
        "Choisir la variable quantitative à analyser :",
        quantitative_vars,
        format_func=lambda x: french_names[x]
    )
    
    st.markdown("---")
    
    # 1. Boxplot standard
    st.subheader(f"1. Boxplot : {french_names[selected_var_box]} par espèce")
    
    fig_box, ax_box = plt.subplots(figsize=(10, 6))
    
    # Création du boxplot avec seaborn
    sns.boxplot(x='species', y=selected_var_box, data=df,
               palette=species_palette, ax=ax_box,
               showmeans=True, meanprops={"marker":"o",
                                        "markerfacecolor":"white",
                                        "markeredgecolor":"black",
                                        "markersize":"8"})
    
    # Ajouter les points individuels
    sns.stripplot(x='species', y=selected_var_box, data=df,
                 color='black', alpha=0.5, size=4, jitter=True, ax=ax_box)
    
    ax_box.set_xlabel('Espèce', fontweight='bold')
    ax_box.set_ylabel(french_names[selected_var_box] + ' (cm)', fontweight='bold')
    ax_box.set_title(f'Distribution de {french_names[selected_var_box].lower()} par espèce',
                    fontweight='bold')
    ax_box.grid(axis='y', alpha=0.3)
    
    st.pyplot(fig_box)
    
    st.markdown("---")
    
    # 2. Statistiques par espèce - CORRECTION ICI
    st.subheader("2. Statistiques détaillées par espèce")
    
    # Calcul des statistiques avec des fonctions nommées correctement
    stats_by_species = df.groupby('species')[selected_var_box].agg([
        'count', 'mean', 'std', 'min', 
        ('q1', lambda x: x.quantile(0.25)),  # Quartile 1
        ('median', 'median'),                # Médiane
        ('q3', lambda x: x.quantile(0.75)),  # Quartile 3
        'max'
    ]).round(2)
    
    # Renommer les colonnes pour plus de clarté
    stats_by_species.columns = ['N', 'Moyenne', 'Écart-type', 'Min', 'Q1', 'Médiane', 'Q3', 'Max']
    
    # Afficher les statistiques
    col_stats_table, col_stats_viz = st.columns([2, 1])
    
    with col_stats_table:
        st.dataframe(stats_by_species.style
                    .background_gradient(subset=['Moyenne', 'Écart-type'], cmap='YlOrRd'),
                    use_container_width=True)
    
    with col_stats_viz:
        # Visualisation des moyennes
        fig_means, ax_means = plt.subplots(figsize=(6, 4))
        
        species_order = df['species'].unique()
        means = [stats_by_species.loc[s, 'Moyenne'] for s in species_order]
        
        bars = ax_means.bar(species_order, means,
                           color=[species_palette[s] for s in species_order])
        
        # Ajouter les valeurs
        for bar, mean in zip(bars, means):
            ax_means.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
                         f'{mean:.2f}', ha='center', va='bottom', fontweight='bold')
        
        ax_means.set_xlabel('Espèce')
        ax_means.set_ylabel('Moyenne (cm)')
        ax_means.set_title('Moyennes par espèce', fontweight='bold')
        ax_means.grid(axis='y', alpha=0.3)
        
        st.pyplot(fig_means)
    
    st.markdown("---")
    
    # 3. Comparaison avec violin plot
    st.subheader("3. Comparaison : Boxplot vs Violin plot")
    
    fig_compare, (ax_box2, ax_violin) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Boxplot
    sns.boxplot(x='species', y=selected_var_box, data=df,
               palette=species_palette, ax=ax_box2)
    ax_box2.set_xlabel('Espèce')
    ax_box2.set_ylabel(french_names[selected_var_box] + ' (cm)')
    ax_box2.set_title('Boxplot', fontweight='bold')
    ax_box2.grid(axis='y', alpha=0.3)
    
    # Violin plot
    sns.violinplot(x='species', y=selected_var_box, data=df,
                  palette=species_palette, inner='quartile', ax=ax_violin)
    ax_violin.set_xlabel('Espèce')
    ax_violin.set_ylabel(french_names[selected_var_box] + ' (cm)')
    ax_violin.set_title('Violin plot', fontweight='bold')
    ax_violin.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    st.pyplot(fig_compare)
    
    st.markdown("""
    **📊 Comparaison Boxplot vs Violin plot :**
    
    | Aspect | Boxplot | Violin plot |
    |--------|---------|-------------|
    | **Forme** | Résumé statistique (quartiles) | Distribution complète (densité) |
    | **Densité** | Non visible | Visible grâce à la largeur |
    | **Multimodalité** | Non détectée | Détectable visuellement |
    | **Simplicité** | Plus simple | Plus complexe |
    | **Usage** | Comparaison de groupes | Analyse détaillée des distributions |
    """)
    
    st.markdown("---")
    
    # 4. Analyse de PetalLength (exemple demandé)
    if selected_var_box == 'PetalLength':
        st.subheader("4. Analyse spécifique : Longueur des pétales par espèce")
        
        # Calcul des intervalles interquartiles
        iqr_setosa = stats_by_species.loc['setosa', 'Q3'] - stats_by_species.loc['setosa', 'Q1']
        iqr_versicolor = stats_by_species.loc['versicolor', 'Q3'] - stats_by_species.loc['versicolor', 'Q1']
        iqr_virginica = stats_by_species.loc['virginica', 'Q3'] - stats_by_species.loc['virginica', 'Q1']
        
        st.markdown(f"""
        **🔍 Observations détaillées :**
        
        1. **Séparation parfaite** :
           - Les 3 boxplots sont complètement séparés
           - Pas de chevauchement des boîtes à moustaches
        
        2. **Setosa** :
           - Valeurs très basses ({stats_by_species.loc['setosa', 'Min']:.1f}-{stats_by_species.loc['setosa', 'Max']:.1f} cm)
           - Faible dispersion (IQR étroit : {iqr_setosa:.1f} cm)
           - Distribution symétrique
        
        3. **Versicolor** :
           - Valeurs intermédiaires ({stats_by_species.loc['versicolor', 'Min']:.1f}-{stats_by_species.loc['versicolor', 'Max']:.1f} cm)
           - Bonne séparation de virginica
           - Quelques valeurs proches du seuil inférieur
        
        4. **Virginica** :
           - Valeurs élevées ({stats_by_species.loc['virginica', 'Min']:.1f}-{stats_by_species.loc['virginica', 'Max']:.1f} cm)
           - Plus grande dispersion (IQR large : {iqr_virginica:.1f} cm)
           - Distribution légèrement asymétrique vers la droite
        
        **🎯 Conclusion :**
        PetalLength est une variable **excellente** pour discriminer les espèces d'iris.
        La séparation est si nette qu'un simple seuil sur cette variable suffirait presque
        pour la classification.
        """)
    
    # 5. Tous les boxplots côte à côte
    st.subheader("5. Vue d'ensemble : Toutes les variables par espèce")
    
    fig_all_box, axes_all = plt.subplots(2, 2, figsize=(14, 10))
    axes_all = axes_all.flatten()
    
    for idx, var in enumerate(quantitative_vars):
        ax = axes_all[idx]
        sns.boxplot(x='species', y=var, data=df, palette=species_palette, ax=ax)
        ax.set_xlabel('Espèce')
        ax.set_ylabel(french_names[var] + ' (cm)')
        ax.set_title(french_names[var], fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
    
    plt.suptitle('Distribution de toutes les variables par espèce', fontweight='bold', fontsize=16, y=1.02)
    plt.tight_layout()
    st.pyplot(fig_all_box)

# ============================================================================
# EXERCICE 5 - VISUALISATIONS AVANCÉES
# ============================================================================

elif menu_option == "🎨 Exercice 5 - Visualisations avancées":
    st.title("🎨 Exercice 5 : Visualisations avancées par espèce")
    
    st.markdown("""
    ### Objectif
    Développer des visualisations avancées pour mettre en évidence :
    1. Les différences entre espèces
    2. Les relations entre variables au sein de chaque espèce
    3. Les profils caractéristiques de chaque espèce
    """)
    
    # Sélection du type de visualisation
    viz_type = st.selectbox(
        "Choisir le type de visualisation :",
        [
            "Pair plot par espèce",
            "Radar chart (profil moyen)",
            "Matrices de corrélation par espèce",
            "Facet grid (scatter plots par espèce)",
            "3D Scatter plot"
        ]
    )
    
    st.markdown("---")
    
    if viz_type == "Pair plot par espèce":
        st.subheader("1. Pair plot avec coloration par espèce")
        
        try:
            pair_fig = sns.pairplot(df, hue='species', vars=quantitative_vars,
                                   palette=species_palette, diag_kind='kde',
                                   plot_kws={'alpha': 0.7, 's': 30}, height=2.5)
            
            pair_fig.fig.suptitle('Pair plot des variables quantitatives par espèce',
                                 fontweight='bold', fontsize=14, y=1.02)
            
            st.pyplot(pair_fig)
            
        except Exception as e:
            st.error(f"Erreur lors de la création du pair plot : {e}")
            
            # Alternative
            st.info("Création d'une alternative...")
            
            fig_alt, axes_alt = plt.subplots(4, 4, figsize=(14, 12))
            
            for i in range(4):
                for j in range(4):
                    ax = axes_alt[i, j]
                    
                    if i == j:
                        # KDE sur la diagonale
                        for species in df['species'].unique():
                            subset = df[df['species'] == species]
                            sns.kdeplot(data=subset[quantitative_vars[i]], ax=ax,
                                       label=species, color=species_palette[species])
                        ax.set_title(quantitative_vars[i])
                    else:
                        # Scatter plot
                        for species in df['species'].unique():
                            subset = df[df['species'] == species]
                            ax.scatter(subset[quantitative_vars[j]], subset[quantitative_vars[i]],
                                      color=species_palette[species], alpha=0.5, s=20,
                                      label=species if i==0 and j==3 else "")
                    
                    if i == 3:
                        ax.set_xlabel(quantitative_vars[j])
                    if j == 0:
                        ax.set_ylabel(quantitative_vars[i])
            
            plt.suptitle('Relations entre variables par espèce', fontweight='bold', fontsize=14, y=1.02)
            plt.tight_layout()
            st.pyplot(fig_alt)
    
    elif viz_type == "Radar chart (profil moyen)":
        st.subheader("2. Radar chart des caractéristiques moyennes")
        
        # Calcul des moyennes par espèce
        radar_data = df.groupby('species')[quantitative_vars].mean().reset_index()
        
        # Normalisation des données pour le radar chart
        radar_normalized = radar_data.copy()
        for var in quantitative_vars:
            min_val = df[var].min()
            max_val = df[var].max()
            radar_normalized[var] = (radar_data[var] - min_val) / (max_val - min_val) * 100
        
        if use_plotly:
            # Version Plotly
            fig_radar = go.Figure()
            
            for species in radar_normalized['species']:
                values = radar_normalized[radar_normalized['species'] == species][quantitative_vars].values.flatten().tolist()
                values += values[:1]  # Fermer le cercle
                
                fig_radar.add_trace(go.Scatterpolar(
                    r=values,
                    theta=[french_names[var] for var in quantitative_vars] + [french_names[quantitative_vars[0]]],
                    name=species,
                    fill='toself',
                    line_color=species_palette[species]
                ))
            
            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 100]
                    )),
                showlegend=True,
                title='Profil moyen des espèces d\'Iris (normalisé)',
                title_font_size=16
            )
            
            st.plotly_chart(fig_radar, use_container_width=True)
            
        else:
            # Version Matplotlib
            fig_radar, ax_radar = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))
            
            categories = [french_names[var] for var in quantitative_vars]
            N = len(categories)
            angles = [n / float(N) * 2 * np.pi for n in range(N)]
            angles += angles[:1]
            
            for species in radar_normalized['species']:
                values = radar_normalized[radar_normalized['species'] == species][quantitative_vars].values.flatten().tolist()
                values += values[:1]
                
                ax_radar.plot(angles, values, linewidth=2, linestyle='solid',
                            label=species, color=species_palette[species])
                ax_radar.fill(angles, values, color=species_palette[species], alpha=0.25)
            
            ax_radar.set_xticks(angles[:-1])
            ax_radar.set_xticklabels(categories)
            ax_radar.set_title('Profil moyen des espèces', fontweight='bold', pad=20)
            ax_radar.legend(loc='upper right')
            
            st.pyplot(fig_radar)
    
    elif viz_type == "Matrices de corrélation par espèce":
        st.subheader("3. Matrices de corrélation par espèce")
        
        # Calcul des corrélations par espèce
        fig_corr_species, axes_corr = plt.subplots(1, 3, figsize=(15, 4))
        
        for idx, species in enumerate(df['species'].unique()):
            subset = df[df['species'] == species]
            corr_matrix = subset[quantitative_vars].corr()
            
            im = axes_corr[idx].imshow(corr_matrix, cmap='coolwarm', vmin=-1, vmax=1)
            axes_corr[idx].set_title(f'{species}', fontweight='bold')
            axes_corr[idx].set_xticks(range(len(quantitative_vars)))
            axes_corr[idx].set_yticks(range(len(quantitative_vars)))
            axes_corr[idx].set_xticklabels(['SL', 'SW', 'PL', 'PW'], rotation=45)
            axes_corr[idx].set_yticklabels(['SL', 'SW', 'PL', 'PW'], rotation=0)
            
            # Ajouter les valeurs
            for i in range(len(quantitative_vars)):
                for j in range(len(quantitative_vars)):
                    axes_corr[idx].text(j, i, f'{corr_matrix.iloc[i, j]:.2f}',
                                      ha='center', va='center',
                                      color='white' if abs(corr_matrix.iloc[i, j]) > 0.5 else 'black',
                                      fontsize=9, fontweight='bold')
        
        plt.colorbar(im, ax=axes_corr, orientation='horizontal', fraction=0.05, pad=0.1)
        plt.suptitle('Matrices de corrélation par espèce', fontweight='bold', fontsize=14, y=1.05)
        st.pyplot(fig_corr_species)
        
        # Analyse comparative
        st.subheader("Analyse comparative des corrélations")
        
        corr_comparison = pd.DataFrame()
        
        for species in df['species'].unique():
            subset = df[df['species'] == species]
            corr_matrix = subset[quantitative_vars].corr()
            
            corr_comparison[f'{species}_PL_PW'] = [corr_matrix.loc['PetalLength', 'PetalWidth']]
            corr_comparison[f'{species}_SL_SW'] = [corr_matrix.loc['SepalLength', 'SepalWidth']]
            corr_comparison[f'{species}_SL_PL'] = [corr_matrix.loc['SepalLength', 'PetalLength']]
        
        corr_comparison.index = ['Corrélation']
        st.dataframe(corr_comparison.T.round(3).style
                    .background_gradient(cmap='coolwarm', vmin=-1, vmax=1),
                    use_container_width=True)
        
        st.markdown("""
        **🔍 Observations :**
        
        1. **PetalLength-PetalWidth** :
           - Virginica : Corrélation très forte (≈0.32) → croissance proportionnelle
           - Versicolor : Corrélation modérée (≈0.79)
           - Setosa : Corrélation plus faible (≈0.31) → relation moins linéaire
        
        2. **SepalLength-SepalWidth** :
           - Toutes espèces : Corrélations faibles à négatives
           - Compromis longueur/largeur variable selon l'espèce
        
        3. **SepalLength-PetalLength** :
           - Virginica : Corrélation forte → coordination de croissance
           - Setosa : Corrélation faible → croissance indépendante
        """)
    
    elif viz_type == "Facet grid (scatter plots par espèce)":
        st.subheader("4. Facet grid : Scatter plots par espèce")
        
        # Sélection des variables
        col_facet1, col_facet2 = st.columns(2)
        
        with col_facet1:
            facet_x = st.selectbox("Variable X :", quantitative_vars,
                                 index=2, format_func=lambda x: french_names[x])
        
        with col_facet2:
            facet_y = st.selectbox("Variable Y :", quantitative_vars,
                                 index=3, format_func=lambda x: french_names[x])
        
        # Création du facet grid
        fig_facet, axes_facet = plt.subplots(1, 3, figsize=(15, 5), sharey=True, sharex=True)
        
        for idx, species in enumerate(df['species'].unique()):
            subset = df[df['species'] == species]
            ax = axes_facet[idx]
            
            ax.scatter(subset[facet_x], subset[facet_y],
                      color=species_palette[species], alpha=0.7, s=50)
            
            # Régression linéaire par espèce
            if len(subset) > 1:
                m_temp, b_temp = linear_regression(subset[facet_x].values, subset[facet_y].values)
                x_range = np.array([subset[facet_x].min(), subset[facet_x].max()])
                ax.plot(x_range, m_temp * x_range + b_temp,
                       'k--', linewidth=2, alpha=0.7,
                       label=f'y = {m_temp:.2f}x + {b_temp:.2f}')
            
            ax.set_xlabel(french_names[facet_x] + ' (cm)', fontweight='bold')
            if idx == 0:
                ax.set_ylabel(french_names[facet_y] + ' (cm)', fontweight='bold')
            ax.set_title(species, fontweight='bold', fontsize=12)
            ax.legend()
            ax.grid(alpha=0.3)
        
        plt.suptitle(f'Relation {french_names[facet_x]} - {french_names[facet_y]} par espèce',
                    fontweight='bold', fontsize=14, y=1.05)
        plt.tight_layout()
        st.pyplot(fig_facet)
    
    else:  # 3D Scatter plot
        st.subheader("5. Visualisation 3D")
        
        try:
            fig_3d = px.scatter_3d(df, x='PetalLength', y='PetalWidth', z='SepalLength',
                                  color='species', color_discrete_map=species_palette,
                                  title='Visualisation 3D des espèces d\'Iris',
                                  labels={'PetalLength': 'Longueur Pétale (cm)',
                                         'PetalWidth': 'Largeur Pétale (cm)',
                                         'SepalLength': 'Longueur Sépale (cm)'},
                                  opacity=0.7, size_max=10)
            
            fig_3d.update_layout(
                scene=dict(
                    xaxis_title='Longueur Pétale (cm)',
                    yaxis_title='Largeur Pétale (cm)',
                    zaxis_title='Longueur Sépale (cm)'
                ),
                legend_title_text='Espèce'
            )
            
            st.plotly_chart(fig_3d, use_container_width=True)
            
        except Exception as e:
            st.error(f"Erreur avec Plotly 3D : {e}")
            st.info("Alternative 2D avec taille variable :")
            
            fig_2d_alt, ax_2d_alt = plt.subplots(figsize=(10, 7))
            
            scatter = ax_2d_alt.scatter(df['PetalLength'], df['PetalWidth'],
                                       c=df['species'].map(lambda x: list(species_palette.keys()).index(x)),
                                       cmap='viridis', alpha=0.7,
                                       s=df['SepalLength'] * 20,
                                       edgecolor='k', linewidth=0.5)
            
            ax_2d_alt.set_xlabel('Longueur du pétale (cm)', fontweight='bold')
            ax_2d_alt.set_ylabel('Largeur du pétale (cm)', fontweight='bold')
            ax_2d_alt.set_title('Scatter plot avec taille proportionnelle à la longueur du sépale',
                              fontweight='bold')
            ax_2d_alt.grid(alpha=0.3)
            
            # Légende pour les espèces
            from matplotlib.lines import Line2D
            legend_elements = []
            for idx, species in enumerate(df['species'].unique()):
                legend_elements.append(Line2D([0], [0], marker='o', color='w',
                                            markerfacecolor=plt.cm.viridis(idx/3),
                                            markersize=10, label=species))
            
            ax_2d_alt.legend(handles=legend_elements, title='Espèce',
                           loc='upper left', bbox_to_anchor=(1, 1))
            
            plt.tight_layout()
            st.pyplot(fig_2d_alt)
    
    st.markdown("---")
    
    # Synthèse
    st.subheader("🎯 Synthèse des visualisations")
    
    st.markdown("""
    ### Recommandations pour la visualisation :
    
    | Objectif | Visualisation recommandée | Avantages |
    |----------|--------------------------|-----------|
    | **Comparaison espèces** | Boxplots ou Violin plots | Comparaison directe des distributions |
    | **Relations entre variables** | Scatter plots colorés par espèce | Visualisation des clusters |
    | **Profil complet** | Radar chart | Vue synthétique des caractéristiques |
    | **Vue d'ensemble** | Pair plot | Toutes les relations en un coup d'œil |
    | **Analyse détaillée** | Facet grid | Relations spécifiques par espèce |
    | **Visualisation avancée** | 3D scatter plot | Perspective spatiale des données |
    
    **🎨 Conseil :** Combiner plusieurs visualisations pour une analyse complète.
    """)

# ============================================================================
# MODÉLISATION KNN
# ============================================================================

elif menu_option == "🤖 Modélisation KNN":
    st.title("🤖 Modélisation avec K-Nearest Neighbors")
    
    st.warning("⚠️ Cette partie nécessite scikit-learn. Installation : `pip install scikit-learn`")
    
    try:
        from sklearn.model_selection import train_test_split
        from sklearn.preprocessing import StandardScaler, LabelEncoder
        from sklearn.neighbors import KNeighborsClassifier
        from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
        
        st.markdown("""
        ### Objectif
        Construire et évaluer un modèle KNN pour classifier les espèces d'iris.
        """)
        
        # 1. Préparation des données
        st.subheader("1. Préparation des données")
        
        # Encodage de la variable cible
        le = LabelEncoder()
        df_model = df.copy()
        df_model['species_encoded'] = le.fit_transform(df_model['species'])
        
        # Séparation X/y
        X = df_model[quantitative_vars]
        y = df_model['species_encoded']
        
        col_x, col_y = st.columns(2)
        
        with col_x:
            st.markdown("**Caractéristiques (X)**")
            st.dataframe(X.head(), use_container_width=True)
            st.write(f"Shape : {X.shape}")
        
        with col_y:
            st.markdown("**Cible (y)**")
            st.dataframe(pd.DataFrame({
                'Espèce': le.inverse_transform(y),
                'Code': y
            }).head(), use_container_width=True)
            st.write("Encodage :")
            for i, species in enumerate(le.classes_):
                st.write(f"- {i} = {species}")
        
        st.markdown("---")
        
        # 2. Division train/test
        st.subheader("2. Division des données")
        
        col_split1, col_split2 = st.columns(2)
        
        with col_split1:
            test_size = st.slider("Taille de l'ensemble de test :",
                                0.1, 0.4, 0.2, 0.05,
                                help="Proportion des données réservées pour le test")
        
        with col_split2:
            random_state = st.number_input("Random state :",
                                         0, 100, 42,
                                         help="Pour la reproductibilité")
        
        # Division avec stratification
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state,
            stratify=y
        )
        
        st.success(f"""
        ✅ Division effectuée :
        - **Train** : {X_train.shape[0]} échantillons ({X_train.shape[0]/len(X)*100:.0f}%)
        - **Test** : {X_test.shape[0]} échantillons ({X_test.shape[0]/len(X)*100:.0f}%)
        """)
        
        # Distribution par espèce
        train_dist = pd.Series(le.inverse_transform(y_train)).value_counts()
        test_dist = pd.Series(le.inverse_transform(y_test)).value_counts()
        
        col_train_dist, col_test_dist = st.columns(2)
        
        with col_train_dist:
            st.markdown("**Distribution train :**")
            for species in le.classes_:
                count = train_dist.get(species, 0)
                st.write(f"- {species} : {count} ({count/len(y_train)*100:.1f}%)")
        
        with col_test_dist:
            st.markdown("**Distribution test :**")
            for species in le.classes_:
                count = test_dist.get(species, 0)
                st.write(f"- {species} : {count} ({count/len(y_test)*100:.1f}%)")
        
        st.markdown("---")
        
        # 3. Normalisation
        st.subheader("3. Normalisation des caractéristiques")
        
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Visualisation avant/après
        fig_norm, axes_norm = plt.subplots(2, 2, figsize=(12, 8))
        
        for idx, var in enumerate(quantitative_vars):
            ax = axes_norm[idx // 2, idx % 2]
            
            # Avant normalisation
            ax.hist(X_train[var], bins=15, alpha=0.5, label='Avant', color='blue')
            
            # Après normalisation
            ax.hist(X_train_scaled[:, idx], bins=15, alpha=0.5, label='Après', color='red')
            
            ax.set_xlabel(french_names[var])
            ax.set_ylabel('Fréquence')
            ax.set_title(french_names[var])
            ax.legend()
            ax.grid(alpha=0.3)
        
        plt.suptitle('Comparaison avant/après normalisation', fontweight='bold', y=1.02)
        plt.tight_layout()
        st.pyplot(fig_norm)
        
        st.markdown("""
        **💡 Pourquoi normaliser ?**
        - KNN utilise les distances entre points
        - Les variables à grande échelle domineraient les autres
        - StandardScaler : soustrait la moyenne, divise par l'écart-type
        """)
        
        st.markdown("---")
        
        # 4. Entraînement du modèle
        st.subheader("4. Entraînement du modèle KNN")
        
        col_k, col_weights = st.columns(2)
        
        with col_k:
            n_neighbors = st.slider("Nombre de voisins (k) :",
                                  1, 20, 3, 1,
                                  help="Nombre de voisins considérés pour la décision")
        
        with col_weights:
            weights = st.selectbox("Poids des voisins :",
                                 ['uniform', 'distance'],
                                 help="Poids uniforme ou proportionnel à la distance")
        
        # Création et entraînement
        knn = KNeighborsClassifier(n_neighbors=n_neighbors, weights=weights)
        knn.fit(X_train_scaled, y_train)
        
        st.success(f"✅ Modèle KNN entraîné avec k={n_neighbors}")
        
        # Score sur le train
        train_score = knn.score(X_train_scaled, y_train)
        st.metric("Score sur l'entraînement", f"{train_score*100:.1f}%")
        
        st.markdown("---")
        
        # 5. Évaluation
        st.subheader("5. Évaluation sur l'ensemble de test")
        
        # Prédictions
        y_pred = knn.predict(X_test_scaled)
        y_pred_labels = le.inverse_transform(y_pred)
        y_test_labels = le.inverse_transform(y_test)
        
        # Matrice de confusion
        st.markdown("**Matrice de confusion**")
        
        conf_mat = confusion_matrix(y_test, y_pred)
        
        fig_conf, ax_conf = plt.subplots(figsize=(8, 6))
        sns.heatmap(conf_mat, annot=True, fmt='d', cmap='Blues',
                   xticklabels=le.classes_, yticklabels=le.classes_,
                   ax=ax_conf, cbar_kws={'label': 'Nombre'})
        
        ax_conf.set_xlabel('Prédictions', fontweight='bold')
        ax_conf.set_ylabel('Vraies classes', fontweight='bold')
        ax_conf.set_title('Matrice de confusion', fontweight='bold')
        
        st.pyplot(fig_conf)
        
        # Métriques
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred, target_names=le.classes_,
                                      output_dict=True)
        report_df = pd.DataFrame(report).transpose()
        
        col_acc, col_prec, col_rec, col_f1 = st.columns(4)
        
        with col_acc:
            st.metric("Exactitude (Accuracy)", f"{accuracy*100:.2f}%")
        
        with col_prec:
            prec = report_df.loc['weighted avg', 'precision']
            st.metric("Précision moyenne", f"{prec*100:.2f}%")
        
        with col_rec:
            rec = report_df.loc['weighted avg', 'recall']
            st.metric("Rappel moyen", f"{rec*100:.2f}%")
        
        with col_f1:
            f1 = report_df.loc['weighted avg', 'f1-score']
            st.metric("F1-score moyen", f"{f1*100:.2f}%")
        
        # Rapport détaillé
        st.markdown("**Rapport de classification**")
        st.dataframe(report_df.round(3).style
                    .background_gradient(subset=['precision', 'recall', 'f1-score'], cmap='YlGnBu'),
                    use_container_width=True)
        
        # Analyse des erreurs
        errors = y_test_labels != y_pred_labels
        if errors.any():
            st.warning(f"⚠️ {errors.sum()} erreur(s) de prédiction")
            
            error_data = []
            for idx in np.where(errors)[0]:
                error_data.append({
                    'Échantillon': idx,
                    'Vraie classe': y_test_labels[idx],
                    'Prédiction': y_pred_labels[idx],
                    'Confiance': np.max(knn.predict_proba([X_test_scaled[idx]])[0])
                })
            
            error_df = pd.DataFrame(error_data)
            st.dataframe(error_df, use_container_width=True)
        else:
            st.success("🎉 Parfait ! Aucune erreur de prédiction.")
        
        st.markdown("---")
        
        # 6. Prédiction interactive
        st.subheader("6. Prédiction interactive")
        
        st.markdown("**Testez le modèle avec de nouvelles valeurs :**")
        
        col_input1, col_input2, col_input3, col_input4 = st.columns(4)
        
        with col_input1:
            sl = st.number_input("Longueur sépale (cm)", 0.0, 10.0, 5.1, 0.1)
        
        with col_input2:
            sw = st.number_input("Largeur sépale (cm)", 0.0, 10.0, 3.5, 0.1)
        
        with col_input3:
            pl = st.number_input("Longueur pétale (cm)", 0.0, 10.0, 1.4, 0.1)
        
        with col_input4:
            pw = st.number_input("Largeur pétale (cm)", 0.0, 10.0, 0.2, 0.1)
        
        if st.button("🔮 Prédire l'espèce", type="primary"):
            input_data = [[sl, sw, pl, pw]]
            input_scaled = scaler.transform(input_data)
            
            prediction_code = knn.predict(input_scaled)[0]
            prediction = le.inverse_transform([prediction_code])[0]
            probabilities = knn.predict_proba(input_scaled)[0]
            
            col_result, col_proba = st.columns(2)
            
            with col_result:
                st.success(f"**Espèce prédite : {prediction}**")
                color = species_palette[prediction]
                html = f"""
                <div style="background-color:{color}; padding:20px; border-radius:10px; text-align:center;">
                    <h2 style="color:white; margin:0;">{prediction.upper()}</h2>
                </div>
                """
                st.markdown(html, unsafe_allow_html=True)
            
            with col_proba:
                st.markdown("**Probabilités :**")
                for i, species in enumerate(le.classes_):
                    prob = probabilities[i] * 100
                    st.write(f"{species} : {prob:.1f}%")
                    st.progress(float(prob/100))
            
            # Comparaison avec les moyennes
            st.markdown("**Comparaison avec les moyennes :**")
            means = df.groupby('species')[quantitative_vars].mean()
            
            comp_data = []
            for species in le.classes_:
                dist = np.sqrt(np.sum((input_data[0] - means.loc[species].values) ** 2))
                comp_data.append({
                    'Espèce': species,
                    'Distance euclidienne': f"{dist:.2f}",
                    'Similarité': f"{(1-dist/max(dist, 0.1))*100:.1f}%"
                })
            
            comp_df = pd.DataFrame(comp_data)
            st.dataframe(comp_df, use_container_width=True)
    
    except ImportError:
        st.error("""
        ❌ Scikit-learn n'est pas installé !
        
        Pour installer :
        ```bash
        pip install scikit-learn
        ```
        """)

# ============================================================================
# OPTIMISATION & COMPARAISON
# ============================================================================

elif menu_option == "📈 Optimisation & Comparaison":
    st.title("📈 Optimisation et comparaison des modèles")
    
    try:
        from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
        from sklearn.preprocessing import StandardScaler, LabelEncoder
        from sklearn.neighbors import KNeighborsClassifier
        from sklearn.linear_model import LogisticRegression
        from sklearn.tree import DecisionTreeClassifier
        from sklearn.svm import SVC
        from sklearn.naive_bayes import GaussianNB
        from sklearn.metrics import accuracy_score
        
        st.markdown("""
        ### Objectif
        Optimiser le modèle KNN et comparer avec d'autres algorithmes de classification.
        """)
        
        # Préparation des données
        le = LabelEncoder()
        df_model = df.copy()
        df_model['species_encoded'] = le.fit_transform(df_model['species'])
        
        X = df_model[quantitative_vars]
        y = df_model['species_encoded']
        
        # Normalisation
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        st.markdown("---")
        
        # 1. Optimisation de KNN
        st.subheader("1. Optimisation du paramètre k pour KNN")
        
        # Recherche du meilleur k
        k_values = list(range(1, 31))
        cv_scores = []
        
        for k in k_values:
            knn_temp = KNeighborsClassifier(n_neighbors=k)
            scores = cross_val_score(knn_temp, X_scaled, y, cv=5, scoring='accuracy')
            cv_scores.append(scores.mean())
        
        best_k = k_values[cv_scores.index(max(cv_scores))]
        
        # Visualisation
        fig_k, ax_k = plt.subplots(figsize=(12, 6))
        
        ax_k.plot(k_values, cv_scores, 'o-', linewidth=2, markersize=8)
        ax_k.axvline(x=best_k, color='red', linestyle='--',
                    label=f'Meilleur k = {best_k}')
        ax_k.axhline(y=max(cv_scores), color='green', linestyle=':',
                    label=f'Meilleur score = {max(cv_scores):.3f}')
        
        ax_k.set_xlabel('Nombre de voisins (k)', fontweight='bold')
        ax_k.set_ylabel('Score de validation croisée', fontweight='bold')
        ax_k.set_title('Optimisation du paramètre k pour KNN (5-fold CV)', fontweight='bold')
        ax_k.legend()
        ax_k.grid(True, alpha=0.3)
        ax_k.set_xticks(k_values[::2])
        
        st.pyplot(fig_k)
        
        st.info(f"""
        **🎯 Meilleur paramètre : k = {best_k}**
        - Score moyen : {max(cv_scores)*100:.1f}%
        - Recommandation : utiliser k = {best_k} pour de nouvelles prédictions
        """)
        
        st.markdown("""
        **📊 Interprétation :**
        - k trop petit (< 5) : risque de surapprentissage (trop sensible au bruit)
        - k trop grand (> 15) : risque de sous-apprentissage (perte de détails locaux)
        - Optimum : compromis entre précision et robustesse
        """)
        
        st.markdown("---")
        
       
    
    except ImportError:
        st.error("Scikit-learn requis pour cette partie. Installation : `pip install scikit-learn`")

# ============================================================================
# PIED DE PAGE
# ============================================================================


st.markdown("**TP1 INFO40113 - Réalisé par TCHUENTEU GUETCHUENG DAVID (20U2891)**")
>>>>>>> a9cc1fa4cdb8ee150b9179b7ade5923cb663abd5
