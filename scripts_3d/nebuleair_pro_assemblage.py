"""Assemblage 3D du NebuleAir Pro (petite version, boîtier Takachi WP13-18-5G)
pour la vue 3D du wiki.

Boîtier = modèle simplifié de takachi_wp.py (cotes publiques), percé aux
emplacements des pièces. Pièces AirCarto = STL du dossier publié.

Usage :
    ~/.venvs/cad3d/bin/python scripts_3d/nebuleair_pro_assemblage.py

Sortie : docs/assets/3d_files/nebuleair_pro/nebuleair_pro_WP13-18-5G_v1.glb

Repère du boîtier (mm) : origine au centre du fond, X = largeur (130),
Y = longueur (175, vertical une fois posé : +Y vers le haut), Z = profondeur
(dos contre le poteau en Z=0, couvercle en face avant en Z=45).
"""
from pathlib import Path

import numpy as np
import trimesh

from takachi_wp import BOXES, build, cyl, diff

ROOT = Path(__file__).resolve().parent.parent
DIR = ROOT / "docs/assets/3d_files/nebuleair_pro"
REF = "WP13-18-5G"

# --- AirVent (vent_top + vent_ecrou) -------------------------------------
# Dans le repère des STL : axe du tube en (35.558, 38.476), sortie vers +z,
# paroi entre z=0.5 (face intérieure, écrou) et z=3.5 (face extérieure, capot),
# ouverture du capot du côté -y (à orienter vers le bas).
VENT_AXIS = np.array([35.558, 38.476])
VENT_OUTER_Z = 3.5
VENT_HOLE_D = 16.0  # filetage Ø15.6

# Emplacements : (nom, face, coordonnées sur la face). À AJUSTER selon le
# capteur réel. Faces : "droite" (X=+65), "gauche" (X=-65), "avant" (couvercle).
#   droite/gauche : (Y, Z) du centre du trou ; Z=18 = milieu de la paroi du fond
#   avant         : (X, Y) du centre du trou sur le couvercle
VENTS = [
    ("airvent_droite", "droite", (40.0, 18.0)),
    ("airvent_gauche", "gauche", (40.0, 18.0)),
    ("airvent_avant", "avant", (0.0, 40.0)),
]

COLORS = {
    "corps": [205, 207, 208, 255],
    "couvercle": [222, 224, 225, 255],
    "vent_top": [45, 52, 60, 255],
    "vent_ecrou": [70, 78, 88, 255],
}


def frame(face, a, b, p):
    """Matrice 4x4 : repère local AirVent -> repère boîtier."""
    W = p["width"] / 2
    top = p["body_h"] + p["cover_h"]
    if face == "droite":
        ex, ey, ez, pos = [0, 0, -1], [0, 1, 0], [1, 0, 0], [W, a, b]
    elif face == "gauche":
        ex, ey, ez, pos = [0, 0, 1], [0, 1, 0], [-1, 0, 0], [-W, a, b]
    elif face == "avant":
        # sur le creux du couvercle : face intérieure du couvercle à top - top_thk
        ex, ey, ez = [1, 0, 0], [0, 1, 0], [0, 0, 1]
        pos = [a, b, top - p["top"] + (VENT_OUTER_Z - 0.5)]
    else:
        raise ValueError(face)
    R = np.column_stack([ex, ey, ez])
    T = np.eye(4)
    T[:3, :3] = R
    T[:3, 3] = np.array(pos, float) - R @ np.array([*VENT_AXIS, VENT_OUTER_Z])
    return T


def hole_cutter(face, a, b, p):
    """Cylindre à soustraire du boîtier au droit d'un AirVent."""
    c = cyl(VENT_HOLE_D, 20.0, 0, 0, -10.0)  # axe Z, centré sur l'origine
    T = frame(face, a, b, p)
    T2 = np.eye(4)
    T2[:3, :3] = T[:3, :3]
    T2[:3, 3] = T[:3, :3] @ np.array([*VENT_AXIS, VENT_OUTER_Z]) + T[:3, 3]
    c.apply_transform(T2)
    return c


def paint(m, rgba):
    m.visual = trimesh.visual.TextureVisuals(material=trimesh.visual.material.PBRMaterial(
        baseColorFactor=rgba, metallicFactor=0.0, roughnessFactor=0.6))
    return m


def main():
    p = BOXES[REF]
    body, cover = build(p)
    W = p["width"] / 2
    body_cuts = [hole_cutter(f, a, b, p) for _, f, (a, b) in VENTS if f in ("droite", "gauche")]
    cover_cuts = [hole_cutter(f, a, b, p) for _, f, (a, b) in VENTS if f == "avant"]
    if body_cuts:
        body = diff(body, body_cuts)
    if cover_cuts:
        cover = diff(cover, cover_cuts)

    top = trimesh.load(DIR / "vent_top_v24.stl")
    nut = trimesh.load(DIR / "vent_ecrou_v10.stl")

    scene = trimesh.Scene()
    scene.add_geometry(paint(body, COLORS["corps"]), node_name="boitier_corps", geom_name="boitier_corps")
    scene.add_geometry(paint(cover, COLORS["couvercle"]), node_name="boitier_couvercle", geom_name="boitier_couvercle")
    for name, face, (a, b) in VENTS:
        T = frame(face, a, b, p)
        for part, mesh in (("capot", top), ("ecrou", nut)):
            m = mesh.copy()
            m.apply_transform(T)
            key = "vent_top" if part == "capot" else "vent_ecrou"
            scene.add_geometry(paint(m, COLORS[key]), node_name=f"{name}_{part}", geom_name=f"{name}_{part}")

    # glTF : Y vers le haut (déjà le cas : +Y = haut du capteur posé), en mètres.
    # On centre le modèle pour que la vue 3D tourne autour du capteur.
    scene.apply_translation(-scene.bounds.mean(axis=0))
    scene.apply_scale(0.001)
    out = DIR / f"nebuleair_pro_{REF}_v1.glb"
    scene.export(out)
    print("->", out, f"{out.stat().st_size / 1024:.0f} Ko")


if __name__ == "__main__":
    main()
