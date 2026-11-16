// Visualiseur 3D (page Modèles 3D) : curseur « Ouvrir le capteur ».
// Le GLB contient une animation « ouverture » (couvercle qui s'éloigne du fond) ;
// le curseur fixe sa position au lieu de la jouer.
document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".viewer-3d").forEach(function (box) {
    var mv = box.querySelector("model-viewer");
    var range = box.querySelector(".viewer-3d-open input[type=range]");
    if (!mv || !range) return;
    var controls = range.closest(".viewer-3d-open");
    controls.hidden = true;
    mv.addEventListener("load", function () {
      if ((mv.availableAnimations || []).indexOf("ouverture") === -1) return;
      mv.animationName = "ouverture";
      mv.pause();
      controls.hidden = false;
    });
    range.addEventListener("input", function () {
      mv.autoRotate = false;
      // la fin exacte de l'animation est ramenée à 0 par model-viewer : on s'arrête juste avant
      var d = mv.duration || 1;
      var v = parseFloat(range.value);
      mv.currentTime = Math.min(v * d, d - 0.001);
      // la caméra suit l'ouverture : elle vise le milieu entre fond et couvercle
      var open = parseFloat(mv.dataset.openM || "0");
      if (open) mv.cameraTarget = "0m 0m " + (v * open / 2).toFixed(4) + "m";
    });
  });
});
