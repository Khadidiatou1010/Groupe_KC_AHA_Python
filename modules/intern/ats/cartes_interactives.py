"""
cartes_interactives.py
----------------------
Fonctions pour les cartes FOLIUM (zoom, survol, couches qu'on peut cocher/décocher).
"""

import folium


def preparer_pour_folium(gdf, tolerance_m=100):
    """Simplifie les contours (pour alléger la carte) puis passe en latitude/longitude,
    le système de coordonnées qu'utilise Folium (EPSG:4326)."""
    gdf = gdf.copy()
    gdf["geometry"] = gdf.geometry.simplify(tolerance_m)
    gdf = gdf.to_crs(epsg=4326)
    return gdf


def ajouter_points(carte, points, nom_couche, couleur, rayon=3, infobulle=None, alias=None):
    """Ajoute une couche de points sur une carte Folium existante.
    - infobulle : liste des colonnes affichées au survol
    - alias : les jolis noms de ces colonnes"""
    options_infobulle = {}
    if alias is not None:
        options_infobulle = {"aliases": alias}
    points.to_crs(epsg=4326).explore(
        m=carte,
        color=couleur,
        marker_type="circle_marker",
        marker_kwds={"radius": rayon, "weight": 1, "fillOpacity": 0.9},
        tooltip=infobulle,
        tooltip_kwds=options_infobulle,
        name=nom_couche
    )


def ajouter_menu_couches(carte):
    """Ajoute le menu en haut à droite pour cocher/décocher chaque couche.
    collapsed=False : le menu reste toujours ouvert (plus facile pendant une présentation)."""
    folium.LayerControl(collapsed=False).add_to(carte)


def carte_delais(communes_web, casernes, forets_loin, col_nom="nom", palette="YlOrRd", fichier=None):
    """Carte interactive : délai moyen par commune + casernes + forêts les plus éloignées."""
    carte = communes_web.explore(
        column="delai_moyen",
        cmap=palette,
        scheme="quantiles",
        k=5,
        tooltip=[col_nom, "nb_incendies", "nb_forets", "delai_moyen", "typologie"],
        tooltip_kwds={"aliases": ["Commune", "Incendies", "Forêts", "Délai moyen (min)", "Typologie"]},
        style_kwds={"weight": 0.3, "color": "grey", "fillOpacity": 0.9},
        missing_kwds={"color": "lightgrey"},
        legend_kwds={"caption": "Délai moyen (min)"},
        tiles="OpenStreetMap",
        name="Délai moyen par commune"
    )
    ajouter_points(carte, casernes, "Casernes", "#1D3557", rayon=2, infobulle=["name"], alias=["Caserne"])
    ajouter_points(
        carte, forets_loin, "Forêts les plus éloignées", "darkgreen", rayon=5,
        infobulle=[col_nom, "delai_min", "surface_ha", "nom_caserne"],
        alias=["Commune", "Délai (min)", "Surface (ha)", "Caserne la plus proche"]
    )
    ajouter_menu_couches(carte)
    if fichier is not None:
        carte.save(fichier)
    return carte


def carte_typologie(communes_web, casernes, couleurs, col_nom="nom", fichier=None):
    """Carte interactive de la typologie des communes, avec les casernes."""
    carte = communes_web.explore(
        column="typologie",
        categorical=True,
        categories=list(couleurs.keys()),
        cmap=list(couleurs.values()),
        tooltip=[col_nom, "nb_incendies", "delai_moyen", "typologie"],
        tooltip_kwds={"aliases": ["Commune", "Incendies", "Délai moyen (min)", "Typologie"]},
        style_kwds={"weight": 0.3, "color": "grey", "fillOpacity": 0.9},
        legend_kwds={"caption": "Typologie"},
        tiles="OpenStreetMap",
        name="Typologie des communes"
    )
    ajouter_points(carte, casernes, "Casernes", "#1D3557", rayon=2, infobulle=["name"], alias=["Caserne"])
    ajouter_menu_couches(carte)
    if fichier is not None:
        carte.save(fichier)
    return carte
