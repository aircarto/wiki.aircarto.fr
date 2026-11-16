# 3D models

!!! warning "Page under construction"
    This page is being worked on: the models and the position of the parts may still change.

View our sensors in 3D, right in your browser: **rotate** the model with your mouse or finger, **zoom** with the wheel or by pinching. On a phone, the button at the bottom right shows the sensor in augmented reality, placed in your room.

<script type="module" src="https://cdn.jsdelivr.net/npm/@google/model-viewer@3.5.0/dist/model-viewer.min.js"></script>

## NebuleAir Pro

**Vertical** (small) version: Takachi WP13-18-5G enclosure, NextPM particulate sensor and external BME280 probe. Three AirVent vents: one on each side and one on the front.

<div class="viewer-3d">
<model-viewer src="../../assets/3d_files/nebuleair_pro/nebuleair_pro_WP13-18-5G_v1.glb"
  alt="NebuleAir Pro, vertical version, in 3D"
  camera-controls touch-action="pan-y" auto-rotate auto-rotate-delay="3000"
  camera-orbit="35deg 70deg auto" shadow-intensity="1" exposure="1.1"
  ar ar-modes="webxr scene-viewer quick-look">
</model-viewer>
</div>

!!! note "Enclosure"
    The enclosure is an off-the-shelf part (Takachi **WP13-18-5G**, IP68). The one shown here is a **simplified model redrawn by AirCarto** from the manufacturer's public dimensions, for display only: the enclosure itself is bought from Takachi.

### Files to print

| Part | Purpose | File |
|---|---|---|
| AirVent — cap | Vent: fits on the outside, opening facing down | [vent_top_v24.stl](../assets/3d_files/nebuleair_pro/vent_top_v24.stl) |
| AirVent — nut | Screws onto the cap from the inside, on either side of the 3 mm wall | [vent_ecrou_v10.stl](../assets/3d_files/nebuleair_pro/vent_ecrou_v10.stl) |

Hole to drill in the enclosure for one AirVent: **Ø16 mm**.
