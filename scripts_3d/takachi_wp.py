"""Modèle 3D SIMPLIFIÉ des boîtiers Takachi WP, redessiné à partir des cotes
publiques du plan PDF du fabricant (pas à partir du STEP Takachi, dont la
licence interdit la diffusion).

Sert à la visualisation et aux essais d'ajustement de nos pièces. Ce n'est PAS
un fichier pour imprimer le boîtier : le boîtier s'achète chez Takachi.

Usage :
    ~/.venvs/cad3d/bin/python scripts_3d/takachi_wp.py WP13-18-5G

Sortie (dans docs/assets/3d_files/nebuleair_pro/) :
    takachi_<ref>_simplifie_corps_v1.stl
    takachi_<ref>_simplifie_couvercle_v1.stl
    takachi_<ref>_simplifie_v1.glb   (assemblage coloré, pour le wiki)

Repère : origine au centre du fond, X = largeur, Y = longueur, Z = hauteur (mm).
"""
import sys
from pathlib import Path

import numpy as np
import trimesh
from shapely.geometry import box

# Cotes relevées sur le plan public Takachi (pages 2 à 4). Ajouter ici le
# WP15-21-6G quand on aura son plan.
BOXES = {
    "WP13-18-5G": dict(
        width=130.0, length=175.0,      # extérieur
        body_h=33.0, cover_h=12.0,      # total 45
        corner_r=20.0,                  # 4-R20
        wall=3.0, floor=3.0, top=3.0,   # coupes E-E et C-C
        panel=(93.8, 138.8), panel_r=2.0, panel_depth=1.0,  # creux du couvercle
        # 6 vis du couvercle (posées par le dessous), plots Ø7.7
        lid_screws=[(sx * 50.0, sy * 75.0) for sx in (-1, 1) for sy in (-1, 1)]
                   + [(-58.0, 0.0), (58.0, 0.0)],
        lid_boss_d=7.7, lid_screw_hole_d=2.8, counterbore_d=5.7, counterbore_h=3.0,
        # 8 plots de carte M2.3 (grille 80 x 120)
        pcb_bosses=[(x, y) for x in (-40.0, 0.0, 40.0) for y in (-60.0, 60.0)]
                   + [(-40.0, 0.0), (40.0, 0.0)],
        pcb_boss_d=4.6, pcb_boss_h=6.0, pcb_hole_d=2.0,
        # 2 trous M4 de fixation sur poteau (entraxe 156.2)
        mount_holes=[(0.0, -78.1), (0.0, 78.1)], mount_hole_d=4.3,
        # à l'intérieur, autour de chaque trou M4 : plot Ø10 + muret rectangulaire
        # collé à la paroi (30 de large, jusqu'à 18.5 du bord extérieur, R3)
        mount_boss_d=10.0, mount_rim_w=30.0, mount_rim_reach=18.5,
        mount_rim_t=1.5, mount_rim_r=3.0, mount_rim_h=8.0,
    ),
}

SEG = 64  # finesse des arrondis


