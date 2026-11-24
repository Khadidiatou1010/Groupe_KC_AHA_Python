# Incendies de forêt en Provence-Alpes-Côte d'Azur

## I. Introduction

### Contexte

Chaque été, les images reviennent : des collines en flammes, des routes coupées, des habitants évacués à quelques kilomètres de la mer. En France, la région **Provence-Alpes-Côte d’Azur (PACA)** est l’une des plus exposées aux feux de forêt. Rien d’étonnant : tous les ingrédients y sont réunis.

La forêt et la garrigue couvrent une grande partie du territoire, des pins d’Alep du littoral aux mélèzes des Alpes. Le climat méditerranéen y impose des étés chauds et secs, souvent balayés par le Mistral. Et le **changement climatique** aggrave la situation : il allonge la saison des feux, assèche la végétation et rend les départs de feu plus fréquents et plus difficiles à maîtriser.

À ce risque naturel s’ajoute une forte pression humaine. Plus de cinq millions d’habitants, une urbanisation qui grignote les lisières des massifs et l’une des premières destinations touristiques de France : la population est nombreuse là où la forêt est la plus inflammable. Or, la grande majorité des feux sont d’origine humaine (imprudences, travaux, mégots, malveillance). Entre 2016 et 2025, la base nationale BDIFF recense ainsi **près de 6 000 feux de forêt en PACA**, qui ont parcouru **près de 35 000 hectares**.

Deux questions deviennent alors essentielles pour protéger les populations : **quelles habitations vivent au contact direct de la forêt ?** Et **les secours peuvent-ils atteindre rapidement les forêts quand un feu se déclare ?**

### Objectif et démarche

C'est ainsi que dans le cadre de notre projet Python, nous nous intéressons donc à **l’exposition au risque d’incendie de forêt en PACA**, en croisant trois dimensions : **la forêt**, **l’habitat** et **les secours**. Le travail se fait en deux parties.

**Partie 1. L’interface habitat-forêt**

Cette partie identifie les habitations situées au contact de la forêt, ce qu’on appelle l’**interface habitat-forêt**, là où un feu menace le plus directement les personnes et les biens. Pour chaque adresse de la Base Adresse Nationale, nous mesurons la distance à la lisière forestière la plus proche, puis nous classons les habitations en cinq bandes : *dans la forêt*, *à moins de 50 m*, *de 50 à 100 m*, *de 100 à 200 m* et *au-delà de 200 m*. Un regroupement spatial des adresses distingue ensuite l’habitat **isolé**, **groupé** et **dense**, car une maison isolée en lisière est bien plus difficile à protéger qu’un quartier compact.

Ces mesures sont combinées dans un **score d’exposition** compris entre 0 et 1, qui pondère à parts égales la proximité de la forêt (1 pour une habitation en forêt, puis une valeur qui décroît jusqu’à 0 à 200 m de la lisière) et la part de forêt dans un rayon de 100 m autour de l’habitation. Le score est ensuite agrégé par commune et confronté à l’historique des incendies (tests statistiques et modèle de comptage). Une carte de chaleur met enfin en évidence les « zones d’ombre » de la région : les secteurs où l’habitat est à la fois isolé et fortement exposé.

**Partie 2. L’accessibilité des secours** 

Cette partie se demande si les sapeurs-pompiers peuvent atteindre rapidement les forêts de la région. Pour chacune des forêts de la région PACA, nous identifions la caserne la plus proche et estimons un **délai théorique d’intervention**, à partir de la distance à vol d’oiseau corrigée d’un coefficient de détour et d’une vitesse moyenne. Ces délais sont ensuite agrégés par commune et croisés avec l’historique des incendies, pour repérer les **communes prioritaires** : celles qui cumulent beaucoup de feux et un accès plus long.

Les données mobilisées pour ces deux analyses sont présentées dans la section suivante.


## II. Les données utilisées

