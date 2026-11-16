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

import nextpm
from takachi_wp import BOXES, bracket_wpmb_m4, build, cyl, diff

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
    ("airvent_avant", "avant", (0.0, 40.0)),  # X recalculé plus bas si NEXTPM_CENTERED_X
]

# NextPM : fixé sous le couvercle, tube d'entrée d'air emboîté dans l'AirVent
# avant (tube Ø11 dans l'alésage Ø~12.5 de l'AirVent). Rotation autour de Z
# (degrés) choisie pour que le capteur tienne dans le boîtier sans toucher les
# écrous des AirVent latérales : À CONFIRMER sur le capteur réel.
NEXTPM_VENT = "airvent_avant"
NEXTPM_ROT_DEG = 180.0
NEXTPM_INSERTION = 3.0  # mm de tube engagés dans l'AirVent
NEXTPM_TUBE_XY = (51.8, 7.0)  # axe du tube dans le repère de nextpm.py
NEXTPM_CENTERED_X = True  # NextPM centré en largeur : l'AirVent avant suit son tube


def _nextpm_centered_vent_x():
    """X de l'AirVent avant pour que le corps du NextPM soit centré (X=0)."""
    centre_rel_tube = np.array([nextpm.L / 2 - NEXTPM_TUBE_XY[0], nextpm.W / 2 - NEXTPM_TUBE_XY[1], 0.0])
    R = trimesh.transformations.rotation_matrix(np.radians(NEXTPM_ROT_DEG), [0, 0, 1])[:3, :3]
    return float(-(R @ centre_rel_tube)[0])


if NEXTPM_CENTERED_X:
    VENTS = [(n, f, (_nextpm_centered_vent_x(), b) if n == NEXTPM_VENT else (a, b)) for n, f, (a, b) in VENTS]

# Presse-étoupe du cordon d'alimentation : face du bas (Y=-87.5), à gauche vu de
# face (X<0), à mi-profondeur du fond. Modèle générique M16 x 1,5 (câble Ø4-8).
GLAND_X, GLAND_Z = -30.0, 18.0
GLAND_HOLE_D = 16.2
CABLE_D = 6.0
CABLE_LEN = 90.0       # tronçon de cordon affiché sous le capteur (hors cotes)


def gland_parts(wall):
    """Presse-étoupe générique M16 dans son repère : axe +Z vers l'extérieur,
    face extérieure de la paroi en Z=0, face intérieure en Z=-wall."""
    def hexa(af, h, z0):
        m = trimesh.creation.cylinder(radius=af / np.sqrt(3), height=h, sections=6)
        m.apply_translation([0, 0, z0 + h / 2])
        return m
    body = trimesh.util.concatenate([
        hexa(20.0, 5.0, 0.0),                                  # 6 pans contre la paroi
        cyl(16.0, 4.0, 0, 0, 5.0),                             # filetage du chapeau
        cyl(19.0, 6.0, 0, 0, 7.0),                             # chapeau
        cyl(15.0, 2.5, 0, 0, 13.0),                            # dôme
        cyl(15.6, wall + 6.0, 0, 0, -wall - 6.0),              # filetage M16 dans la paroi
    ])
    nut = hexa(20.0, 4.0, -wall - 4.0)                        # contre-écrou intérieur
    return body, nut


def gland_frame(p):
    """Repère presse-étoupe -> boîtier : axe vers -Y (sortie par le bas)."""
    T = np.eye(4)
    T[:3, :3] = np.column_stack([[1, 0, 0], [0, 0, 1], [0, -1, 0]])
    T[:3, 3] = [GLAND_X, -p["length"] / 2, GLAND_Z]
    return T


# Poteau (mât) et colliers de serrage : décor de montage, hors cotes du capteur.
POLE_D = 60.0          # diamètre du poteau (mm), courant pour un mât d'éclairage
POLE_LEN = 420.0       # longueur du tronçon affiché (mm)
STRAP_W = 9.0          # largeur du collier inox (mm)
STRAP_T = 0.8          # épaisseur du collier (mm)

