# NebuleAir Pro — fichiers 3D

Le NebuleAir Pro est construit sur un **boîtier étanche du commerce Takachi**. Les pièces imprimées en 3D (aérations AirVent, attaches des cartes et des sondes, supports) viennent s'y fixer.

Deux tailles de boîtier existent, selon les sondes embarquées :

| Version | Boîtier Takachi | Montage | Sondes |
|---|---|---|---|
| **Petite** | **WP13-18-5G** | vertical | 1 capteur de particules NextPM + sonde BME280 externe (température, humidité, pression) |
| **Grande** | **WP15-21-6G** | horizontal | NextPM + BME280, avec la place pour **2 sondes gaz** supplémentaires : 2 Alphasense **ou** 2 Envea Cairsens |

### WP13-18-5G en bref

- Dimensions extérieures : **130 × 175 × 45 mm** (fond 33 mm + couvercle 12 mm), angles R20
- Étanchéité **IP68** (immersion 1 m pendant 24 h)
- « G » = gris clair, en **ASA anti-UV** (-20 °C à +60 °C)
- Couvercle fixé par 6 vis M2,5 posées par le dessous ; 8 plots M2.3 pour une carte ; 2 trous M4 pour la patte de fixation sur poteau

Source : plan public du fabricant, sur la fiche produit Takachi.

## Modèle simplifié du boîtier

`takachi_WP13-18-5G_simplifie_*` est un modèle **redessiné par AirCarto à partir des cotes publiques** du plan Takachi (forme extérieure, parois, plots, trous de vis). Il ne reprend pas le modèle 3D du fabricant. Il sert à la **visualisation** et à vérifier l'ajustement de nos pièces : ce n'est pas un fichier pour fabriquer le boîtier, qui s'achète chez Takachi.

- `…_corps_v1.stl` / `…_couvercle_v1.stl` : les deux pièces
- `…_v1.glb` : assemblage, pour la vue 3D du wiki

Généré par `scripts_3d/takachi_wp.py` (à la racine du dépôt) : modifier les cotes dans ce script puis le relancer, plutôt que d'éditer les fichiers à la main.

## Organisation des fichiers

Un fichier par pièce, nommé `<piece>_<boîtier>_v<N>.<ext>`, par exemple `airvent_WP15-21-6G_v2.stl` :

- `.stl` / `.3mf` : fichiers prêts à imprimer
- `.step` : fichiers éditables (CAO)
- `.glb` : assemblage complet, utilisé pour la visualisation 3D sur le wiki

Les anciennes versions sont gardées (pas d'écrasement), pour savoir quelle pièce va avec quelle série de capteurs.

## ⚠️ Aucun fichier Takachi ici

Ce dossier est publié sur le wiki et le dépôt est public. Les plans (PDF, DWG, DXF) et le modèle STEP téléchargés chez Takachi sont sous licence du fabricant : ils ne doivent **jamais** être déposés ici, ni intégrés dans un assemblage publié. Ils sont rangés dans le Nextcloud de l'équipe (`AirCarto/Boitiers_3D/NebuleAir_Pro/source/`).
