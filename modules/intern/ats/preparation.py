"""
preparation.py
--------------
Fonctions pour NETTOYER et FILTRER les données avant les calculs.
"""

import pandas as pd
import geopandas as gpd


def preparer_communes(df_admin, deps, col_code="code", col_dep="dep"):
    """Garde les communes ("com") des départements choisis
    et crée la colonne du département (2 premiers caractères du code INSEE)."""
    communes = df_admin[df_admin["type"] == "com"].copy()
    communes[col_dep] = communes[col_code].str[:2]
    communes = communes[communes[col_dep].isin(deps)].copy()
    return communes


def preparer_casernes(df_casernes, zone):
    """Transforme les casernes en points et garde celles qui sont dans la zone."""
    casernes = df_casernes.copy()
    # certaines casernes n'ont pas de nom dans OSM
    if "name" not in casernes.columns:
        casernes["name"] = "Sans nom"
    casernes["name"] = casernes["name"].fillna("Sans nom")
    # les polygones deviennent des points
    casernes["geometry"] = casernes.geometry.centroid
    # je garde les casernes dans la zone
    casernes = casernes[casernes.within(zone)].copy()
    # je ne garde que le nom et la géométrie
    casernes = casernes[["name", "geometry"]]
    return casernes


def preparer_incendies(df_incendies, deps):
    """Remet les codes au bon format, garde les départements choisis
    et convertit la surface parcourue en hectares."""
    df = df_incendies.copy()
    df["Code INSEE"] = df["Code INSEE"].astype(str).str.zfill(5)
    df["dep"] = df["Département"].astype(str).str.zfill(2)
    df = df[df["dep"].isin(deps)].copy()
    df["surface_ha"] = pd.to_numeric(df["Surface parcourue (m2)"], errors="coerce") / 10000
    return df


def compter_incendies(df_incendies):
    """Nombre d'incendies par commune (code INSEE)."""
    nb = df_incendies.groupby("Code INSEE").size().reset_index(name="nb_incendies")
    return nb


def preparer_forets(df_ocsol, source, surface_min_ha):
    """Garde les polygones de forêt, retire les petits bosquets
    et donne un identifiant à chaque forêt."""
    # exo_19 indique la source de chaque polygone : "BD FORET" = forêt
    # .str.upper() met tout en majuscules, au cas où ("BD Foret", "BD FORET"...)
    forets = df_ocsol[df_ocsol["exo_19"].str.upper() == source].copy()
    forets["surface_ha"] = forets.geometry.area / 10000
    forets = forets[forets["surface_ha"] >= surface_min_ha].copy()
    forets["id_foret"] = range(len(forets))
    # "fid" est un nom réservé dans les GeoPackage : je le renomme pour pouvoir enregistrer
    if "fid" in forets.columns:
        forets = forets.rename(columns={"fid": "fid_origine"})
    return forets


def points_des_forets(forets):
    """Un point par forêt, toujours situé À L'INTÉRIEUR du polygone."""
    points = forets[["id_foret", "lib3_19", "surface_ha", "geometry"]].copy()
    points["geometry"] = forets.geometry.representative_point()
    return points
