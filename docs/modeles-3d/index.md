# Modèles 3D

!!! warning "Page en cours de modification"
    Cette page est en cours de construction : les modèles et l'emplacement des pièces peuvent encore changer.

Visualisez nos capteurs en 3D, directement dans le navigateur : **faites tourner** le modèle avec la souris ou le doigt, **zoomez** avec la molette ou en pinçant, et **ouvrez le capteur** avec le curseur sous le modèle. Sur téléphone, le bouton en bas à droite affiche le capteur en réalité augmentée, posé dans votre pièce.

<script type="module" src="https://cdn.jsdelivr.net/npm/@google/model-viewer@3.5.0/dist/model-viewer.min.js"></script>

## NebuleAir Pro

Version **verticale** (petite) : boîtier Takachi WP13-18-5G, capteur de particules NextPM et sonde BME280 externe. Trois aérations AirVent : une sur chaque côté et une sur la face avant. Le NextPM est fixé sous le couvercle, son tube d'entrée d'air emboîté dans l'AirVent avant : ouvrez le capteur pour le voir. Le cordon d'alimentation entre par un presse-étoupe en bas à droite. Il est présenté fixé sur un poteau de Ø60 mm par deux pattes Takachi WPMB-M4 et deux colliers de serrage.

<div class="viewer-3d">
<model-viewer data-open-m="0.13" src="../assets/3d_files/nebuleair_pro/nebuleair_pro_WP13-18-5G_v1.glb?v=2b2bece0"
  alt="NebuleAir Pro, version verticale, en 3D"
  camera-controls touch-action="pan-y" auto-rotate auto-rotate-delay="3000"
  camera-orbit="40deg 70deg 0.72m" animation-crossfade-duration="0" shadow-intensity="1" exposure="1.0"
  ar ar-modes="webxr scene-viewer quick-look">
</model-viewer>
<div class="viewer-3d-open"><label>Ouvrir le capteur <input type="range" min="0" max="1" step="0.01" value="0"></label></div>
<div class="viewer-3d-flow" hidden><label><input type="checkbox"> Voir le flux d'air</label></div>
<div class="viewer-3d-dims" hidden><label><input type="checkbox" checked> Afficher les cotes</label> <span class="viewer-3d-dims-info"></span></div>
</div>

La case **« Voir le flux d'air »** montre le trajet de l'air : il entre par le dessous de l'AirVent avant, est aspiré par le ventilateur du NextPM, puis ressort du boîtier par les AirVent latérales. C'est une illustration du trajet, pas un calcul d'écoulement.

!!! note "Boîtier et NextPM"
    Le boîtier (Takachi **WP13-18-5G**, IP68) et le capteur NextPM (Tera Sensor) sont des pièces du commerce. Ceux affichés ici sont des **modèles simplifiés redessinés par AirCarto** à partir des cotes publiques des fabricants, pour la visualisation.

### Fichiers à imprimer

| Pièce | Rôle | Fichier |
|---|---|---|
| AirVent — capot | Aération : se place à l'extérieur, ouverture vers le bas | [vent_top_v24.stl](../assets/3d_files/nebuleair_pro/vent_top_v24.stl) |
| AirVent — écrou | Se visse à l'intérieur sur le capot, de part et d'autre de la paroi (3 mm) | [vent_ecrou_v10.stl](../assets/3d_files/nebuleair_pro/vent_ecrou_v10.stl) |

Perçage du boîtier pour un AirVent : **Ø16 mm**.

## Panneau solaire et batterie

Sur un site sans courant, le NebuleAir Pro est alimenté par un **panneau solaire** et une **batterie**, fixés sur le même poteau que le capteur. Le capteur est montré à 3 m du sol, à côté d'une silhouette de 1,75 m pour l'échelle.

<div class="viewer-3d">
<model-viewer src="../assets/3d_files/kit_solaire/nebuleair_pro_kit_solaire_v1.glb?v=147e295a"
  alt="NebuleAir Pro avec panneau solaire et batterie sur un poteau, en 3D"
  camera-controls touch-action="pan-y" auto-rotate auto-rotate-delay="3000"
  camera-orbit="40deg 78deg auto" shadow-intensity="1" exposure="1.0"
  ar ar-modes="webxr scene-viewer quick-look">
</model-viewer>
</div>

| Élément | Caractéristiques |
|---|---|
| Panneau solaire | 50 W, 12 V, monocristallin · 670 × 460 × 30 mm · 3,2 kg |
| Support du panneau | Aluminium, incliné à 45°, fixé par 2 colliers inox (poteau jusqu'à Ø80 mm) |
| Batterie | RE-LION® Solar Powerbox PERF 120 · lithium-ion 120 Wh (11,1 V) · régulateur solaire et BMS intégrés · IP65 · 270 × 150 × 85 mm |
| Raccordement | Sorties 5 V et 12 V sur connecteurs à vis ; le capteur est branché sur le 12 V, par son presse-étoupe |

**Autonomie.** Le NebuleAir Pro consomme environ **0,5 W** : la batterie seule tient une dizaine de jours sans soleil (120 Wh ÷ 0,5 W ≈ 240 h). Selon les simulations de RE-LION® sur les données d'ensoleillement depuis 2005, un appareil de 0,6 W fonctionne toute l'année sans coupure, même la pire année : à Marseille dès un panneau de 25 W, à Lille avec le panneau de 50 W.

!!! note "Modèles simplifiés"
    Le panneau, son support et la batterie sont des modèles **simplifiés redessinés par AirCarto** à partir des dimensions publiques des fabricants, pour la visualisation.
