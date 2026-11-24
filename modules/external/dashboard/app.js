// app.js : les petites interactions du dashboard

// 1. Onglets des cartes interactives
// Chaque groupe de boutons (.onglets) commande une iframe, dont l'id est dans data-cible.
// Un clic sur un bouton affiche la carte indiquée dans son attribut data-carte.
document.querySelectorAll(".onglets").forEach(function (groupe) {
  var iframe = document.getElementById(groupe.dataset.cible);
  groupe.querySelectorAll("button").forEach(function (bouton) {
    bouton.addEventListener("click", function () {
      iframe.src = bouton.dataset.carte;
      groupe.querySelectorAll("button").forEach(function (b) { b.classList.remove("actif"); });
      bouton.classList.add("actif");
    });
  });
});

// 2. Menu : le lien de la section visible à l'écran est mis en couleur
var liens = document.querySelectorAll(".sidebar nav a");
var sections = Array.from(liens).map(function (lien) {
  return document.querySelector(lien.getAttribute("href"));
});

window.addEventListener("scroll", function () {
  var position = window.scrollY + 120;
  sections.forEach(function (section, i) {
    if (section && section.offsetTop <= position) {
      liens.forEach(function (l) { l.classList.remove("actif"); });
      liens[i].classList.add("actif");
    }
  });
});

// 3. Bouton pour ouvrir / fermer la barre latérale
var boutonMenu = document.getElementById("bouton-menu");

// sur un petit écran, la barre est fermée au départ
if (window.innerWidth < 900) {
  document.body.classList.add("menu-ferme");
}

boutonMenu.addEventListener("click", function () {
  document.body.classList.toggle("menu-ferme");
});

// sur un petit écran, cliquer sur un lien du menu referme la barre
document.querySelectorAll(".sidebar nav a").forEach(function (lien) {
  lien.addEventListener("click", function () {
    if (window.innerWidth < 900) {
      document.body.classList.add("menu-ferme");
    }
  });
});
