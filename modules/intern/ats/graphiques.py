"""
graphiques.py
-------------
Fonctions pour les TABLEAUX mis en forme, les GRAPHIQUES et les CARTES STATIQUES.
Chaque fonction peut enregistrer son résultat avec le paramètre "fichier".
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


def joli_tableau(tableau, titre, couleurs="Reds", colonnes=None, decimales=1):
    """Met en forme un tableau : décimales, séparateur de milliers, dégradé de couleur.
    - colonnes : les colonnes à colorer (toutes si None)"""
    format_nombres = "{:,." + str(decimales) + "f}"
    return (tableau.style
            .format(format_nombres, subset=tableau.select_dtypes("number").columns)
            .background_gradient(cmap=couleurs, subset=colonnes)
            .set_caption(titre))


def enregistrer(fichier):
    """Enregistre la figure en cours (si un nom de fichier est donné) puis l'affiche."""
    if fichier is not None:
        plt.savefig(fichier, dpi=300, bbox_inches="tight")
    plt.show()


def barres(serie, titre, xlabel, ylabel, couleur="#c0392b", horizontal=False, fichier=None):
    """Diagramme en barres à partir d'une série (index = catégories, valeurs = hauteurs)."""
    fig, ax = plt.subplots(figsize=(8, 4.5))
    if horizontal:
        ax.barh(serie.index.astype(str), serie.values, color=couleur)
        ax.invert_yaxis()   # la plus grande valeur en haut
    else:
        ax.bar(serie.index.astype(str), serie.values, color=couleur)
    ax.set_title(titre)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    enregistrer(fichier)


def histogramme(valeurs, titre, xlabel, ylabel, couleur="#c0392b", log=False, mediane=False, fichier=None):
    """Histogramme. log=True pour une échelle logarithmique, mediane=True pour tracer la médiane."""
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.hist(valeurs, bins=40, color=couleur, edgecolor="white", log=log)
    if mediane:
        ax.axvline(valeurs.median(), color="black", linestyle="--", label="Médiane")
        ax.legend()
    ax.set_title(titre)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    enregistrer(fichier)


def nuage_de_points(x, y, titre, xlabel, ylabel, seuil_x=None, seuil_y=None, fichier=None):
    """Nuage de points, avec en option des lignes pointillées pour les seuils."""
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(x, y, alpha=0.5, color="#2c3e50")
    if seuil_x is not None:
        ax.axvline(seuil_x, color="grey", linestyle=":")
    if seuil_y is not None:
        ax.axhline(seuil_y, color="grey", linestyle=":")
    ax.set_title(titre)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    enregistrer(fichier)


def carte_choroplethe(gdf, colonne, titre, titre_legende, couleurs="YlOrRd",
                      methode="quantiles", points=None, fichier=None):
    """Carte où chaque polygone est coloré selon la valeur d'une colonne.
    - methode : "quantiles", "natural_breaks"... (découpage en 5 classes)
    - points : une couche de points à ajouter par-dessus (par exemple les casernes)"""
    fig, ax = plt.subplots(figsize=(10, 9))
    gdf.plot(
        ax=ax,
        column=colonne,
        cmap=couleurs,
        scheme=methode,
        k=5,
        legend=True,
        edgecolor="grey",
        linewidth=0.2,
        missing_kwds={"color": "whitesmoke", "label": "Pas de donnée"},
        legend_kwds={"title": titre_legende, "loc": "upper left", "fmt": "{:.0f}"}
    )
    if points is not None:
        points.plot(ax=ax, color="black", markersize=4)
    ax.set_title(titre, fontsize=14)
    ax.set_axis_off()
    enregistrer(fichier)


def carte_categories(gdf, colonne, couleurs, titre, titre_legende, fichier=None):
    """Carte où chaque polygone est coloré selon sa catégorie.
    - couleurs : un dictionnaire {catégorie: couleur}"""
    fig, ax = plt.subplots(figsize=(10, 9))
    legende = []
    for categorie, couleur in couleurs.items():
        sous_ensemble = gdf[gdf[colonne] == categorie]
        if len(sous_ensemble) > 0:
            sous_ensemble.plot(ax=ax, color=couleur, edgecolor="grey", linewidth=0.2)
        legende.append(mpatches.Patch(facecolor=couleur, edgecolor="grey", label=categorie))
    ax.legend(handles=legende, loc="upper left", title=titre_legende)
    ax.set_title(titre, fontsize=14)
    ax.set_axis_off()
    enregistrer(fichier)


def carte_forets_casernes(communes, forets, casernes, fichier=None):
    """Carte de situation : contours des communes, forêts en vert, casernes en rouge."""
    fig, ax = plt.subplots(figsize=(10, 9))
    communes.plot(ax=ax, color="white", edgecolor="lightgrey", linewidth=0.3)
    forets.plot(ax=ax, color="forestgreen", alpha=0.7)
    casernes.plot(ax=ax, color="red", markersize=10)
    legende = [
        mpatches.Patch(color="forestgreen", label="Forêts"),
        plt.Line2D([], [], marker="o", color="red", linestyle="", label="Casernes")
    ]
    ax.legend(handles=legende, loc="upper left")
    ax.set_title("Forêts et casernes de sapeurs-pompiers en PACA", fontsize=14)
    ax.set_axis_off()
    enregistrer(fichier)
