"""
parametres.py
-------------
Tous les réglages de l'étude, au même endroit.
Si on veut changer une hypothèse (vitesse, détour...), on la change ICI
et tous les notebooks en tiennent compte.
"""

# ---- zone d'étude ----
DEPS_PACA = ["04", "05", "06", "13", "83", "84"]
MARGE_CASERNES_M = 20000      # on garde aussi les casernes à moins de 20 km de PACA

# ---- forêts ----
SOURCE_FORETS = "BD FORET"    # valeur de la colonne exo_19 qui désigne les forêts
SURFACE_MIN_HA = 1            # on ignore les forêts de moins de 1 hectare

# ---- conversion distance -> délai ----
COEF_DETOUR = 1.3             # la route est environ 1,3 fois plus longue que la ligne droite
VITESSE_KMH = 50              # vitesse moyenne d'un camion d'intervention

# ---- classes de délai ----
BORNES_DELAI = [0, 10, 20, 30, 10000]
NOMS_CLASSES_DELAI = ["Moins de 10 min", "10 à 20 min", "20 à 30 min", "Plus de 30 min"]

# ---- couleurs de la typologie des communes ----
COULEURS_TYPOLOGIE = {
    "Prioritaire": "#B2182B",              # rouge profond : les deux risques à la fois
    "Exposée mais desservie": "#F4A261",   # orange doux : beaucoup de feux
    "Éloignée, peu de feux": "#F7E08C",    # violet : délai long
    "Faible enjeu": "#E3DED6",             # gris beige : presque neutre
    "Pas de forêt": "#FFFFFF"
}

# ---- noms des fichiers de données ----
FICHIER_COMMUNES = "entites-administratives.shp"
FICHIER_FORETS = "occupation-du-sol-region-sud-2019Polygon.shp"
FICHIER_INCENDIES = "Incendies.csv"
FICHIER_CASERNES = "casernes_osm.geojson"

# ---- colonnes de la couche communes ----
COL_CODE = "code"   # code INSEE de la commune
COL_NOM = "nom"     # nom de la commune
COL_DEP = "dep"     # code du département (créé pendant la préparation)


# adresse publique du fichier lourd (stockage SSP Cloud)
URL_FORETS = "https://minio.lab.sspcloud.fr/khcoulibaly/diffusion/occupation_du_sol.zip"



# Palette de couleurs. C'est pour avoir une jolie palette pour les délai
import matplotlib
from matplotlib.colors import LinearSegmentedColormap

# palette des délais : de crème (court) à rouge brique (long)
palette_braise = LinearSegmentedColormap.from_list(
    "braise",
    ["#FFF4D6", "#FDCB8A", "#F58B4C", "#D9480F", "#8A1C0B"]
)

# j'enregistre la palette dans matplotlib pour pouvoir l'appeler par son nom
# (le "if" évite une erreur si le module est rechargé et la palette existe déjà)
if "braise" not in matplotlib.colormaps:
    matplotlib.colormaps.register(palette_braise)

PALETTE_DELAI = "braise"