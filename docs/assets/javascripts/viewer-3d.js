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
      mv.currentTime = parseFloat(range.value) * (mv.duration || 1);
    });
  });
});
