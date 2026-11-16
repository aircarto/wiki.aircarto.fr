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
      openV = v;
      renderDims();
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

    // --- Cotes du boîtier (fichier .dims.json écrit par le script d'assemblage) ---
    var dimsBox = box.querySelector(".viewer-3d-dims input[type=checkbox]");
    var dimsInfo = box.querySelector(".viewer-3d-dims-info");
    var dimsSvg = null, dimsLines = [], dimsOn = true, openV = 0;
    var en = (document.documentElement.lang || "").indexOf("en") === 0;

    function hs(name) { return mv.queryHotspot("hotspot-dim-" + name); }

    function renderDims() {
      if (!dimsSvg) return;
      // masquées capteur ouvert, et vues de dos (les cotes sont sur la face avant)
      var front = hs("wl");
      var show = dimsOn && openV < 0.02 && !(front && front.facingCamera === false);
      dimsSvg.style.display = show ? "" : "none";
      mv.querySelectorAll(".dim-label").forEach(function (el) { el.style.display = show ? "" : "none"; });
      if (!show) return;
      dimsLines.forEach(function (l) {
        var a = hs(l.a), b = hs(l.b);
        if (!a || !b) return;
        l.el.setAttribute("x1", a.canvasPosition.x); l.el.setAttribute("y1", a.canvasPosition.y);
        l.el.setAttribute("x2", b.canvasPosition.x); l.el.setAttribute("y2", b.canvasPosition.y);
      });
    }

    var dimsReady = false;
    function setupDims() {
      if (dimsReady) return; // « load » peut se redéclencher : une seule fois
      dimsReady = true;
      var url = (mv.getAttribute("src") || "").split("?")[0].replace(/\.glb$/, ".dims.json");
      fetch(url).then(function (r) { return r.ok ? r.json() : null; }).then(function (d) {
        if (!d || !d.boitier) return;
        var lo = d.boitier.min, hi = d.boitier.max, mm = d.boitier.mm;
        var off = 0.024, side = hi[0] + 0.022; // décalage des lignes hors du boîtier (AirVent, presse-étoupe)
        var P = {
          w1: [lo[0], lo[1] - off, hi[2]], w2: [hi[0], lo[1] - off, hi[2]],
          h1: [side, lo[1], hi[2]], h2: [side, hi[1], hi[2]],
          d1: [side, lo[1] - off, lo[2]], d2: [side, lo[1] - off, hi[2]],
        };
        function mid(a, b) { return [0, 1, 2].map(function (i) { return (a[i] + b[i]) / 2; }); }
        var labels = { wl: [mid(P.w1, P.w2), mm[0]], hl: [mid(P.h1, P.h2), mm[1]], dl: [mid(P.d1, P.d2), mm[2]] };
        function add(name, pos, cls, text) {
          var el = document.createElement("div");
          el.slot = "hotspot-dim-" + name;
          el.className = cls;
          el.dataset.position = pos.map(function (v) { return v.toFixed(5) + "m"; }).join(" ");
          el.dataset.normal = "0m 0m 1m"; // face avant : sert à savoir si on la voit
          if (text) el.textContent = text;
          mv.appendChild(el);
        }
        Object.keys(P).forEach(function (k) { add(k, P[k], "dim-dot"); });
        Object.keys(labels).forEach(function (k) { add(k, labels[k][0], "dim-label", labels[k][1] + " mm"); });
        var ns = "http://www.w3.org/2000/svg";
        dimsSvg = document.createElementNS(ns, "svg");
        dimsSvg.setAttribute("class", "dim-lines");
        [["w1", "w2"], ["h1", "h2"], ["d1", "d2"]].forEach(function (pair) {
          var line = document.createElementNS(ns, "line");
          dimsSvg.appendChild(line);
          dimsLines.push({ el: line, a: pair[0], b: pair[1] });
        });
        mv.appendChild(dimsSvg);
        if (dimsInfo) {
          var e = d.encombrement_mm.map(Math.round);
          dimsInfo.textContent = (en ? "Enclosure " : "Boîtier ") + d.boitier.ref + " : " + mm.join(" × ") + " mm" +
            (en ? " · overall size with vents, cable gland and brackets: " : " · encombrement avec AirVent, presse-étoupe et pattes : ") +
            e.join(" × ") + " mm";
        }
        if (dimsBox) {
          dimsBox.closest(".viewer-3d-dims").hidden = false;
          dimsBox.addEventListener("change", function () { dimsOn = dimsBox.checked; renderDims(); });
        }
        requestAnimationFrame(renderDims);
      });
    }
    // la visibilité des repères est mise à jour au rendu suivant : on recalcule aussi après
    mv.addEventListener("camera-change", function () { renderDims(); requestAnimationFrame(renderDims); });
    window.addEventListener("resize", function () { requestAnimationFrame(renderDims); });

    mv.addEventListener("load", function () {
      setupDims();
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
