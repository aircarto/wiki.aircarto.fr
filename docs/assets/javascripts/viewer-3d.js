// Visualiseur 3D (page Modèles 3D) : curseur « Ouvrir le capteur ».
// Le GLB contient une animation « ouverture » (vue éclatée : le couvercle et
// les pièces qui y sont fixées s'éloignent du fond) ; le curseur fixe sa
// position au lieu de la jouer. À l'arrivée sur le modèle, le capteur apparaît
// ouvert puis se referme doucement (le curseur suit), sauf si l'utilisateur
// touche au modèle ou au curseur avant.
document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".viewer-3d").forEach(function (box) {
    var mv = box.querySelector("model-viewer");
    var range = box.querySelector(".viewer-3d-open input[type=range]");
    if (!mv || !range) return;
    var controls = range.closest(".viewer-3d-open");
    controls.hidden = true;
    var intro = null; // animation d'introduction en cours (id requestAnimationFrame)

    function apply(v) {
      // la fin exacte de l'animation est ramenée à 0 par model-viewer : on s'arrête juste avant
      var d = mv.duration || 1;
      mv.currentTime = Math.min(v * d, d - 0.001);
      // la caméra suit l'ouverture : elle vise le milieu entre fond et couvercle
      var open = parseFloat(mv.dataset.openM || "0");
      if (open) mv.cameraTarget = "0m 0m " + (v * open / 2).toFixed(4) + "m";
    }

    function stopIntro() {
      if (intro) cancelAnimationFrame(intro);
      intro = null;
    }

    function playIntro() {
      var hold = 700, dur = 2600, t0 = null;
      range.value = 1;
      apply(1);
      function step(now) {
        if (t0 === null) t0 = now;
        var k = Math.min(Math.max((now - t0 - hold) / dur, 0), 1);
        var v = 1 - (1 - Math.cos(Math.PI * k)) / 2; // ralenti au début et à la fin
        range.value = v;
        apply(v);
        intro = k < 1 ? requestAnimationFrame(step) : null;
      }
      intro = requestAnimationFrame(step);
    }

    mv.addEventListener("load", function () {
      if ((mv.availableAnimations || []).indexOf("ouverture") === -1) return;
      mv.animationName = "ouverture";
      mv.pause();
      controls.hidden = false;
      var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
      if (reduce) return;
      // démarre quand le visualiseur est visible à l'écran
      if ("IntersectionObserver" in window) {
        var io = new IntersectionObserver(function (entries) {
          if (entries.some(function (e) { return e.isIntersecting; })) {
            io.disconnect();
            setTimeout(playIntro, 50); // laisse model-viewer appliquer l'animation choisie
          }
        }, { threshold: 0.4 });
        io.observe(mv);
      } else {
        setTimeout(playIntro, 50);
      }
    });

    range.addEventListener("input", function () {
      stopIntro();
      mv.autoRotate = false;
      apply(parseFloat(range.value));
    });
    mv.addEventListener("pointerdown", stopIntro);
  });
});
