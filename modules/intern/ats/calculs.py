"""
calculs.py
----------
Fonctions du COEUR de l'analyse : caserne la plus proche, délais,
agrégation par commune et typologie.
"""

import pandas as pd
import geopandas as gpd


def caserne_plus_proche(points_forets, casernes):
    """Pour chaque forêt, trouve la caserne la plus proche et la distance (en mètres)."""
    casernes_simple = casernes.rename(columns={"name": "nom_caserne"})
    resultat = gpd.sjoin_nearest(
        points_forets,
        casernes_simple,
        how="left",
        distance_col="distance_m"
    )
    # en cas d'égalité, une forêt peut apparaître 2 fois : je garde la première
    resultat = resultat.drop_duplicates(subset="id_foret")
    resultat = resultat.drop(columns="index_right")
    return resultat


def distance_vers_delai(resultat, coef_detour, vitesse_kmh):
    """Ajoute la distance en km et le délai théorique en minutes.
    délai (min) = distance (km) x détour / vitesse (km/h) x 60"""
    resultat = resultat.copy()
    resultat["distance_km"] = resultat["distance_m"] / 1000
    resultat["delai_min"] = resultat["distance_km"] * coef_detour / vitesse_kmh * 60
    return resultat


def rattacher_aux_communes(resultat, communes, col_code="code", col_nom="nom", col_dep="dep"):
    """Ajoute à chaque forêt la commune dans laquelle elle se trouve.
    Les forêts hors de la zone disparaissent (how="inner")."""
    communes_simple = communes[[col_code, col_nom, col_dep, "geometry"]]
    forets_communes = gpd.sjoin(resultat, communes_simple, how="inner", predicate="within")
    forets_communes = forets_communes.drop(columns="index_right")
    return forets_communes


def statistiques_par_commune(forets_communes, communes, nb_incendies, col_code="code"):
    """Calcule les indicateurs par commune et ajoute le nombre d'incendies."""
    stats = forets_communes.groupby(col_code).agg(
        nb_forets=("id_foret", "count"),
        surface_foret_ha=("surface_ha", "sum"),
        delai_moyen=("delai_min", "mean"),
        delai_max=("delai_min", "max")
    ).reset_index()

    carte = communes.merge(stats, on=col_code, how="left")
    carte = carte.merge(nb_incendies, left_on=col_code, right_on="Code INSEE", how="left")
    carte = carte.drop(columns="Code INSEE")
    # une commune absente de la BDIFF n'a eu aucun incendie enregistré
    carte["nb_incendies"] = carte["nb_incendies"].fillna(0)
    return carte


def classer_delais(forets_communes, bornes, noms_classes):
    """Ajoute une colonne avec la classe de délai de chaque forêt."""
    forets_communes = forets_communes.copy()
    forets_communes["classe_delai"] = pd.cut(forets_communes["delai_min"], bins=bornes, labels=noms_classes)
    return forets_communes


def typologie_communes(carte):
    """Classe chaque commune selon son nombre d'incendies et son délai moyen.
    Les seuils sont les médianes, calculées sur les communes qui ont des forêts.
    Renvoie la carte avec la colonne "typologie", et les deux seuils."""
    avec_foret = carte[carte["nb_forets"] > 0]
    seuil_incendies = avec_foret["nb_incendies"].median()
    seuil_delai = avec_foret["delai_moyen"].median()

    def classer(ligne):
        if pd.isna(ligne["delai_moyen"]):
            return "Pas de forêt"
        beaucoup_feux = ligne["nb_incendies"] > seuil_incendies
        delai_long = ligne["delai_moyen"] > seuil_delai
        if beaucoup_feux and delai_long:
            return "Prioritaire"
        elif beaucoup_feux:
            return "Exposée mais desservie"
        elif delai_long:
            return "Éloignée, peu de feux"
        else:
            return "Faible enjeu"

    carte = carte.copy()
    carte["typologie"] = carte.apply(classer, axis=1)
    return carte, seuil_incendies, seuil_delai
