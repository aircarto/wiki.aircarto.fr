# Modèles 3D

Visualisez nos capteurs en 3D, directement dans le navigateur : **faites tourner** le modèle avec la souris ou le doigt, **zoomez** avec la molette ou en pinçant. Sur téléphone, le bouton en bas à droite affiche le capteur en réalité augmentée, posé dans votre pièce.

<script type="module" src="https://cdn.jsdelivr.net/npm/@google/model-viewer@3.5.0/dist/model-viewer.min.js"></script>

## NebuleAir Pro

Version **verticale** (petite) : boîtier Takachi WP13-18-5G, capteur de particules NextPM et sonde BME280 externe. Trois aérations AirVent : une sur chaque côté et une sur la face avant.

<div class="viewer-3d">
<model-viewer src="../assets/3d_files/nebuleair_pro/nebuleair_pro_WP13-18-5G_v1.glb"
  alt="NebuleAir Pro, version verticale, en 3D"
  camera-controls touch-action="pan-y" auto-rotate auto-rotate-delay="3000"
  camera-orbit="35deg 70deg auto" shadow-intensity="1" exposure="1.1"
  ar ar-modes="webxr scene-viewer quick-look">
</model-viewer>
</div>

!!! note "Boîtier"
    Le boîtier est un modèle du commerce (Takachi **WP13-18-5G**, IP68). Celui affiché ici est un **modèle simplifié redessiné par AirCarto** à partir des cotes publiques du fabricant, pour la visualisation : le boîtier s'achète chez Takachi.

### Fichiers à imprimer

| Pièce | Rôle | Fichier |
|---|---|---|
| AirVent — capot | Aération : se place à l'extérieur, ouverture vers le bas | [vent_top_v24.stl](../assets/3d_files/nebuleair_pro/vent_top_v24.stl) |
| AirVent — écrou | Se visse à l'intérieur sur le capot, de part et d'autre de la paroi (3 mm) | [vent_ecrou_v10.stl](../assets/3d_files/nebuleair_pro/vent_ecrou_v10.stl) |

Perçage du boîtier pour un AirVent : **Ø16 mm**.
