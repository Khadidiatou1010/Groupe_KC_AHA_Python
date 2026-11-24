"""
chargement.py
-------------
Fonctions pour TROUVER et LIRE les fichiers de données.
"""

import os
import pandas as pd
import geopandas as gpd
import urllib.request
import zipfile



def trouver_dossier(nom_dossier):
    """Cherche un dossier (par exemple "Data") en remontant de 0 à 3 niveaux.
    Renvoie son chemin, ou None s'il est introuvable."""
    for essai in [".", "..", "../..", "../../.."]:
        chemin = os.path.join(essai, nom_dossier)
        if os.path.exists(chemin):
            return chemin
    print("ATTENTION : dossier introuvable :", nom_dossier)
    return None


def trouver_fichier(nom_fichier, dossier_donnees):
    """Cherche un fichier dans le dossier de données et tous ses sous-dossiers."""
    for racine, sous_dossiers, fichiers in os.walk(dossier_donnees):
        if nom_fichier in fichiers:
            return os.path.join(racine, nom_fichier)
    print("ATTENTION : fichier introuvable :", nom_fichier)
    return None


def charger_couche(chemin, encodage=None, filtre=None):
    """Lit un fichier géographique (shp, gpkg, geojson) et le met en Lambert-93.
    - encodage : par exemple "utf-8" pour bien lire les accents
    - filtre : une condition SQL, par exemple "niv1_19 = 3", pour ne lire qu'une partie"""
    gdf = gpd.read_file(chemin, encoding=encodage, where=filtre)
    gdf = gdf.to_crs(epsg=2154)
    return gdf


def charger_incendies(chemin):
    """Lit le CSV de la BDIFF.
    Le fichier a 3 lignes de titre avant le tableau (skiprows=3).
    Les codes sont lus en texte pour garder les zéros (04112, 2A092...)."""
    df = pd.read_csv(
        chemin,
        sep=";",
        encoding="utf-8",
        skiprows=3,
        dtype={"Code INSEE": str, "Département": str}
    )
    return df


def apercu(df, nom):
    """Affiche un résumé rapide d'une table : taille, colonnes, valeurs manquantes."""
    print("=====", nom, "=====")
    print("Lignes :", df.shape[0], "| Colonnes :", df.shape[1])
    print("Colonnes :", list(df.columns))
    manquants = df.isna().sum()
    manquants = manquants[manquants > 0].sort_values(ascending=False)
    if len(manquants) > 0:
        print("Valeurs manquantes :")
        print(manquants.head(10))
    else:
        print("Aucune valeur manquante")
    print()


def telecharger_et_dezipper(url, dossier_destination, fichier_attendu):
    """Télécharge un zip et le décompresse, SEULEMENT si le fichier attendu n'est pas déjà là."""
    chemin_attendu = os.path.join(dossier_destination, fichier_attendu)
    if os.path.exists(chemin_attendu):
        return chemin_attendu
    print("Téléchargement de", url)
    os.makedirs(dossier_destination, exist_ok=True)
    chemin_zip = os.path.join(dossier_destination, "telechargement.zip")
    urllib.request.urlretrieve(url, chemin_zip)
    with zipfile.ZipFile(chemin_zip) as z:
        z.extractall(dossier_destination)
    os.remove(chemin_zip)      # je supprime le zip, je garde les fichiers décompressés
    return chemin_attendu