def rounded_rect(w, l, r):
    r = min(r, w / 2 - 0.01, l / 2 - 0.01)
    return box(-w / 2 + r, -l / 2 + r, w / 2 - r, l / 2 - r).buffer(r, quad_segs=SEG // 4)


def prism(poly, h, z0=0.0):
    m = trimesh.creation.extrude_polygon(poly, h)
    m.apply_translation([0, 0, z0])
    return m


def cyl(d, h, x, y, z0):
    m = trimesh.creation.cylinder(radius=d / 2, height=h, sections=SEG)
    m.apply_translation([x, y, z0 + h / 2])
    return m


def union(meshes):
    return trimesh.boolean.union(meshes, engine="manifold")


def diff(a, cutters):
    return trimesh.boolean.difference([a] + list(cutters), engine="manifold")


def build(p):
    W, L, R, t = p["width"], p["length"], p["corner_r"], p["wall"]
    outer = rounded_rect(W, L, R)
    inner = rounded_rect(W - 2 * t, L - 2 * t, R - t)

    # --- Corps (fond) ------------------------------------------------------
    hb = p["body_h"]
    body = diff(prism(outer, hb), [prism(inner, hb, p["floor"])])
    bosses = [cyl(p["lid_boss_d"], hb - p["floor"], x, y, p["floor"]) for x, y in p["lid_screws"]]
    bosses += [cyl(p["pcb_boss_d"], p["pcb_boss_h"], x, y, p["floor"]) for x, y in p["pcb_bosses"]]
    for x, y in p["mount_holes"]:
        sgn = 1 if y > 0 else -1
        y_in = sgn * (L / 2 - p["mount_rim_reach"])      # bord du muret côté intérieur
        y_out = sgn * (L / 2 - t / 2)                      # noyé dans la paroi
        y0, y1 = sorted((y_in, y_out))
        rw, rt, rr = p["mount_rim_w"], p["mount_rim_t"], p["mount_rim_r"]
        outer_rim = rounded_rect(rw, y1 - y0, rr)
        from shapely import affinity
        outer_rim = affinity.translate(outer_rim, x, (y0 + y1) / 2)
        ring = outer_rim.difference(outer_rim.buffer(-rt, quad_segs=SEG // 4))
        bosses.append(prism(ring, p["mount_rim_h"], p["floor"] - 0.01))
        bosses.append(cyl(p["mount_boss_d"], p["mount_rim_h"], x, y, p["floor"] - 0.01))
    body = union([body] + bosses)
    holes = [cyl(p["lid_screw_hole_d"], hb + 2, x, y, -1) for x, y in p["lid_screws"]]
    holes += [cyl(p["counterbore_d"], p["counterbore_h"] + 1, x, y, -1) for x, y in p["lid_screws"]]
    holes += [cyl(p["pcb_hole_d"], p["pcb_boss_h"], x, y, p["floor"] + 1) for x, y in p["pcb_bosses"]]
    holes += [cyl(p["mount_hole_d"], p["floor"] + p["mount_rim_h"] + 2, x, y, -1) for x, y in p["mount_holes"]]
    body = diff(body, holes)

    # --- Couvercle -----------------------------------------------------------
    hc, z0 = p["cover_h"], hb
    cover = diff(prism(outer, hc, z0), [prism(inner, hc - p["top"], z0 - 0.001)])
    cover = union([cover] + [cyl(p["lid_boss_d"], hc - p["top"], x, y, z0) for x, y in p["lid_screws"]])
    pw, pl = p["panel"]
    cover = diff(cover, [prism(rounded_rect(pw, pl, p["panel_r"]), p["panel_depth"] + 1, z0 + hc - p["panel_depth"])]
                 + [cyl(3.6, 6.0, x, y, z0 - 0.5) for x, y in p["lid_screws"]])  # logement inserts M2.5
    return body, cover


def bracket_wpmb_m4():
    """Patte de fixation sur poteau Takachi WPMB-M4 (modèle simplifié, cotes du
    plan public) : bloc 28 x 18 x 12 mm, gorge en V côté poteau, insert M4 côté
    boîtier, 2 fentes pour le collier de serrage.

    Repère : face d'appui contre le boîtier en Z=0, gorge vers -Z (Z de -12 à 0),
    28 mm selon X, 18 mm selon Y (axe de la gorge = axe du poteau), centrée en X/Y.
    """
    from shapely.geometry import Polygon
    profile = Polygon([(-14, 0), (14, 0), (14, -12), (10.2, -12), (5, -7.4),
                       (-5, -7.4), (-10.2, -12), (-14, -12)])
    m = trimesh.creation.extrude_polygon(profile, 18.0)  # profil (x, z), extrudé selon Y
    m.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [1, 0, 0]))
    m.apply_translation([0, 9.0, 0])
    cutters = [cyl(5.6, 6.5, 0, 0, -6.0)]  # logement de l'insert M4
    for x in (-6.55, 6.55):                 # fentes du collier (entraxe 13.1)
        slot = trimesh.creation.box(extents=[2.5, 7.0, 30.0])
        slot.apply_translation([x, 0, -6.0])
        cutters.append(slot)
    return diff(m, cutters)


def main(ref):
    p = BOXES[ref]
    body, cover = build(p)
    out = Path(__file__).resolve().parent.parent / "docs/assets/3d_files/nebuleair_pro"
    out.mkdir(parents=True, exist_ok=True)
    stem = f"takachi_{ref}_simplifie"
    body.export(out / f"{stem}_corps_v1.stl")
    cover.export(out / f"{stem}_couvercle_v1.stl")

    # « G » = gris clair (white gray) ; matériau PBR pour un rendu propre sur le wiki
    for m, c in ((body, [205, 207, 208, 255]), (cover, [222, 224, 225, 255])):
        m.visual = trimesh.visual.TextureVisuals(material=trimesh.visual.material.PBRMaterial(
            baseColorFactor=c, metallicFactor=0.0, roughnessFactor=0.6))
    scene = trimesh.Scene()
    scene.add_geometry(body, node_name="corps", geom_name="corps")
    scene.add_geometry(cover, node_name="couvercle", geom_name="couvercle")
    # glTF : Y vers le haut, en mètres
    scene.apply_transform(trimesh.transformations.rotation_matrix(-np.pi / 2, [1, 0, 0]))
    scene.apply_scale(0.001)
    scene.export(out / f"{stem}_v1.glb")

    for name, m in (("corps", body), ("couvercle", cover)):
        ext = m.bounds[1] - m.bounds[0]
        print(f"{name}: étanche={m.is_watertight} dims={ext.round(2)} mm faces={len(m.faces)}")
    print("->", out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "WP13-18-5G")