COLORS = {
    "corps": [128, 135, 144, 255],
    "couvercle": [140, 147, 156, 255],
    "vent_top": [45, 52, 60, 255],
    "vent_ecrou": [70, 78, 88, 255],
    "patte_poteau": [128, 135, 144, 255],
    "poteau": [150, 156, 160, 255],
    "collier": [200, 204, 208, 255],
    "presse_etoupe": [38, 40, 44, 255],
    "cable": [22, 23, 25, 255],
    "nextpm_metal": [175, 180, 186, 255],
    "nextpm_noir": [32, 34, 37, 255],
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
OPEN_DISTANCE_M = 0.13
# Vue éclatée : chaque groupe de pièces avance d'une fraction de l'ouverture.
# Le NextPM se détache du couvercle et s'arrête à mi-chemin, pour être visible.
OPEN_GROUPS = [
    ("ouverture_couvercle", ("boitier_couvercle", "airvent_avant"), 1.0),
    ("ouverture_nextpm", ("nextpm",), 0.5),
]


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
    acc = gltf["accessors"]
    acc.append({"bufferView": push(times), "componentType": 5126, "count": 2, "type": "SCALAR",
                "min": [0.0], "max": [1.0]})
    t_acc = len(acc) - 1

    roots = list(gltf["scenes"][0]["nodes"])
    samplers, channels, moved = [], [], 0
    for group, prefixes, fraction in OPEN_GROUPS:
        d = OPEN_DISTANCE_M * fraction
        acc.append({"bufferView": push([[0, 0, 0], [0, 0, d]]), "componentType": 5126, "count": 2,
                    "type": "VEC3", "min": [0, 0, 0], "max": [0, 0, d]})
        members = [i for i in roots if gltf["nodes"][i].get("name", "").startswith(prefixes)]
        gltf["nodes"].append({"name": group, "translation": [0, 0, 0], "children": members})
        parent = len(gltf["nodes"]) - 1
        roots = [i for i in roots if i not in members] + [parent]
        samplers.append({"input": t_acc, "output": len(acc) - 1, "interpolation": "LINEAR"})
        channels.append({"sampler": len(samplers) - 1, "target": {"node": parent, "path": "translation"}})
        moved += len(members)
    gltf["scenes"][0]["nodes"] = roots
    gltf["animations"] = [{"name": "ouverture", "samplers": samplers, "channels": channels}]
    while len(binary) % 4:
        binary.append(0)
    gltf["buffers"][0]["byteLength"] = len(binary)

    js = json.dumps(gltf, separators=(",", ":")).encode()
    js += b" " * (-len(js) % 4)
    out = struct.pack("<III", 0x46546C67, 2, 12 + 8 + len(js) + 8 + len(binary))
    out += struct.pack("<II", len(js), 0x4E4F534A) + js
    out += struct.pack("<II", len(binary), 0x004E4942) + bytes(binary)
    Path(glb_path).write_bytes(out)
    return moved


def pole_centre_z(bracket_profile, r):
    """Z de l'axe du poteau calé dans la gorge en V des pattes (le plus haut
    possible sans pénétrer la patte), par dichotomie sur le profil (x, z)."""
    from shapely.geometry import Point
    hi, lo = -12.0 + r, -12.0 - 2 * r  # hi : pénètre, lo : libre
    for _ in range(60):
        mid = (hi + lo) / 2
        if Point(0, mid).buffer(r, quad_segs=64).intersection(bracket_profile).area > 1e-4:
            hi = mid
        else:
            lo = mid
    return lo


def strap_mesh(zc, r, y):
    """Collier de serrage : bande qui fait le tour du poteau et passe dans les
    fentes de la patte (entraxe 13.1), avec le boîtier de vis sans fin."""
    from shapely.geometry import MultiPoint, Point
    hull = Point(0, zc).buffer(r, quad_segs=64).union(MultiPoint([(-6.55, -3.0), (6.55, -3.0)])).convex_hull
    band = hull.buffer(STRAP_T, quad_segs=16).difference(hull)
    m = trimesh.creation.extrude_polygon(band, STRAP_W)  # profil (x, z), extrudé selon Y
    m.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [1, 0, 0]))
    m.apply_translation([0, y + STRAP_W / 2, 0])
    screw = trimesh.creation.box(extents=[14.0, STRAP_W + 3.0, 7.0])  # vis sans fin, côté opposé
    screw.apply_translation([0, y, zc - r - STRAP_T - 3.0])
    return trimesh.util.concatenate([m, screw])


