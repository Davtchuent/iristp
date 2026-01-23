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
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# FONCTIONS UTILITAIRES
# ============================================================================

@st.cache_data
def load_data():
    """Charge et prépare les données Iris"""
    df = pd.read_csv('iris.csv', sep=';')
    df = df.rename(columns={'Species': 'species'})
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
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
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