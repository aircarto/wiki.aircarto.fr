# Modèles 3D

!!! warning "Page en cours de modification"
    Cette page est en cours de construction : les modèles et l'emplacement des pièces peuvent encore changer.

Visualisez nos capteurs en 3D, directement dans le navigateur : **faites tourner** le modèle avec la souris ou le doigt, **zoomez** avec la molette ou en pinçant, et **ouvrez le capteur** avec le curseur sous le modèle. Sur téléphone, le bouton en bas à droite affiche le capteur en réalité augmentée, posé dans votre pièce.

<script type="module" src="https://cdn.jsdelivr.net/npm/@google/model-viewer@3.5.0/dist/model-viewer.min.js"></script>

## NebuleAir Pro

Version **verticale** (petite) : boîtier Takachi WP13-18-5G, capteur de particules NextPM et sonde BME280 externe. Trois aérations AirVent : une sur chaque côté et une sur la face avant. Le NextPM est fixé sous le couvercle, son tube d'entrée d'air emboîté dans l'AirVent avant : ouvrez le capteur pour le voir. Il est présenté fixé sur un poteau de Ø60 mm par deux pattes Takachi WPMB-M4 et deux colliers de serrage.

<div class="viewer-3d">
<model-viewer data-open-m="0.13" src="../assets/3d_files/nebuleair_pro/nebuleair_pro_WP13-18-5G_v1.glb"
  alt="NebuleAir Pro, version verticale, en 3D"
  camera-controls touch-action="pan-y" auto-rotate auto-rotate-delay="3000"
  camera-orbit="40deg 70deg 0.72m" shadow-intensity="1" exposure="1.0"
  ar ar-modes="webxr scene-viewer quick-look">
</model-viewer>
<div class="viewer-3d-open"><label>Ouvrir le capteur <input type="range" min="0" max="1" step="0.01" value="0"></label></div>
<div class="viewer-3d-dims" hidden><label><input type="checkbox" checked> Afficher les cotes</label> <span class="viewer-3d-dims-info"></span></div>
</div>

!!! note "Boîtier et NextPM"
    Le boîtier (Takachi **WP13-18-5G**, IP68) et le capteur NextPM (Tera Sensor) sont des pièces du commerce. Ceux affichés ici sont des **modèles simplifiés redessinés par AirCarto** à partir des cotes publiques des fabricants, pour la visualisation.

### Fichiers à imprimer

| Pièce | Rôle | Fichier |
|---|---|---|
| AirVent — capot | Aération : se place à l'extérieur, ouverture vers le bas | [vent_top_v24.stl](../assets/3d_files/nebuleair_pro/vent_top_v24.stl) |
| AirVent — écrou | Se visse à l'intérieur sur le capot, de part et d'autre de la paroi (3 mm) | [vent_ecrou_v10.stl](../assets/3d_files/nebuleair_pro/vent_ecrou_v10.stl) |

Perçage du boîtier pour un AirVent : **Ø16 mm**.
