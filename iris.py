#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Application Streamlit - TP Classification des Fleurs Iris
Université de Yaoundé 1 - École Normale Supérieure
Module: Introduction à l'IA et Machine Learning (INFO4111)
"""

import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Configuration de la page
st.set_page_config(
    page_title="TP Iris - Classification ML",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Style CSS personnalisé
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #43A047;
        font-weight: bold;
        margin-top: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #1E88E5;
    }
    .stAlert {
        background-color: #E3F2FD;
    }
    </style>
""", unsafe_allow_html=True)

# Titre principal
st.markdown('<p class="main-header">🌸 TP N°1: Classification des Fleurs Iris</p>', unsafe_allow_html=True)
st.markdown("### 📚 Université de Yaoundé 1 - École Normale Supérieure")
st.markdown("**Module:** Introduction à l'IA et Machine Learning (INFO4111)")
st.markdown("---")

# Fonction pour charger les données
@st.cache_data
def load_data():
    """Charge le dataset Iris"""
    try:
        df = pd.read_csv('Iris.csv', sep=';')
    except:
        # Si le fichier n'est pas trouvé localement, utiliser le chemin complet
        df = pd.read_csv('/mnt/user-data/uploads/Iris.csv', sep=';')
    return df

# Charger les données
df = load_data()

# Sidebar pour la navigation
st.sidebar.title("📋 Navigation")
page = st.sidebar.radio(
    "Choisir une section:",
    ["🏠 Accueil", 
     "📊 Exploration des Données", 
     "📈 Visualisations", 
     "🤖 Modélisation ML", 
     "🔮 Prédiction Interactive",
     "📝 Rapport Complet"]
)

st.sidebar.markdown("---")
st.sidebar.info("💡 **Astuce:** Utilisez la navigation pour explorer toutes les sections du TP!")

