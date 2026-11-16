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
import json
import struct
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
    "corps": [128, 135, 144, 255],
    "couvercle": [140, 147, 156, 255],
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


EDGE_COLOR = [40, 45, 52, 255]
EDGE_ANGLE_DEG = 25  # arêtes vives au-delà de cet angle entre deux faces


def edges(m):
    """Arêtes vives du maillage, en traits (lignes glTF), pour lire les formes."""
    sel = m.face_adjacency_angles > np.radians(EDGE_ANGLE_DEG)
    # Traits décalés de 0,15 mm vers l'extérieur : sinon ils se confondent avec
    # la surface et s'affichent en pointillés.
    # (normales calculées sur une copie : sinon trimesh les exporte et lisse
    # l'ombrage des faces planes)
    v = m.vertices + m.copy().vertex_normals * 0.15
    path = trimesh.load_path(v[m.face_adjacency_edges[sel]])
    path.colors = np.tile(EDGE_COLOR, (len(path.entities), 1))
    return path


# Animation « ouverture » : le couvercle et ce qui y est fixé s'éloignent du fond
# (axe +Z, face avant). Pilotée par le curseur de la page Modèles 3D.
OPEN_DISTANCE_M = 0.07
OPEN_PREFIXES = ("boitier_couvercle", "airvent_avant")


def add_opening_animation(glb_path):
    """Ajoute au GLB un nœud parent animé (translation) pour ouvrir le boîtier."""
    data = Path(glb_path).read_bytes()
    jlen = struct.unpack("<I", data[12:16])[0]
    gltf = json.loads(data[20:20 + jlen])
    blen = struct.unpack("<I", data[20 + jlen:24 + jlen])[0]
    binary = bytearray(data[28 + jlen:28 + jlen + blen])

    def push(arr):
        while len(binary) % 4:
            binary.append(0)
        off = len(binary)
        raw = np.asarray(arr, dtype="<f4").tobytes()
        binary.extend(raw)
        gltf["bufferViews"].append({"buffer": 0, "byteOffset": off, "byteLength": len(raw)})
        return len(gltf["bufferViews"]) - 1

    times = [0.0, 1.0]
    moves = [[0, 0, 0], [0, 0, OPEN_DISTANCE_M]]
    acc = gltf["accessors"]
    acc.append({"bufferView": push(times), "componentType": 5126, "count": 2, "type": "SCALAR",
                "min": [0.0], "max": [1.0]})
    t_acc = len(acc) - 1
    acc.append({"bufferView": push(moves), "componentType": 5126, "count": 2, "type": "VEC3",
                "min": [0, 0, 0], "max": [0, 0, OPEN_DISTANCE_M]})
    v_acc = len(acc) - 1

    roots = gltf["scenes"][0]["nodes"]
    moving = [i for i in roots if gltf["nodes"][i].get("name", "").startswith(OPEN_PREFIXES)]
    gltf["nodes"].append({"name": "ouverture", "translation": [0, 0, 0], "children": moving})
    parent = len(gltf["nodes"]) - 1
    gltf["scenes"][0]["nodes"] = [i for i in roots if i not in moving] + [parent]
    gltf["animations"] = [{"name": "ouverture",
                           "samplers": [{"input": t_acc, "output": v_acc, "interpolation": "LINEAR"}],
                           "channels": [{"sampler": 0, "target": {"node": parent, "path": "translation"}}]}]
    while len(binary) % 4:
        binary.append(0)
    gltf["buffers"][0]["byteLength"] = len(binary)

    js = json.dumps(gltf, separators=(",", ":")).encode()
    js += b" " * (-len(js) % 4)
    out = struct.pack("<III", 0x46546C67, 2, 12 + 8 + len(js) + 8 + len(binary))
    out += struct.pack("<II", len(js), 0x4E4F534A) + js
    out += struct.pack("<II", len(binary), 0x004E4942) + bytes(binary)
    Path(glb_path).write_bytes(out)
    return len(moving)


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
    scene.add_geometry(edges(body), node_name="boitier_corps_aretes", geom_name="boitier_corps_aretes")
    scene.add_geometry(edges(cover), node_name="boitier_couvercle_aretes", geom_name="boitier_couvercle_aretes")
    for name, face, (a, b) in VENTS:
        T = frame(face, a, b, p)
        for part, mesh in (("capot", top), ("ecrou", nut)):
            m = mesh.copy()
            m.apply_transform(T)
            key = "vent_top" if part == "capot" else "vent_ecrou"
            scene.add_geometry(paint(m, COLORS[key]), node_name=f"{name}_{part}", geom_name=f"{name}_{part}")
            scene.add_geometry(edges(m), node_name=f"{name}_{part}_aretes", geom_name=f"{name}_{part}_aretes")

    # glTF : Y vers le haut (déjà le cas : +Y = haut du capteur posé), en mètres.
    # On centre le modèle pour que la vue 3D tourne autour du capteur.
    scene.apply_translation(-scene.bounds.mean(axis=0))
    scene.apply_scale(0.001)
    out = DIR / f"nebuleair_pro_{REF}_v1.glb"
    scene.export(out)
    n = add_opening_animation(out)
    print("->", out, f"{out.stat().st_size / 1024:.0f} Ko ; animation « ouverture » sur {n} nœuds")


if __name__ == "__main__":
    main()
