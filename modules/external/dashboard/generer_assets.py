"""
generer_assets.py
-----------------
Met à jour les images et les cartes du dashboard À PARTIR DES NOTEBOOKS.

Le script ouvre les notebooks du projet, retrouve les cellules qui produisent
nos graphiques et nos cartes (grâce à un petit texte présent dans leur code),
puis enregistre leurs sorties dans img/ (graphiques PNG) et cartes/ (cartes Folium).

Utilisation, depuis la racine du projet :
    python modules/external/dashboard/generer_assets.py

À relancer après avoir réexécuté un notebook dont les résultats ont changé.
"""

import base64
import html
import json
import os
import re

# ---------- dossiers ----------
DOSSIER_DASHBOARD = os.path.dirname(os.path.abspath(__file__))
RACINE_PROJET = os.path.abspath(os.path.join(DOSSIER_DASHBOARD, "..", "..", ".."))
DOSSIER_IMG = os.path.join(DOSSIER_DASHBOARD, "img")
DOSSIER_CARTES = os.path.join(DOSSIER_DASHBOARD, "cartes")

# ---------- fond des cartes Folium ----------
# "original" : garde le fond utilisé dans les notebooks (Carto, avec la clé API)
# "esri"     : remplace les fonds Carto par un fond gris clair gratuit et sans clé
FOND = "esri"

FOND_SANS_CLE = "https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}"
ATTRIBUTION_FOND = "Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ"

# ---------- ce qu'on extrait ----------
# (notebook, texte présent dans le code de la cellule, type de sortie, nom du fichier créé)
SORTIES = [
    # Partie 1 : interface habitat-forêt
    ("main/ihf/01_data_visualization.ipynb", "plot.plot_ban_data(df_gen)", "png", "ihf_adresses_paca.png"),
    ("main/ihf/01_data_visualization.ipynb", "plot_bdf.plot_bd_forests_data(gdf_forest)", "png", "ihf_forets.png"),
    ("main/ihf/02_data_analysis.ipynb", "Distance to forest edge by settlement type", "png", "ihf_bandes_typologie.png"),
    ("main/ihf/02_data_analysis.ipynb", "violinplot", "png", "ihf_score_departements.png"),
    ("main/ihf/02_data_analysis.ipynb", "CELL = 500", "html", "ihf_grille_ihf.html"),
    ("main/ihf/02_data_analysis.ipynb", 'nom_commune == "Allons"', "html", "ihf_exemple_allons.html"),
    ("main/ihf/02_data_analysis.ipynb", "HeatMap(", "html", "ihf_zones_ombre.html"),
    # Partie 2 : accessibilité et temps de secours
    ("main/ats/01_preparation_exploration.ipynb", "incendies_par_annee", "png", "ats_incendies_annee.png"),
    ("main/ats/01_preparation_exploration.ipynb", "incendies_causes", "png", "ats_causes.png"),
    ("main/ats/01_preparation_exploration.ipynb", "casernes_par_departement", "png", "ats_casernes_departement.png"),
    ("main/ats/03_resultats_cartes.ipynb", "histogramme_delais", "png", "ats_histogramme_delais.png"),
    ("main/ats/03_resultats_cartes.ipynb", "nuage_incendies_delai", "png", "ats_nuage_incendies_delai.png"),
    ("main/ats/03_resultats_cartes.ipynb", "carte1_forets_casernes", "png", "ats_carte_forets_casernes.png"),
    ("main/ats/03_resultats_cartes.ipynb", "carte2_delai_moyen", "png", "ats_carte_delai.png"),
    ("main/ats/03_resultats_cartes.ipynb", "carte4_typologie", "png", "ats_carte_typologie.png"),
    ("main/ats/03_resultats_cartes.ipynb", "carte_delais(", "html", "ats_delais.html"),
    ("main/ats/03_resultats_cartes.ipynb", "carte_typologie(", "html", "ats_typologie.html"),
]


def lire_notebook(chemin):
    """Un notebook est un fichier JSON : je le lis comme un dictionnaire."""
    with open(chemin, encoding="utf-8") as f:
        return json.load(f)


def trouver_cellule(notebook, marqueur):
    """Renvoie la première cellule de code dont le code contient le marqueur."""
    for cellule in notebook["cells"]:
        if cellule["cell_type"] == "code" and marqueur in "".join(cellule["source"]):
            return cellule
    return None


def extraire_png(cellule):
    """Renvoie l'image PNG (en octets) produite par la cellule, ou None."""
    for sortie in cellule.get("outputs", []):
        donnees = sortie.get("data", {})
        if "image/png" in donnees:
            return base64.b64decode(donnees["image/png"])
    return None


def extraire_carte(cellule):
    """Renvoie la page HTML complète de la carte Folium affichée par la cellule, ou None.
    Dans le notebook, la carte est cachée dans l'attribut srcdoc d'une <iframe>."""
    for sortie in cellule.get("outputs", []):
        donnees = sortie.get("data", {})
        if "text/html" in donnees:
            texte = "".join(donnees["text/html"])
            resultat = re.search(r'srcdoc="(.*?)"', texte, re.S)
            if resultat:
                return html.unescape(resultat.group(1))
    return None


def nettoyer_carte(page):
    """Remplace les fonds de carte qui demandent une clé API par un fond gratuit,
    pour ne jamais publier de clé et pour que la carte s'affiche partout."""
    page = re.sub(r'https://basemaps\.cartocdn\.com/[^"\']*', FOND_SANS_CLE, page)
    page = re.sub(r'(&copy;|©) ?CARTO', ATTRIBUTION_FOND, page)
    return page


def remplacer_osm(page):
    """Les serveurs d'OpenStreetMap refusent les cartes ouvertes depuis un fichier local
    (erreur 403 « Access blocked »). Je remplace donc leurs tuiles par le fond Esri, gratuit et sans clé."""
    page = re.sub(r'https://(\{s\}\.)?tile\.openstreetmap\.org/\{z\}/\{x\}/\{y\}\.png', FOND_SANS_CLE, page)
    return page


def main():
    os.makedirs(DOSSIER_IMG, exist_ok=True)
    os.makedirs(DOSSIER_CARTES, exist_ok=True)
    notebooks = {}

    for chemin_nb, marqueur, type_sortie, nom_fichier in SORTIES:
        chemin_complet = os.path.join(RACINE_PROJET, chemin_nb)
        if chemin_complet not in notebooks:
            notebooks[chemin_complet] = lire_notebook(chemin_complet)

        cellule = trouver_cellule(notebooks[chemin_complet], marqueur)
        if cellule is None:
            print("Cellule introuvable :", chemin_nb, "→", marqueur)
            continue

        if type_sortie == "png":
            image = extraire_png(cellule)
            if image is None:
                print("Pas d'image (relancer le notebook ?) :", nom_fichier)
                continue
            with open(os.path.join(DOSSIER_IMG, nom_fichier), "wb") as f:
                f.write(image)
        else:
            page = extraire_carte(cellule)
            if page is None:
                print("Pas de carte (relancer le notebook ?) :", nom_fichier)
                continue
            page = remplacer_osm(page)
            if FOND == "esri":
                page = nettoyer_carte(page)
            with open(os.path.join(DOSSIER_CARTES, nom_fichier), "w", encoding="utf-8") as f:
                f.write(page)

        print("OK :", nom_fichier)


if __name__ == "__main__":
    main()