def paint(m, rgba):
    m.visual = trimesh.visual.TextureVisuals(material=trimesh.visual.material.PBRMaterial(
        baseColorFactor=rgba, metallicFactor=0.0, roughnessFactor=0.6))
    return m


def main():
    p = BOXES[REF]
    body, cover = build(p)
    W = p["width"] / 2
    body_cuts = [hole_cutter(f, a, b, p) for _, f, (a, b) in VENTS if f in ("droite", "gauche")]
    gland_hole = cyl(GLAND_HOLE_D, 20.0, 0, 0, -10.0)
    gland_hole.apply_transform(gland_frame(p))
    body_cuts.append(gland_hole)
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

    # --- Pattes de fixation sur poteau WPMB-M4 (dos du boîtier, trous M4) ---
    bracket = bracket_wpmb_m4()
    for i, (x, y) in enumerate(p["mount_holes"]):
        m = bracket.copy()
        m.apply_translation([x, y, 0.0])
        name = f"patte_poteau_{'bas' if y < 0 else 'haut'}"
        scene.add_geometry(paint(m, COLORS["patte_poteau"]), node_name=name, geom_name=name)
        scene.add_geometry(edges(m), node_name=f"{name}_aretes", geom_name=f"{name}_aretes")

    # --- Presse-étoupe du cordon d'alimentation (bas, à gauche) ---
    Tg = gland_frame(p)
    for part, mesh in zip(("presse_etoupe", "presse_etoupe_ecrou"), gland_parts(p["wall"])):
        mesh.apply_transform(Tg)
        scene.add_geometry(paint(mesh, COLORS["presse_etoupe"]), node_name=part, geom_name=part)
        scene.add_geometry(edges(mesh), node_name=f"{part}_aretes", geom_name=f"{part}_aretes")

    # --- NextPM sous le couvercle ---
    vname, vface, (va, vb) = next(v for v in VENTS if v[0] == NEXTPM_VENT)
    Tv = frame(vface, va, vb, p)
    axis_w = Tv[:3, :3] @ np.array([*VENT_AXIS, 0.0]) + Tv[:3, 3]  # axe de l'AirVent
    vent_bottom_z = (Tv @ np.array([*VENT_AXIS, -5.5, 1.0]))[2]      # bas du filetage
    Tn = trimesh.transformations.rotation_matrix(np.radians(NEXTPM_ROT_DEG), [0, 0, 1])
    tube_after_rot = Tn[:3, :3] @ np.array([*NEXTPM_TUBE_XY, 0.0])
    Tn[:3, 3] = [axis_w[0] - tube_after_rot[0], axis_w[1] - tube_after_rot[1],
                 vent_bottom_z + NEXTPM_INSERTION - nextpm.H_TOT]
    for part, mesh in zip(("nextpm_metal", "nextpm_noir"), nextpm.build()):
        mesh.apply_transform(Tn)
        scene.add_geometry(paint(mesh, COLORS[part]), node_name=part, geom_name=part)
        scene.add_geometry(edges(mesh), node_name=f"{part}_aretes", geom_name=f"{part}_aretes")
        lo, hi = mesh.bounds
        print(f"{part}: X {lo[0]:.1f}..{hi[0]:.1f}  Y {lo[1]:.1f}..{hi[1]:.1f}  Z {lo[2]:.1f}..{hi[2]:.1f}")

    # Centre et encombrement du CAPTEUR seul (sans le poteau) : la vue 3D tourne
    # autour du capteur et les cotes ne comptent pas le décor.
    centre = scene.bounds.mean(axis=0)
    overall = scene.bounds[1] - scene.bounds[0]

    # --- Poteau + 2 colliers (un par patte) ---
    from shapely.geometry import Polygon
    profile = Polygon([(-14, 0), (14, 0), (14, -12), (10.2, -12), (5, -7.4),
                       (-5, -7.4), (-10.2, -12), (-14, -12)])  # = takachi_wp.bracket_wpmb_m4
    r = POLE_D / 2
    zc = pole_centre_z(profile, r)
    pole = trimesh.creation.cylinder(radius=r, height=POLE_LEN, sections=96)
    pole.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [1, 0, 0]))
    pole.apply_translation([0, 0, zc])
    pole.visual = trimesh.visual.TextureVisuals(material=trimesh.visual.material.PBRMaterial(
        baseColorFactor=COLORS["poteau"], metallicFactor=0.5, roughnessFactor=0.45))
    scene.add_geometry(pole, node_name="poteau", geom_name="poteau")
    for x, y in p["mount_holes"]:
        name = f"collier_{'bas' if y < 0 else 'haut'}"
        m = strap_mesh(zc, r, y)
        m.visual = trimesh.visual.TextureVisuals(material=trimesh.visual.material.PBRMaterial(
            baseColorFactor=COLORS["collier"], metallicFactor=0.8, roughnessFactor=0.3))
        scene.add_geometry(m, node_name=name, geom_name=name)
    print(f"poteau Ø{POLE_D:.0f} : axe à Z={zc:.1f} mm (dos du boîtier à Z=0)")

    # Cordon d'alimentation sortant du presse-étoupe (décor, hors cotes) :
    # de l'intérieur du boîtier jusqu'à CABLE_LEN sous le chapeau.
    y_in, y_out = -p["length"] / 2 + 12.0, -p["length"] / 2 - 15.5 - CABLE_LEN
    cable = trimesh.creation.cylinder(radius=CABLE_D / 2, height=y_in - y_out, sections=32)
    cable.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [1, 0, 0]))
    cable.apply_translation([GLAND_X, (y_in + y_out) / 2, GLAND_Z])
    scene.add_geometry(paint(cable, COLORS["cable"]), node_name="cordon_alim", geom_name="cordon_alim")

    # glTF : Y vers le haut (déjà le cas : +Y = haut du capteur posé), en mètres.
    scene.apply_translation(-centre)
    scene.apply_scale(0.001)
    out = DIR / f"nebuleair_pro_{REF}_v1.glb"

    # Cotes pour la page Modèles 3D (lues par viewer-3d.js) : boîtier fermé, dans
    # le repère du GLB (mètres, modèle centré) + encombrement total en mm.
    box_min = np.array([-p["width"] / 2, -p["length"] / 2, 0.0])
    box_max = np.array([p["width"] / 2, p["length"] / 2, p["body_h"] + p["cover_h"]])
    dims = {
        "boitier": {"ref": REF,
                    "min": ((box_min - centre) * 0.001).round(5).tolist(),
                    "max": ((box_max - centre) * 0.001).round(5).tolist(),
                    "mm": [p["width"], p["length"], p["body_h"] + p["cover_h"]]},
        "encombrement_mm": overall.round(1).tolist(),
    }
    out.with_suffix(".dims.json").write_text(json.dumps(dims, indent=1))
    scene.export(out)
    n = add_opening_animation(out)
    print("->", out, f"{out.stat().st_size / 1024:.0f} Ko ; animation « ouverture » sur {n} nœuds")


if __name__ == "__main__":
    main()
