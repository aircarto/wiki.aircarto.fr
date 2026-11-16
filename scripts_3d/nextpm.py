"""Modèle 3D SIMPLIFIÉ du capteur de particules NextPM (Tera Sensor), redessiné
à partir des cotes publiques du datasheet (page « Mechanical specifications »)
et du guide utilisateur (§5.2 : air, fixation). Pour la visualisation et les
essais d'ajustement, pas une reproduction du capteur.

Usage :
    ~/.venvs/cad3d/bin/python scripts_3d/nextpm.py

Sortie (docs/assets/3d_files/nextPM/) :
    nextpm_simplifie_v1.stl  (une seule pièce, pour la CAO / l'ajustement)
    nextpm_simplifie_v1.glb  (couleurs : boîtier métal + parties noires)

Repère (mm) : origine au coin du corps, X = longueur (59.85), Y = largeur (50),
Z = hauteur ; Z=0 = dos (trous de fixation), dessus = tube d'entrée d'air.
Vue de dessus : bloc ventilateur en haut à droite, tube d'entrée en bas à droite,
connecteur Molex sur la face avant (Y=0), sortie d'air sur le côté droit (X max).
"""
from pathlib import Path

import numpy as np
import trimesh
from shapely.geometry import box

from takachi_wp import SEG, cyl, diff, union

OUT = Path(__file__).resolve().parent.parent / "docs/assets/3d_files/nextPM"

L, W, H = 59.85, 50.0, 18.4          # corps
H_TOT = 23.6                          # avec bloc ventilateur et tube
TOP = H_TOT - H                       # 5.2 mm au-dessus du corps
R_BODY = 2.0
METAL_X = 40.0                        # au-delà : partie en plastique noir


def rbox(x0, y0, x1, y1, z0, z1, r):
    r = min(r, (x1 - x0) / 2 - 0.01, (y1 - y0) / 2 - 0.01)
    poly = box(x0 + r, y0 + r, x1 - r, y1 - r).buffer(r, quad_segs=SEG // 4)
    m = trimesh.creation.extrude_polygon(poly, z1 - z0)
    m.apply_translation([0, 0, z0])
    return m


def build():
    metal = rbox(0, 0, METAL_X + 1.0, W, 0, H, R_BODY)
    black = rbox(METAL_X, 0, L, W, 0, H, R_BODY)
    metal = diff(metal, [rbox(METAL_X, -1, L + 1, W + 1, -1, H + 1, 0.01)])

    # Bloc ventilateur / sortie d'air (dessus, en haut à droite)
    fan = rbox(37.7, 25.4, 59.2, W - 0.4, H - 0.5, H_TOT, 3.0)
    # Tube d'entrée d'air (dessus, en bas à droite) : Ø11 ext., Ø8 int.
    tube = diff(cyl(11.0, TOP + 0.5, 51.8, 7.0, H - 0.5), [cyl(8.0, TOP + 2, 51.8, 7.0, H - 1.5)])
    # Fente de sortie d'air sur le côté droit du bloc
    black = union([black, fan, tube])
    black = diff(black, [rbox(L - 1.5, 30.0, L + 1.0, 45.0, H + 0.8, H_TOT - 1.0, 0.5)])

    # Clips latéraux (encombrement 62.03 x 52.49 avec les clips)
    clip_x = (62.03 - L) / 2
    clip_y = 52.49 - W
    clips = [
        rbox(-clip_x, 18.0, 0.2, 27.0, 5.0, 13.0, 0.4),
        rbox(L - 0.2, 18.0, L + clip_x, 27.0, 5.0, 13.0, 0.4),
        rbox(26.0, W - 0.2, 37.0, W + clip_y, 5.0, 13.0, 0.4),
    ]

    # Connecteur Molex 6 broches (face avant, côté gauche) : logement
    molex = rbox(8.0, -0.5, 22.0, 4.0, 5.0, 11.0, 0.3)
    metal = diff(union([metal] + clips[:1] + clips[2:]), [molex])
    black = union([black, clips[1]])

    # Trous de fixation M2.5 au dos (profondeur 5 mm), guide §5.2.2 :
    # vus de dos, trou 2 à 5.4 mm du bord droit et 10.4 mm du bas, trou 1 à
    # 29 mm à gauche et 32 mm au-dessus. Vu de dessus, X est inversé.
    h2 = (5.4, 10.4)
    h1 = (5.4 + 29.0, 10.4 + 32.0)
    holes = [cyl(2.2, 5.0 + 1, x, y, -1) for x, y in (h1, h2)]
    metal = diff(metal, holes)
    black = diff(black, holes)
    return metal, black


def paint(m, rgba, rough):
    m.visual = trimesh.visual.TextureVisuals(material=trimesh.visual.material.PBRMaterial(
        baseColorFactor=rgba, metallicFactor=0.0, roughnessFactor=rough))
    return m


def main():
    metal, black = build()
    OUT.mkdir(parents=True, exist_ok=True)
    whole = union([metal, black])
    whole.export(OUT / "nextpm_simplifie_v1.stl")

    scene = trimesh.Scene()
    scene.add_geometry(paint(metal, [175, 180, 186, 255], 0.45), node_name="nextpm_metal", geom_name="nextpm_metal")
    scene.add_geometry(paint(black, [32, 34, 37, 255], 0.7), node_name="nextpm_noir", geom_name="nextpm_noir")
    # glTF : Y vers le haut, en mètres ; capteur posé à plat (dessus vers le haut)
    scene.apply_transform(trimesh.transformations.rotation_matrix(-np.pi / 2, [1, 0, 0]))
    scene.apply_translation(-scene.bounds.mean(axis=0))
    scene.apply_scale(0.001)
    scene.export(OUT / "nextpm_simplifie_v1.glb")
    ext = whole.extents.round(2)
    print(f"NextPM : étanche={whole.is_watertight} encombrement={ext} mm faces={len(whole.faces)}")


if __name__ == "__main__":
    main()
