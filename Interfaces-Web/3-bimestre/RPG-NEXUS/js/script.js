// ==============================
// RPG NEXUS - JAVASCRIPT
// ==============================

console.log("RPG Nexus iniciado.");

// Efeito simples na navbar
window.addEventListener("scroll", function () {

    const navbar = document.querySelector(".navbar");

    if (window.scrollY > 50) {

        navbar.style.background =
            "rgba(5, 6, 9, 0.98)";

    } else {

        navbar.style.background =
            "rgba(8, 9, 13, 0.9)";

    }

});