| Base | Producteur | Description | Format | Variables utilisées | Lien | Pourquoi on l'utilise |
|---|---|---|---|---|---|---|
| Entités administratives | Datasud | Contours des communes et départements de PACA (1 005 entités, Lambert-93) | Shapefile | `type`, `code`, `nom` | https://www.datasud.fr/explorer/en/jeux-de-donnees/entites-administratives-de-la-region-sud/telechargements | Unité d'analyse : rattacher forêts et incendies aux communes, cartographier | 
| Occupation du sol 2019 (région Sud) | à compléter | Occupation du sol de PACA en 3 niveaux de nomenclature (277 512 polygones) | Shapefile | `niv1_19`, `lib3_19`, `exo_19` | https://www.datasud.fr/explorer/en/jeux-de-donnees/occupation-sol-region-sud-2019-1-3/info | Visualiser et localiser les forêts (`exo_19 = "BD FORET"`) |
| BDIFF (Base de Données sur les Incendies de Forêts en France) | Ministère de l'Agriculture | Feux de forêt 2016-2025, France entière (27 444 feux) : date, commune, surfaces, cause | CSV | `Code INSEE`, `Département`, `Année`, `Surface parcourue (m2)`, `Nature` | https://bdiff.agriculture.gouv.fr/incendies | Nombre d'incendies par commune, surfaces brûlées, causes | 
| Casernes de pompiers (OpenStreetMap) | Contributeurs OSM | Casernes sélectionnées avec le filtre `amenity=fire_station` dans un rectangle autour de PACA.  | GeoJSON | `name`, géométrie | https://overpass-turbo.eu | Points de départ des secours pour calculer les délais 
| Base Adresse Nationale (par département) | Données publiques | Adresses géolocalisées des 6 départements de PACA | CSV | longitude, latitude, communes | https://adresse.data.gouv.fr | Interface forêt habitât |



## III. Structure du dépôt

```
Groupe_KC_AHA_Python/
│
├── README.md                          ← ce fichier
├── requirements.txt                   ← bibliothèques Python à installer
├── notebook_principal.ipynb           ← synthèse de l’étude (à lire en premier)
│
├── data/                              ← données brutes
│   ├── communes/                      ← entités administratives de PACA (shapefile)
│   ├── fires/                         ← incendies de forêt BDIFF 2016-2025 (CSV) + documentation
│   ├── help_centers/                  ← casernes de pompiers OpenStreetMap (GeoJSON)
│   ├── paca_adress/                   ← Base Adresse Nationale, un CSV par département
│   └── forests/                       ← occupation du sol 2019, téléchargée automatiquement (non versionnée)
│
├── main/                              ← notebooks d’analyse
│   ├── ihf/                           ← Partie 1 : interface habitat-forêt
│   │   ├── 01_data_visualization.ipynb
│   │   └── 02_data_analysis.ipynb
│   └── ats/                           ← Partie 2 : accessibilité et temps de secours
│       ├── 01_preparation_exploration.ipynb
│       ├── 02_calcul_delais.ipynb
│       └── 03_resultats_cartes.ipynb
│
└── modules/                           ← fonctions réutilisables, appelées par les notebooks
    └── intern/
        ├── ihf/                       ← Partie 1
        │   ├── utils.py
        │   ├── analysis/utilities.py
        │   ├── ban/                   ← lecture et cartes des adresses (extract.py, plot.py)
        │   └── bd_forests/            ← lecture et cartes des forêts (extract.py, plot.py)
        └── ats/                       ← Partie 2
            ├── parametres.py          ← réglages de l’étude (vitesse, détour, couleurs…)
            ├── chargement.py          ← trouver, télécharger et lire les fichiers
            ├── preparation.py         ← filtrer et nettoyer les données
            ├── calculs.py             ← caserne la plus proche, délais, typologie
            ├── graphiques.py          ← tableaux, graphiques et cartes statiques
            └── cartes_interactives.py ← cartes Folium
```

**Principe :** les notebooks racontent l’analyse étape par étape, avec un code court. Le code technique (lecture des fichiers, calculs, cartes) est rangé dans des **modules** du dossier `modules/`. Les notebooks restent ainsi lisibles, et une même fonction peut servir plusieurs fois sans copier-coller.

**NB :** Le fichier d’occupation du sol est trop lourd pour GitHub (plus de 100 Mo). Il est hébergé sur le stockage public de SSP Cloud et **se télécharge automatiquement** dans `data/forests/` au premier lancement.


## V. Cadre du projet

Ce travail a été réalisé dans le cadre du cours de **Python pour la data science** à l’**ENSAE Paris**, année universitaire 2026-2027.

| | |
|---|---|
| **Étudiants** | Khadidiatou Coulibaly · Abdou Hamid Alagbe |
| **Supervision** | M. Daniel Marin |
| **Outils** | Python (pandas, geopandas, matplotlib, folium, contextily), SSP Cloud, GitHub |


