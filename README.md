# Les données utilisées 

| Base | Producteur | Description | Format | Variables utilisées | Lien | Pourquoi on l'utilise | Utilisée ? |
|---|---|---|---|---|---|---|---|
| Entités administratives | à compléter | Contours des communes et départements de PACA (1 005 entités, Lambert-93) | Shapefile | `type`, `code`, `nom` | à compléter | Unité d'analyse : rattacher forêts et incendies aux communes, cartographier | 
| Occupation du sol 2019 (région Sud) | à compléter | Occupation du sol de PACA en 3 niveaux de nomenclature (277 512 polygones) | Shapefile | `niv1_19`, `lib3_19`, `exo_19` | https://www.datasud.fr/explorer/en/jeux-de-donnees/occupation-sol-region-sud-2019-1-3/info | Visualiser et localiser les forêts (`exo_19 = "BD FORET"`) |
| BDIFF (Base de Données sur les Incendies de Forêts en France) | Ministère de l'Agriculture | Feux de forêt 2016-2025, France entière (27 444 feux) : date, commune, surfaces, cause | CSV | `Code INSEE`, `Département`, `Année`, `Surface parcourue (m2)`, `Nature` | https://bdiff.agriculture.gouv.fr | Nombre d'incendies par commune, surfaces brûlées, causes | 
| Casernes de pompiers (OpenStreetMap) | Contributeurs OSM | Casernes `amenity=fire_station` dans un rectangle autour de PACA | GeoJSON | `name`, géométrie | https://overpass-turbo.eu | Points de départ des secours pour calculer les délais 
| Base Adresse Nationale (par département) | à compléter | Adresses géolocalisées des 6 départements de PACA | CSV | — | https://adresse.data.gouv.fr | Non utilisée dans cette analyse |