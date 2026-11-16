# 3D models

!!! warning "Page under construction"
    This page is being worked on: the models and the position of the parts may still change.

View our sensors in 3D, right in your browser: **rotate** the model with your mouse or finger, **zoom** with the wheel or by pinching, and **open the sensor** with the slider below the model. On a phone, the button at the bottom right shows the sensor in augmented reality, placed in your room.

<script type="module" src="https://cdn.jsdelivr.net/npm/@google/model-viewer@3.5.0/dist/model-viewer.min.js"></script>

## NebuleAir Pro

**Vertical** (small) version: Takachi WP13-18-5G enclosure, NextPM particulate sensor and external BME280 probe. Three AirVent vents: one on each side and one on the front. The NextPM is mounted under the lid, its air inlet tube fitted into the front AirVent: open the sensor to see it. The power cord enters through a cable gland at the bottom right. It is shown mounted on a Ø60 mm pole with two Takachi WPMB-M4 brackets and two hose clamps.

<div class="viewer-3d">
<model-viewer data-open-m="0.13" src="../../assets/3d_files/nebuleair_pro/nebuleair_pro_WP13-18-5G_v1.glb?v=2b2bece0"
  alt="NebuleAir Pro, vertical version, in 3D"
  camera-controls touch-action="pan-y" auto-rotate auto-rotate-delay="3000"
  camera-orbit="40deg 70deg 0.72m" animation-crossfade-duration="0" shadow-intensity="1" exposure="1.0"
  ar ar-modes="webxr scene-viewer quick-look">
</model-viewer>
<div class="viewer-3d-open"><label>Open the sensor <input type="range" min="0" max="1" step="0.01" value="0"></label></div>
<div class="viewer-3d-flow" hidden><label><input type="checkbox"> Show the airflow</label></div>
<div class="viewer-3d-dims" hidden><label><input type="checkbox" checked> Show dimensions</label> <span class="viewer-3d-dims-info"></span></div>
</div>

The **"Show the airflow"** box shows the path of the air: it enters from below the front AirVent, is drawn in by the NextPM fan, then leaves the enclosure through the side AirVents. It illustrates the path; it is not a flow calculation.

!!! note "Enclosure and NextPM"
    The enclosure (Takachi **WP13-18-5G**, IP68) and the NextPM sensor (Tera Sensor) are off-the-shelf parts. The ones shown here are **simplified models redrawn by AirCarto** from the manufacturers' public dimensions, for display only.

### Files to print

| Part | Purpose | File |
|---|---|---|
| AirVent — cap | Vent: fits on the outside, opening facing down | [vent_top_v24.stl](../assets/3d_files/nebuleair_pro/vent_top_v24.stl) |
| AirVent — nut | Screws onto the cap from the inside, on either side of the 3 mm wall | [vent_ecrou_v10.stl](../assets/3d_files/nebuleair_pro/vent_ecrou_v10.stl) |

Hole to drill in the enclosure for one AirVent: **Ø16 mm**.

## Solar panel and battery

On a site without mains power, the NebuleAir Pro runs on a **solar panel** and a **battery**, mounted on the same pole as the sensor.

<div class="viewer-3d">
<model-viewer src="../../assets/3d_files/kit_solaire/nebuleair_pro_kit_solaire_v1.glb?v=04f06b5e"
  alt="NebuleAir Pro with solar panel and battery on a pole, in 3D"
  camera-controls touch-action="pan-y" auto-rotate auto-rotate-delay="3000"
  camera-orbit="40deg 78deg auto" shadow-intensity="1" exposure="1.0"
  ar ar-modes="webxr scene-viewer quick-look">
</model-viewer>
</div>

| Part | Specifications |
|---|---|
| Solar panel | 50 W, 12 V, monocrystalline · 670 × 460 × 30 mm · 3.2 kg |
| Panel mount | Aluminium, 45° tilt, fixed with 2 stainless hose clamps (pole up to Ø80 mm) |
| Battery | RE-LION® Solar Powerbox PERF 120 · 120 Wh lithium-ion (11.1 V) · built-in solar charger and BMS · IP65 · 270 × 150 × 85 mm |
| Wiring | 5 V and 12 V outputs on screw-lock connectors; the sensor is connected to the 12 V output through its cable gland |

**Autonomy.** The NebuleAir Pro draws about **0.5 W**: the battery alone lasts about ten days without sun (120 Wh ÷ 0.5 W ≈ 240 h). According to RE-LION® simulations based on sunshine data since 2005, a 0.6 W device runs all year without interruption, even in the worst year: in Marseille with a panel from 25 W, in Lille with the 50 W panel.

!!! note "Simplified models"
    The panel, its mount and the battery are **simplified models redrawn by AirCarto** from the manufacturers' public dimensions, for display only.