# ==================== PAGE ACCUEIL ====================
if page == "🏠 Accueil":
    st.markdown('<p class="sub-header">📖 À propos du TP</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("**🎯 Objectif Principal**\n\nClassifier automatiquement les espèces de fleurs Iris en utilisant le Machine Learning")
    
    with col2:
        st.success("**📊 Dataset**\n\n150 observations de 3 espèces d'Iris avec 4 caractéristiques morphologiques")
    
    with col3:
        st.warning("**🔬 Variables**\n\nLongueur/Largeur des Sépales et Pétales (en cm)")
    
    st.markdown("### 📚 Contexte Historique")
    st.write("""
    Ce dataset classique a été collecté par **Edgar Anderson** et utilisé par 
    **Sir R.A. Fisher** en 1936 pour développer l'analyse discriminante linéaire.
    Il reste l'un des datasets les plus utilisés pour l'apprentissage du Machine Learning.
    """)
    
    st.markdown("### 🎓 Objectifs Pédagogiques")
    objectives = [
        "Familiarisation avec Python pour la Data Science",
        "Utilisation des librairies pandas, numpy, matplotlib, seaborn, scikit-learn",
        "Exploration et visualisation de données",
        "Préparation des données pour le ML",
        "Création et entraînement de modèles de classification",
        "Évaluation et comparaison de performances",
        "Déploiement d'un modèle simple"
    ]
    
    for i, obj in enumerate(objectives, 1):
        st.markdown(f"{i}. ✅ {obj}")
    
    # Aperçu rapide des données
    st.markdown("### 👀 Aperçu Rapide des Données")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Nombre d'observations", df.shape[0])
    with col2:
        st.metric("Nombre de variables", df.shape[1])
    with col3:
        st.metric("Espèces uniques", df['Species'].nunique())
    with col4:
        st.metric("Données manquantes", df.isnull().sum().sum())
    
    st.dataframe(df.head(10), use_container_width=True)

# ==================== PAGE EXPLORATION ====================
elif page == "📊 Exploration des Données":
    st.markdown('<p class="sub-header">📊 Exploration des Données</p>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Statistiques", "🔢 Distribution", "🎯 Par Espèce", "🔍 Détails"])
    
    with tab1:
        st.markdown("#### 📈 Statistiques Descriptives")
        st.dataframe(df.describe(), use_container_width=True)
        
        st.markdown("#### 📊 Informations sur le Dataset")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Structure des données:**")
            buffer = df.dtypes.to_frame(name='Type')
            st.dataframe(buffer, use_container_width=True)
        
        with col2:
            st.write("**Répartition des espèces:**")
            species_count = df['Species'].value_counts()
            st.dataframe(species_count.to_frame(name='Effectif'), use_container_width=True)
    
    with tab2:
        st.markdown("#### 📊 Distribution des Variables Numériques")
        
        variable = st.selectbox(
            "Choisir une variable:",
            ['SepalLength', 'SepalWidth', 'PetalLength', 'PetalWidth']
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.hist(df[variable], bins=20, color='#4ECDC4', edgecolor='black', alpha=0.7)
            ax.set_xlabel(variable, fontweight='bold')
            ax.set_ylabel('Fréquence', fontweight='bold')
            ax.set_title(f'Distribution de {variable}', fontweight='bold')
            ax.grid(True, alpha=0.3)
            st.pyplot(fig)
        
        with col2:
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.boxplot(df[variable], vert=True)
            ax.set_ylabel('Valeur (cm)', fontweight='bold')
            ax.set_title(f'Boxplot de {variable}', fontweight='bold')
            ax.grid(True, alpha=0.3)
            st.pyplot(fig)
        
        # Statistiques de la variable sélectionnée
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Moyenne", f"{df[variable].mean():.2f} cm")
        with col2:
            st.metric("Médiane", f"{df[variable].median():.2f} cm")
        with col3:
            st.metric("Écart-type", f"{df[variable].std():.2f} cm")
        with col4:
            st.metric("Étendue", f"{df[variable].max() - df[variable].min():.2f} cm")
    
    with tab3:
        st.markdown("#### 🎯 Analyse par Espèce")
        
        species_selected = st.multiselect(
            "Sélectionner les espèces à comparer:",
            df['Species'].unique(),
            default=df['Species'].unique()
        )
        
        if species_selected:
            df_filtered = df[df['Species'].isin(species_selected)]
            
            st.markdown("##### Statistiques par Espèce")
            st.dataframe(df_filtered.groupby('Species').describe().T, use_container_width=True)
            
            # Boxplots comparatifs
            st.markdown("##### Comparaison Visuelle")
            fig, axes = plt.subplots(2, 2, figsize=(14, 10))
            variables = ['SepalLength', 'SepalWidth', 'PetalLength', 'PetalWidth']
            
            for i, var in enumerate(variables):
                ax = axes[i//2, i%2]
                df_filtered.boxplot(column=var, by='Species', ax=ax, patch_artist=True)
                ax.set_title(f'{var} par Espèce', fontweight='bold')
                ax.set_xlabel('Espèce')
                ax.set_ylabel(f'{var} (cm)')
                plt.sca(ax)
                plt.xticks(rotation=45)
            
            plt.tight_layout()
            st.pyplot(fig)
    
    with tab4:
        st.markdown("#### 🔍 Vue Détaillée des Données")
        
        # Filtres
        col1, col2 = st.columns(2)
        with col1:
            species_filter = st.multiselect(
                "Filtrer par espèce:",
                df['Species'].unique(),
                default=df['Species'].unique()
            )
        
        with col2:
            n_rows = st.slider("Nombre de lignes à afficher:", 5, 150, 20)
        
        df_display = df[df['Species'].isin(species_filter)].head(n_rows)
        st.dataframe(df_display, use_container_width=True)
        
        # Téléchargement
        csv = df_display.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Télécharger les données filtrées (CSV)",
            data=csv,
            file_name='iris_filtered.csv',
            mime='text/csv',
        )

# ==================== PAGE VISUALISATIONS ====================
elif page == "📈 Visualisations":
    st.markdown('<p class="sub-header">📈 Visualisations Avancées</p>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["🎨 Distributions", "🔗 Corrélations", "📊 Pairplot", "🌐 3D", "📉 Interactif"]
    )
    
    with tab1:
        st.markdown("#### 🎨 Distribution des Espèces")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Diagramme en barres
            fig = px.histogram(df, x='Species', color='Species',
                             title='Distribution des Espèces',
                             labels={'Species': 'Espèce', 'count': 'Nombre'},
                             color_discrete_sequence=['#FF6B6B', '#4ECDC4', '#45B7D1'])
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Diagramme en secteurs
            species_count = df['Species'].value_counts()
            fig = px.pie(values=species_count.values, names=species_count.index,
                        title='Répartition en Pourcentage',
                        color_discrete_sequence=['#FF6B6B', '#4ECDC4', '#45B7D1'])
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("#### 📊 Distribution des Variables par Espèce")
        
        variable_viz = st.selectbox(
            "Sélectionner une variable:",
            ['SepalLength', 'SepalWidth', 'PetalLength', 'PetalWidth'],
            key='viz_var'
        )
        
        fig = px.box(df, x='Species', y=variable_viz, color='Species',
                    title=f'Distribution de {variable_viz} par Espèce',
                    color_discrete_sequence=['#FF6B6B', '#4ECDC4', '#45B7D1'])
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.markdown("#### 🔗 Matrice de Corrélation")
        
        corr_matrix = df[['SepalLength', 'SepalWidth', 'PetalLength', 'PetalWidth']].corr()
        
        fig = px.imshow(corr_matrix, 
                       text_auto=True,
                       aspect="auto",
                       color_continuous_scale='RdBu_r',
                       title='Matrice de Corrélation des Variables')
        st.plotly_chart(fig, use_container_width=True)
        
        st.info("""
        **💡 Interprétation:**
        - Corrélation positive forte (> 0.7): Les variables évoluent ensemble
        - Corrélation négative: Les variables évoluent en sens inverse
        - Corrélation faible (< 0.3): Peu de relation linéaire
        """)
        
        # Top corrélations
        st.markdown("#### 🔝 Corrélations les Plus Fortes")
        
        corr_pairs = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr_pairs.append({
                    'Variable 1': corr_matrix.columns[i],
                    'Variable 2': corr_matrix.columns[j],
                    'Corrélation': corr_matrix.iloc[i, j]
                })
        
        corr_df = pd.DataFrame(corr_pairs).sort_values('Corrélation', ascending=False)
        st.dataframe(corr_df, use_container_width=True)
    
    with tab3:
        st.markdown("#### 📊 Pairplot - Relations entre Variables")
        
        st.info("Ce graphique montre les relations deux à deux entre toutes les variables numériques.")
        
        # Pairplot avec matplotlib/seaborn
        fig = plt.figure(figsize=(12, 10))
        
        # Pairplot manuel
        variables = ['SepalLength', 'SepalWidth', 'PetalLength', 'PetalWidth']
        n_vars = len(variables)
        
        for i in range(n_vars):
            for j in range(n_vars):
                ax = plt.subplot(n_vars, n_vars, i * n_vars + j + 1)
                
                if i == j:
                    # Diagonale: histogrammes
                    for species in df['Species'].unique():
                        subset = df[df['Species'] == species]
                        ax.hist(subset[variables[i]], alpha=0.5, label=species, bins=15)
                    if i == 0:
                        ax.legend(fontsize=8)
                else:
                    # Hors diagonale: scatter plots
                    for species in df['Species'].unique():
                        subset = df[df['Species'] == species]
                        ax.scatter(subset[variables[j]], subset[variables[i]], 
                                 alpha=0.6, s=20, label=species)
                
                if i == n_vars - 1:
                    ax.set_xlabel(variables[j], fontsize=9)
                else:
                    ax.set_xticklabels([])
                
                if j == 0:
                    ax.set_ylabel(variables[i], fontsize=9)
                else:
                    ax.set_yticklabels([])
        
        plt.tight_layout()
        st.pyplot(fig)
    
    with tab4:
        st.markdown("#### 🌐 Visualisation 3D")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            x_axis = st.selectbox("Axe X:", ['SepalLength', 'SepalWidth', 'PetalLength', 'PetalWidth'], index=0)
        with col2:
            y_axis = st.selectbox("Axe Y:", ['SepalLength', 'SepalWidth', 'PetalLength', 'PetalWidth'], index=2)
        with col3:
            z_axis = st.selectbox("Axe Z:", ['SepalLength', 'SepalWidth', 'PetalLength', 'PetalWidth'], index=3)
        
        fig = px.scatter_3d(df, x=x_axis, y=y_axis, z=z_axis, color='Species',
                           title=f'Visualisation 3D: {x_axis} vs {y_axis} vs {z_axis}',
                           color_discrete_sequence=['#FF6B6B', '#4ECDC4', '#45B7D1'],
                           height=600)
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tab5:
        st.markdown("#### 📉 Graphique Interactif Personnalisé")
        
        col1, col2 = st.columns(2)
        
        with col1:
            x_var = st.selectbox("Variable X:", 
                                ['SepalLength', 'SepalWidth', 'PetalLength', 'PetalWidth'],
                                key='x_interactive')
            
            chart_type = st.radio("Type de graphique:",
                                 ["Scatter", "Line", "Box"])
        
        with col2:
            y_var = st.selectbox("Variable Y:", 
                                ['SepalLength', 'SepalWidth', 'PetalLength', 'PetalWidth'],
                                index=1,
                                key='y_interactive')
            
            color_by = st.checkbox("Colorer par espèce", value=True)
        
        if chart_type == "Scatter":
            if color_by:
                fig = px.scatter(df, x=x_var, y=y_var, color='Species',
                               title=f'{x_var} vs {y_var}',
                               color_discrete_sequence=['#FF6B6B', '#4ECDC4', '#45B7D1'])
            else:
                fig = px.scatter(df, x=x_var, y=y_var,
                               title=f'{x_var} vs {y_var}')
        
        elif chart_type == "Line":
            fig = px.line(df.sort_values(x_var), x=x_var, y=y_var, color='Species' if color_by else None,
                         title=f'{x_var} vs {y_var}')
        
        else:  # Box
            fig = px.box(df, x='Species', y=y_var, color='Species',
                        title=f'Distribution de {y_var} par Espèce',
                        color_discrete_sequence=['#FF6B6B', '#4ECDC4', '#45B7D1'])
        
        st.plotly_chart(fig, use_container_width=True)

# ==================== PAGE MODÉLISATION ====================
elif page == "🤖 Modélisation ML":
    st.markdown('<p class="sub-header">🤖 Modélisation Machine Learning</p>', unsafe_allow_html=True)
    
    # Préparation des données
    X = df.drop('Species', axis=1)
    y = df['Species']
    
    # Paramètres dans la sidebar
    st.sidebar.markdown("### ⚙️ Paramètres du Modèle")
    test_size = st.sidebar.slider("Taille du test set (%)", 10, 40, 20) / 100
    random_state = st.sidebar.number_input("Random State", 0, 100, 42)
    normalize = st.sidebar.checkbox("Normaliser les données", value=True)
    
    # Split des données
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    
    # Normalisation
    if normalize:
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
    else:
        X_train_scaled = X_train
        X_test_scaled = X_test
    
    # Affichage des informations
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Données d'entraînement", len(X_train))
    with col2:
        st.metric("Données de test", len(X_test))
    with col3:
        st.metric("Features", X.shape[1])
    with col4:
        st.metric("Classes", y.nunique())
    
    st.markdown("---")
    
    # Tabs pour différents modèles
    tab1, tab2, tab3 = st.tabs(["🎯 Entraînement Rapide", "⚖️ Comparaison de Modèles", "🔧 Optimisation"])
    
    with tab1:
        st.markdown("### 🎯 Entraînement d'un Modèle")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            model_choice = st.selectbox(
                "Choisir un modèle:",
                ["K-Nearest Neighbors (KNN)", 
                 "Logistic Regression",
                 "Decision Tree",
                 "Naive Bayes",
                 "Support Vector Machine (SVM)"]
            )
            
            # Paramètres spécifiques au modèle
            if model_choice == "K-Nearest Neighbors (KNN)":
                n_neighbors = st.slider("Nombre de voisins (k)", 1, 20, 3)
                model = KNeighborsClassifier(n_neighbors=n_neighbors)
            
            elif model_choice == "Logistic Regression":
                max_iter = st.slider("Itérations max", 100, 1000, 200)
                model = LogisticRegression(max_iter=max_iter)
            
            elif model_choice == "Decision Tree":
                max_depth = st.slider("Profondeur max", 1, 20, 5)
                model = DecisionTreeClassifier(max_depth=max_depth, random_state=random_state)
            
            elif model_choice == "Naive Bayes":
                model = GaussianNB()
                st.info("Pas d'hyperparamètres à configurer")
            
            else:  # SVM
                C = st.slider("Paramètre C", 0.1, 10.0, 1.0)
                model = SVC(C=C, random_state=random_state)
            
            if st.button("🚀 Entraîner le Modèle", type="primary"):
                with st.spinner("Entraînement en cours..."):
                    # Entraînement
                    model.fit(X_train_scaled, y_train)
                    
                    # Prédictions
                    y_pred = model.predict(X_test_scaled)
                    
                    # Stockage dans session state
                    st.session_state['model'] = model
                    st.session_state['scaler'] = scaler if normalize else None
                    st.session_state['y_pred'] = y_pred
                    st.session_state['y_test'] = y_test
                    
                    st.success("✅ Modèle entraîné avec succès!")
        
        with col2:
            if 'y_pred' in st.session_state:
                y_pred = st.session_state['y_pred']
                y_test = st.session_state['y_test']
                
                # Métriques
                accuracy = accuracy_score(y_test, y_pred)
                
                st.markdown("### 📊 Résultats")
                st.metric("🎯 Accuracy", f"{accuracy * 100:.2f}%", 
                         delta=f"{(accuracy - 0.5) * 100:.1f}% vs random")
                
                # Matrice de confusion
                st.markdown("#### 🔲 Matrice de Confusion")
                conf_matrix = confusion_matrix(y_test, y_pred)
                
                fig = px.imshow(conf_matrix,
                              labels=dict(x="Prédictions", y="Vraies Classes", color="Nombre"),
                              x=df['Species'].unique(),
                              y=df['Species'].unique(),
                              text_auto=True,
                              color_continuous_scale='Blues')
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
                
                # Rapport de classification
                st.markdown("#### 📋 Rapport de Classification")
                report = classification_report(y_test, y_pred, output_dict=True)
                report_df = pd.DataFrame(report).transpose()
                st.dataframe(report_df.style.highlight_max(axis=0, color='lightgreen'), 
                           use_container_width=True)
    
    with tab2:
        st.markdown("### ⚖️ Comparaison de Tous les Modèles")
        
        if st.button("🔄 Comparer les Modèles", type="primary"):
            models = {
                'KNN (k=3)': KNeighborsClassifier(n_neighbors=3),
                'KNN (k=5)': KNeighborsClassifier(n_neighbors=5),
                'Logistic Regression': LogisticRegression(max_iter=200),
                'Decision Tree': DecisionTreeClassifier(max_depth=5, random_state=random_state),
                'Naive Bayes': GaussianNB(),
                'SVM': SVC(random_state=random_state)
            }
            
            results = []
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i, (name, model) in enumerate(models.items()):
                status_text.text(f"Entraînement de {name}...")
                
                # Entraînement
                model.fit(X_train_scaled, y_train)
                
                # Prédictions
                y_pred = model.predict(X_test_scaled)
                
                # Métriques
                accuracy = accuracy_score(y_test, y_pred)
                
                # Validation croisée
                cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=5)
                
                results.append({
                    'Modèle': name,
                    'Accuracy Test': accuracy,
                    'Accuracy CV (mean)': cv_scores.mean(),
                    'Accuracy CV (std)': cv_scores.std()
                })
                
                progress_bar.progress((i + 1) / len(models))
            
            status_text.text("✅ Comparaison terminée!")
            
            # Affichage des résultats
            results_df = pd.DataFrame(results).sort_values('Accuracy Test', ascending=False)
            
            st.markdown("#### 🏆 Résultats de la Comparaison")
            st.dataframe(
                results_df.style.highlight_max(subset=['Accuracy Test', 'Accuracy CV (mean)'], 
                                               color='lightgreen'),
                use_container_width=True
            )
            
            # Graphique de comparaison
            fig = px.bar(results_df, x='Modèle', y='Accuracy Test',
                        title='Comparaison des Performances',
                        color='Accuracy Test',
                        color_continuous_scale='Viridis')
            fig.add_hline(y=results_df['Accuracy Test'].mean(), 
                         line_dash="dash", 
                         annotation_text="Moyenne",
                         line_color="red")
            st.plotly_chart(fig, use_container_width=True)
            
            # Meilleur modèle
            best_model = results_df.iloc[0]
            st.success(f"""
            🏆 **Meilleur Modèle:** {best_model['Modèle']}
            - Accuracy Test: {best_model['Accuracy Test']*100:.2f}%
            - Accuracy CV: {best_model['Accuracy CV (mean)']*100:.2f}% (±{best_model['Accuracy CV (std)']*100:.2f}%)
            """)
    
    with tab3:
        st.markdown("### 🔧 Optimisation des Hyperparamètres (KNN)")
        
        st.info("Cette section explore différentes valeurs de k pour trouver le meilleur paramètre.")
        
        max_k = st.slider("Tester jusqu'à k =", 1, 30, 20)
        
        if st.button("🔍 Lancer l'Optimisation"):
            k_values = range(1, max_k + 1)
            train_scores = []
            test_scores = []
            
            progress_bar = st.progress(0)
            
            for i, k in enumerate(k_values):
                knn = KNeighborsClassifier(n_neighbors=k)
                knn.fit(X_train_scaled, y_train)
                
                train_scores.append(knn.score(X_train_scaled, y_train))
                test_scores.append(knn.score(X_test_scaled, y_test))
                
                progress_bar.progress((i + 1) / len(k_values))
            
            # Graphique
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=list(k_values), y=train_scores, 
                                    mode='lines+markers', name='Train',
                                    line=dict(color='blue')))
            fig.add_trace(go.Scatter(x=list(k_values), y=test_scores, 
                                    mode='lines+markers', name='Test',
                                    line=dict(color='red')))
            
            fig.update_layout(
                title='Accuracy en fonction de k',
                xaxis_title='Nombre de voisins (k)',
                yaxis_title='Accuracy',
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Meilleur k
            best_k = k_values[np.argmax(test_scores)]
            best_accuracy = max(test_scores)
            
            st.success(f"""
            ✨ **Meilleur paramètre trouvé:**
            - k optimal = {best_k}
            - Accuracy = {best_accuracy*100:.2f}%
            """)

# ==================== PAGE PRÉDICTION ====================
elif page == "🔮 Prédiction Interactive":
    st.markdown('<p class="sub-header">🔮 Prédiction Interactive</p>', unsafe_allow_html=True)
    
    st.info("👉 Entrez les caractéristiques d'une fleur Iris pour prédire son espèce!")
    
    # Vérifier si un modèle est entraîné
    if 'model' not in st.session_state:
        st.warning("⚠️ Aucun modèle entraîné. Allez d'abord dans la section 'Modélisation ML'.")
        
        # Proposer d'entraîner un modèle rapide
        if st.button("🚀 Entraîner un modèle KNN rapide"):
            X = df.drop('Species', axis=1)
            y = df['Species']
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            
            model = KNeighborsClassifier(n_neighbors=3)
            model.fit(X_train_scaled, y_train)
            
            st.session_state['model'] = model
            st.session_state['scaler'] = scaler
            
            st.success("✅ Modèle KNN entraîné avec succès!")
            st.rerun()
    
    else:
        model = st.session_state['model']
        scaler = st.session_state.get('scaler', None)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("### 📝 Entrez les Mesures")
            
            # Inputs avec les valeurs moyennes par défaut
            sepal_length = st.slider(
                "Longueur du Sépale (cm)",
                float(df['SepalLength'].min()),
                float(df['SepalLength'].max()),
                float(df['SepalLength'].mean()),
                0.1
            )
            
            sepal_width = st.slider(
                "Largeur du Sépale (cm)",
                float(df['SepalWidth'].min()),
                float(df['SepalWidth'].max()),
                float(df['SepalWidth'].mean()),
                0.1
            )
            
            petal_length = st.slider(
                "Longueur du Pétale (cm)",
                float(df['PetalLength'].min()),
                float(df['PetalLength'].max()),
                float(df['PetalLength'].mean()),
                0.1
            )
            
            petal_width = st.slider(
                "Largeur du Pétale (cm)",
                float(df['PetalWidth'].min()),
                float(df['PetalWidth'].max()),
                float(df['PetalWidth'].mean()),
                0.1
            )
            
            # Boutons prédéfinis
            st.markdown("#### 🌸 Exemples Prédéfinis")
            col_a, col_b, col_c = st.columns(3)
            
            if col_a.button("Setosa type"):
                sepal_length, sepal_width = 5.1, 3.5
                petal_length, petal_width = 1.4, 0.2
            
            if col_b.button("Versicolor type"):
                sepal_length, sepal_width = 5.9, 3.0
                petal_length, petal_width = 4.2, 1.5
            
            if col_c.button("Virginica type"):
                sepal_length, sepal_width = 6.5, 3.0
                petal_length, petal_width = 5.5, 2.0
        
        with col2:
            st.markdown("### 🎯 Prédiction")
            
            # Préparer les données
            input_data = np.array([[sepal_length, sepal_width, petal_length, petal_width]])
            
            if scaler is not None:
                input_data_scaled = scaler.transform(input_data)
            else:
                input_data_scaled = input_data
            
            # Prédiction
            prediction = model.predict(input_data_scaled)[0]
            
            # Probabilités (si disponible)
            if hasattr(model, 'predict_proba'):
                probas = model.predict_proba(input_data_scaled)[0]
                
                st.markdown(f"### 🌸 Espèce Prédite: **{prediction}**")
                
                st.markdown("#### 📊 Probabilités:")
                
                proba_df = pd.DataFrame({
                    'Espèce': model.classes_,
                    'Probabilité': probas
                }).sort_values('Probabilité', ascending=False)
                
                for _, row in proba_df.iterrows():
                    st.progress(row['Probabilité'], text=f"{row['Espèce']}: {row['Probabilité']*100:.1f}%")
                
                # Graphique
                fig = px.bar(proba_df, x='Espèce', y='Probabilité',
                           title='Probabilités de Prédiction',
                           color='Probabilité',
                           color_continuous_scale='Viridis')
                st.plotly_chart(fig, use_container_width=True)
            
            else:
                st.markdown(f"### 🌸 Espèce Prédite: **{prediction}**")
                st.info("Ce modèle ne fournit pas de probabilités.")
            
            # Visualisation de la fleur dans l'espace des features
            st.markdown("#### 📍 Position dans l'Espace des Données")
            
            fig = px.scatter(df, x='PetalLength', y='PetalWidth', color='Species',
                           title='Votre fleur dans l\'espace Pétale',
                           color_discrete_sequence=['#FF6B6B', '#4ECDC4', '#45B7D1'])
            
            # Ajouter le point de prédiction
            fig.add_trace(go.Scatter(
                x=[petal_length],
                y=[petal_width],
                mode='markers',
                marker=dict(size=20, color='yellow', symbol='star', line=dict(color='black', width=2)),
                name='Votre fleur',
                showlegend=True
            ))
            
            st.plotly_chart(fig, use_container_width=True)

# ==================== PAGE RAPPORT ====================
elif page == "📝 Rapport Complet":
    st.markdown('<p class="sub-header">📝 Rapport Complet de l\'Analyse</p>', unsafe_allow_html=True)
    
    st.markdown("""
    ## 📊 Résumé Exécutif
    
    Cette analyse porte sur le dataset classique **Iris** contenant 150 observations de 3 espèces de fleurs Iris.
    L'objectif est de construire un modèle de classification capable de prédire l'espèce en fonction des 
    mesures morphologiques.
    """)
    
    # Section 1: Dataset
    st.markdown("---")
    st.markdown("### 1️⃣ Description du Dataset")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Caractéristiques:**
        - 150 observations
        - 4 variables numériques (features)
        - 1 variable catégorielle (cible)
        - 3 classes parfaitement équilibrées (50 observations chacune)
        - Aucune donnée manquante
        """)
    
    with col2:
        st.markdown("""
        **Variables:**
        - SepalLength: Longueur du sépale (cm)
        - SepalWidth: Largeur du sépale (cm)
        - PetalLength: Longueur du pétale (cm)
        - PetalWidth: Largeur du pétale (cm)
        - Species: Espèce (setosa, versicolor, virginica)
        """)
    
    # Statistiques
    st.dataframe(df.describe(), use_container_width=True)
    
    # Section 2: Insights
    st.markdown("---")
    st.markdown("### 2️⃣ Insights Clés")
    
    st.markdown("""
    #### 📈 Observations Principales:
    
    1. **Variabilité des Features:**
       - Les pétales montrent plus de variabilité que les sépales
       - PetalLength a l'étendue la plus grande (1.0 - 6.9 cm)
       - SepalWidth a l'étendue la plus faible (2.0 - 4.4 cm)
    
    2. **Corrélations:**
       - Forte corrélation positive entre PetalLength et PetalWidth (r = 0.96)
       - Forte corrélation entre SepalLength et PetalLength (r = 0.87)
       - Faible corrélation négative entre SepalWidth et autres variables
    
    3. **Séparabilité des Classes:**
       - Setosa est clairement séparable des deux autres espèces
       - Versicolor et Virginica se chevauchent partiellement
       - Les mesures de pétales sont plus discriminantes que celles des sépales
    """)
    
    # Section 3: Modélisation
    st.markdown("---")
    st.markdown("### 3️⃣ Résultats de la Modélisation")
    
    if 'y_pred' in st.session_state:
        accuracy = accuracy_score(st.session_state['y_test'], st.session_state['y_pred'])
        
        st.success(f"""
        **✅ Performance du Modèle:**
        - Accuracy sur le test set: {accuracy*100:.2f}%
        - Le modèle généralise bien sur des données non vues
        """)
        
        report = classification_report(st.session_state['y_test'], 
                                      st.session_state['y_pred'], 
                                      output_dict=True)
        report_df = pd.DataFrame(report).transpose()
        
        st.dataframe(report_df, use_container_width=True)
    
    else:
        st.info("Entraînez un modèle dans la section 'Modélisation ML' pour voir les résultats ici.")
    
    # Section 4: Conclusions
    st.markdown("---")
    st.markdown("### 4️⃣ Conclusions et Recommandations")
    
    st.markdown("""
    #### ✅ Conclusions:
    
    1. **Qualité des Données:**
       - Dataset bien structuré et équilibré
       - Pas de prétraitement majeur nécessaire
       - Features pertinentes pour la classification
    
    2. **Performance des Modèles:**
       - Excellente performance globale (>95% d'accuracy généralement)
       - KNN avec k=3-5 donne d'excellents résultats
       - La normalisation améliore légèrement les performances
    
    3. **Applicabilité:**
       - Ce type de modèle peut être déployé en production
       - Peut servir de système d'aide à l'identification botanique
       - Extensible à d'autres espèces avec plus de données
    
    #### 🎯 Recommandations:
    
    1. Pour un déploiement en production, considérer:
       - Cross-validation plus robuste (k-fold)
       - Ensemble methods (Random Forest, Gradient Boosting)
       - Validation sur un dataset externe
    
    2. Pour améliorer le modèle:
       - Collecter plus de données sur les espèces qui se chevauchent
       - Ajouter d'autres features morphologiques
       - Tester des modèles deep learning si le dataset s'agrandit
    
    3. Pour l'utilisation:
       - Créer une API REST pour les prédictions
       - Développer une application mobile pour la reconnaissance sur le terrain
       - Intégrer dans un système de gestion de biodiversité
    """)
    
    # Section 5: Références
    st.markdown("---")
    st.markdown("### 5️⃣ Références")
    
    st.markdown("""
    - Fisher, R.A. (1936). The use of multiple measurements in taxonomic problems. 
      *Annals of Eugenics*, 7(2), 179-188.
    - Anderson, E. (1935). The irises of the Gaspe Peninsula. 
      *Bulletin of the American Iris Society*, 59, 2-5.
    - Documentation scikit-learn: https://scikit-learn.org/
    - Documentation Streamlit: https://docs.streamlit.io/
    """)
    
    # Téléchargement du rapport
    st.markdown("---")
    st.markdown("### 📥 Télécharger le Rapport")
    
    # Créer un rapport texte
    report_text = f"""
    RAPPORT D'ANALYSE - CLASSIFICATION DES FLEURS IRIS
    ==================================================
    
    Date: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}
    
    1. DATASET
    ----------
    - Observations: {df.shape[0]}
    - Variables: {df.shape[1]}
    - Classes: {df['Species'].nunique()}
    
    2. STATISTIQUES DESCRIPTIVES
    -----------------------------
    {df.describe().to_string()}
    
    3. DISTRIBUTION DES ESPÈCES
    ----------------------------
    {df['Species'].value_counts().to_string()}
    
    4. MATRICE DE CORRÉLATION
    --------------------------
    {df[['SepalLength', 'SepalWidth', 'PetalLength', 'PetalWidth']].corr().to_string()}
    
    5. CONCLUSIONS
    --------------
    - Dataset bien équilibré et de bonne qualité
    - Features pertinentes pour la classification
    - Excellente séparabilité des classes (surtout Setosa)
    - Modèles de ML performants (>95% accuracy)
    
    ---
    Rapport généré automatiquement par l'application Streamlit
    TP Iris - Université de Yaoundé 1
    """
    
    st.download_button(
        label="📄 Télécharger le Rapport (TXT)",
        data=report_text,
        file_name="rapport_iris_analysis.txt",
        mime="text/plain"
    )
    
    # Télécharger les données
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📊 Télécharger les Données (CSV)",
        data=csv,
        file_name="iris_dataset.csv",
        mime="text/csv"
    )

# Footer
st.markdown("""
<div style='text-align: center; color: gray; padding: 2rem;'>
    <p>🌸 <b>TP Iris - Classification ML</b> 🌸</p>
    <p>Réalisé par TCHUENTEU GUETCHUENG DAVID 20U2891</p>
    <p>sous la supervision de Stéphane C.K. TEKOUAB (PhD & Ing.)</p>
</div>
""", unsafe_allow_html=True)