"""Kit solaire du NebuleAir Pro, pour la vue 3D du wiki : sur un même poteau,
le capteur (assemblage de nebuleair_pro_assemblage.py), la batterie RE-LION®
Solar Powerbox PERF 120 en dessous et le panneau solaire 50 W sur son support
incliné à 45° au-dessus.

Modèles SIMPLIFIÉS, redessinés à partir des dimensions publiques :
  - panneau 50 W 12 V monocristallin : 670 x 460 x 30 mm (670 dans la pente) ;
  - batterie PERF 120 : 270 x 150 x 85 mm (fiche technique RE-LION®) ;
  - support : rail vertical sur le poteau (2 colliers), rail incliné à 45°,
    2 traverses sous le panneau, jambe de force horizontale.

Usage :
    ~/.venvs/cad3d/bin/python scripts_3d/kit_solaire_assemblage.py

Sortie : docs/assets/3d_files/kit_solaire/nebuleair_pro_kit_solaire_v1.glb

Repère : celui du capteur (mm) : X = largeur, Y = haut, Z = vers l'avant ;
dos du boîtier du capteur en Z=0, poteau derrière (axe en Z≈-40).
"""
from pathlib import Path

import numpy as np
import trimesh
from shapely.geometry import MultiPoint, Point, box

import nebuleair_pro_assemblage as na
from takachi_wp import BOXES, bracket_wpmb_m4, cyl, rounded_rect

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs/assets/3d_files/kit_solaire"

# --- Panneau ---------------------------------------------------------------
PANEL_W, PANEL_L, PANEL_T = 460.0, 670.0, 30.0   # largeur (X), longueur dans la pente, épaisseur
PANEL_FRAME = 20.0                                # largeur du cadre alu vu de face
PANEL_CELLS = (4, 9)                              # 36 cellules (12 V)
TILT_DEG = 45.0
# --- Support ---------------------------------------------------------------
RAIL_W, RAIL_T = 41.0, 21.0                       # profilé alu
POLE_RAIL_Y = (250.0, 650.0)                      # rail vertical sur le poteau
SLOPE_RAIL_LEN = 560.0
CROSS_RAIL_V = (-150.0, -520.0)                   # traverses sous le panneau (le long de la pente)
# --- Batterie --------------------------------------------------------------
BAT_W, BAT_H, BAT_D = 150.0, 270.0, 85.0
BAT_TOP_Y = -230.0
BAT_PLATE = 3.0                                   # platine de fixation au dos
# --- Poteau ----------------------------------------------------------------
POLE_Y = (-660.0, 720.0)
CABLE_D = 6.0

COLORS = {
    "alu": [176, 181, 186, 255],
    "cadre": [150, 155, 160, 255],
    "cellules": [24, 38, 74, 255],
    "fond_panneau": [225, 227, 230, 255],
    "boite_jonction": [30, 31, 34, 255],
    "batterie": [58, 62, 68, 255],
    "batterie_face": [78, 84, 92, 255],
    "connecteur": [25, 26, 28, 255],
    "inox": [200, 204, 208, 255],
    "cable": [22, 23, 25, 255],
}
GRID_COLOR = [150, 165, 190, 255]


def paint(m, key, metal=0.0, rough=0.6):
    m.visual = trimesh.visual.TextureVisuals(material=trimesh.visual.material.PBRMaterial(
        baseColorFactor=COLORS[key], metallicFactor=metal, roughnessFactor=rough))
    return m


def add(scene, name, mesh, key, edges=True, **mat):
    scene.add_geometry(paint(mesh, key, **mat), node_name=name, geom_name=name)
    if edges:
        scene.add_geometry(na.edges(mesh), node_name=f"{name}_aretes", geom_name=f"{name}_aretes")


def slab(x0, x1, y0, y1, z0, z1):
    m = trimesh.creation.box(extents=[x1 - x0, y1 - y0, z1 - z0])
    m.apply_translation([(x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2])
    return m


def tube(points, d, sections=24):
    """Câble : cercle balayé le long d'une polyligne lissée."""
    pts = na._chaikin(points, 4)
    return trimesh.creation.sweep_polygon(Point(0, 0).buffer(d / 2, quad_segs=sections // 4), pts)


def pole_band(zc, r, y, pts_front, w=9.0, t=0.8):
    """Collier inox autour du poteau et d'une pièce plaquée devant (points x, z)."""
    hull = Point(0, zc).buffer(r, quad_segs=64).union(MultiPoint(pts_front)).convex_hull
    band = hull.buffer(t, quad_segs=16).difference(hull)
    m = trimesh.creation.extrude_polygon(band, w)
    m.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [1, 0, 0]))
    m.apply_translation([0, y + w / 2, 0])
    screw = trimesh.creation.box(extents=[14.0, w + 3.0, 7.0])  # vis sans fin, derrière le poteau
    screw.apply_translation([0, y, zc - r - t - 3.0])
    return trimesh.util.concatenate([m, screw])


def panel_frame_matrix(origin):
    """Repère local du panneau -> repère du kit. Local : u = X, v = vers le haut
    de la pente (v<0 en descendant), w = normale (vers le ciel et l'avant)."""
    a = np.radians(TILT_DEG)
    ey = np.array([0.0, np.sin(a), -np.cos(a)])   # vers le haut de la pente (vers le poteau)
    ez = np.array([0.0, np.sin(a), np.cos(a)])    # normale du panneau
    T = np.eye(4)
    T[:3, :3] = np.column_stack([[1.0, 0.0, 0.0], ey, ez])
    T[:3, 3] = origin
    return T


def panel_parts():
    """Panneau dans son repère local : v de -PANEL_L à 0 (bord haut à v=0),
    dos du cadre en w=0, face avant en w=PANEL_T."""
    W, L, T, F = PANEL_W, PANEL_L, PANEL_T, PANEL_FRAME
    outer = box(-W / 2, -L, W / 2, 0)
    inner = box(-W / 2 + F, -L + F, W / 2 - F, -F)
    ring = outer.difference(inner)
    frame = trimesh.creation.extrude_polygon(ring, T)
    lip = trimesh.creation.extrude_polygon(box(-W / 2 + F, -L + F, W / 2 - F, -F).difference(
        box(-W / 2 + F + 6, -L + F + 6, W / 2 - F - 6, -F - 6)), 3.0)   # rebord qui tient le verre
    lip.apply_translation([0, 0, T - 5.0])
    frame = trimesh.util.concatenate([frame, lip])
    cells = trimesh.creation.extrude_polygon(inner, 3.2)
    cells.apply_translation([0, 0, T - 5.5])
    back = trimesh.creation.extrude_polygon(inner, 0.8)
    back.apply_translation([0, 0, T - 6.3])
    jbox = slab(-45, 45, -110, -40, T - 6.3 - 18, T - 6.3)
    # quadrillage des cellules (traits), juste au-dessus du verre
    nx, ny = PANEL_CELLS
    x0, x1, y0, y1 = -W / 2 + F + 6, W / 2 - F - 6, -L + F + 6, -F - 6
    z = T - 2.2
    segs = [[[x, y0, z], [x, y1, z]] for x in np.linspace(x0, x1, nx + 1)[1:-1]]
    segs += [[[x0, y, z], [x1, y, z]] for y in np.linspace(y0, y1, ny + 1)[1:-1]]
    return frame, cells, back, jbox, np.array(segs)


def main():
    p = BOXES[na.REF]
    scene, _ = na.sensor_scene(p)
    sensor_bounds = scene.bounds.copy()
    zc, r = na.add_pole(scene, p, length=POLE_Y[1] - POLE_Y[0], y_mid=sum(POLE_Y) / 2)
    front = zc + r                                   # devant du poteau (Z)

    # --- Batterie RE-LION® PERF 120, sous le capteur ----------------------
    bat_y0, bat_y1 = BAT_TOP_Y - BAT_H, BAT_TOP_Y
    bracket = bracket_wpmb_m4()                      # même calage en V que le capteur
    for y in (bat_y0 + 40.0, bat_y1 - 40.0):
        m = bracket.copy()
        m.apply_translation([0, y, 0])
        tag = "bas" if y < (bat_y0 + bat_y1) / 2 else "haut"
        add(scene, f"batterie_support_{tag}", m, "alu", metal=0.6, rough=0.4)
        add(scene, f"batterie_collier_{tag}", na.strap_mesh(zc, r, y), "inox", edges=False, metal=0.8, rough=0.3)
    plate = slab(-55, 55, bat_y0 + 15, bat_y1 - 15, 0, BAT_PLATE)
    add(scene, "batterie_platine", plate, "inox", metal=0.7, rough=0.35)
    z0 = BAT_PLATE
    body = trimesh.creation.extrude_polygon(rounded_rect(BAT_W, BAT_H, 8.0), BAT_D)
    body.apply_translation([0, (bat_y0 + bat_y1) / 2, z0])
    add(scene, "batterie", body, "batterie", rough=0.5)
    lid = trimesh.creation.extrude_polygon(rounded_rect(BAT_W - 24, BAT_H - 24, 4.0), 1.0)
    lid.apply_translation([0, (bat_y0 + bat_y1) / 2, z0 + BAT_D])
    add(scene, "batterie_face", lid, "batterie_face", rough=0.45)
    # connecteurs dessous : entrée solaire, sortie 5 V (bouchée), sortie 12 V (capteur)
    conns = {"solaire": -45.0, "sortie_5v": 0.0, "sortie_12v": 45.0}
    zconn = z0 + BAT_D / 2
    for name, x in conns.items():
        c = cyl(16.0, 14.0, 0, 0, 0)
        c = trimesh.util.concatenate([c, cyl(20.0, 4.0, 0, 0, 0)])
        c.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [1, 0, 0]))  # axe -Y
        c.apply_translation([x, bat_y0, zconn])
        add(scene, f"batterie_connecteur_{name}", c, "connecteur")

    # --- Support du panneau -------------------------------------------------
    ry0, ry1 = POLE_RAIL_Y
    rail = slab(-RAIL_W / 2, RAIL_W / 2, ry0, ry1, front, front + RAIL_T)
    add(scene, "support_rail_poteau", rail, "alu", metal=0.6, rough=0.4)
    for y in (ry0 + 35.0, ry1 - 45.0):
        band = pole_band(zc, r, y, [(-RAIL_W / 2, front + RAIL_T), (RAIL_W / 2, front + RAIL_T)])
        add(scene, f"support_collier_{int(y)}", band, "inox", edges=False, metal=0.8, rough=0.3)
    hinge = np.array([0.0, ry1, front + RAIL_T])        # articulation en haut du rail
    Tp = panel_frame_matrix(hinge)

    def local(m):
        m = m.copy()
        m.apply_transform(Tp)
        return m

    slope = local(slab(-RAIL_W / 2, RAIL_W / 2, -SLOPE_RAIL_LEN, 0, 0, RAIL_T))
    add(scene, "support_rail_incline", slope, "alu", metal=0.6, rough=0.4)
    bolt = cyl(8.0, RAIL_W + 16, 0, 0, -(RAIL_W + 16) / 2)
    bolt.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [0, 1, 0]))
    bolt.apply_translation(hinge + [0, -4.0, 4.0])
    add(scene, "support_articulation", bolt, "inox", edges=False, metal=0.8, rough=0.3)
    for i, v in enumerate(CROSS_RAIL_V):
        cr = local(slab(-PANEL_W / 2 + 8, PANEL_W / 2 - 8, v - RAIL_W / 2, v + RAIL_W / 2, RAIL_T, 2 * RAIL_T))
        add(scene, f"support_traverse_{i}", cr, "alu", metal=0.6, rough=0.4)
    # jambe de force : du bas du rail vertical jusqu'au rail incliné, à l'horizontale
    y_strut = ry0 + 15.0
    a = np.radians(TILT_DEG)
    s = (hinge[1] - y_strut) / np.sin(a)                 # distance le long de la pente
    z_end = hinge[2] + s * np.cos(a)
    strut = cyl(12.0, z_end - (front + RAIL_T), 0, 0, 0)
    strut.apply_translation([0, y_strut, front + RAIL_T])
    add(scene, "support_jambe_de_force", strut, "alu", edges=False, metal=0.6, rough=0.4)

    # --- Panneau ------------------------------------------------------------
    frame, cells, back, jbox, grid = panel_parts()
    w0 = 2 * RAIL_T                                       # posé sur les traverses
    shift = trimesh.transformations.translation_matrix([0, 25.0, w0])  # bord haut un peu au-dessus de l'articulation
    for name, m, key, kw in (("panneau_cadre", frame, "cadre", dict(metal=0.6, rough=0.35)),
                             ("panneau_cellules", cells, "cellules", dict(metal=0.2, rough=0.15)),
                             ("panneau_fond", back, "fond_panneau", {}),
                             ("panneau_boite_jonction", jbox, "boite_jonction", {})):
        m = m.copy()
        m.apply_transform(shift)
        add(scene, name, local(m), key, edges=name != "panneau_cellules", **kw)
    g = np.c_[grid.reshape(-1, 3), np.ones(len(grid) * 2)] @ (Tp @ shift).T
    path = trimesh.load_path(g[:, :3].reshape(-1, 2, 3))
    path.colors = np.tile(GRID_COLOR, (len(path.entities), 1))
    scene.add_geometry(path, node_name="panneau_quadrillage", geom_name="panneau_quadrillage")

    # --- Câbles -------------------------------------------------------------
    # 12 V batterie -> presse-étoupe du capteur (boucle sous la batterie, remonte sur le côté)
    gy = -p["length"] / 2 - na.GLAND_OUT
    x12 = conns["sortie_12v"]
    pts = [(x12, bat_y0 - 14, zconn), (x12, bat_y0 - 60, zconn), (BAT_W / 2 + 25, bat_y0 - 60, zconn),
           (BAT_W / 2 + 25, bat_y0 + 40, zconn), (BAT_W / 2 + 25, bat_y1 + 30, zconn - 10),
           (na.GLAND_X, gy - 50, na.GLAND_Z), (na.GLAND_X, gy, na.GLAND_Z)]
    add(scene, "cable_batterie_capteur", tube(pts, CABLE_D), "cable", edges=False)
    # panneau -> entrée solaire : boîte de jonction, long du poteau (côté gauche), sous la batterie
    jb = (Tp @ shift @ np.array([-30.0, -75.0, PANEL_T - 6.3 - 18, 1.0]))[:3]
    xs = conns["solaire"]
    side = -(r + CABLE_D / 2 + 1)
    pts = [jb, (jb[0], jb[1] - 60, jb[2] - 60), (side, ry0 - 20, zc + 8), (side, 120, zc),
           (side, bat_y0 - 40, zc + 10), (xs, bat_y0 - 60, zconn), (xs, bat_y0 - 14, zconn)]
    add(scene, "cable_panneau_batterie", tube(pts, CABLE_D), "cable", edges=False)

    # Centre de la vue : tout sauf le poteau
    lo = np.minimum(sensor_bounds[0], [-PANEL_W / 2, bat_y0 - 70, zc - r])
    hi = np.maximum(sensor_bounds[1], [PANEL_W / 2, hinge[1] + 60, z_end + 60])
    centre = (lo + hi) / 2
    scene.apply_translation(-centre)
    scene.apply_scale(0.001)
    OUT.mkdir(parents=True, exist_ok=True)
    out = OUT / "nebuleair_pro_kit_solaire_v1.glb"
    scene.export(out)
    print(f"encombrement (hors poteau) : {(hi - lo).round(0)} mm")
    print("->", out, f"{out.stat().st_size / 1024:.0f} Ko")
    na.stamp_pages(out)


if __name__ == "__main__":
    main()
