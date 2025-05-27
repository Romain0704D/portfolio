// Fonction pour ouvrir/fermer le menu latéral
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    sidebar.classList.toggle('open');
}

// Fonction pour ouvrir/fermer les sous-menus
function toggleMenu(menuId) {
    const menu = document.getElementById(menuId);
    const arrow = menu.previousElementSibling.querySelector('.arrow');
    
    // Fermer tous les autres menus
    document.querySelectorAll('.menu-content').forEach(content => {
        if (content.id !== menuId) {
            content.classList.remove('active');
            content.parentElement.querySelector('.arrow').classList.remove('rotated');
        }
    });
    
    // Toggle le menu actuel
    menu.classList.toggle('active');
    arrow.classList.toggle('rotated');
}

// Fonction pour afficher une section spécifique
function showSection(sectionId) {
    // Cacher toutes les sections
    document.querySelectorAll('.content-section').forEach(section => {
        section.classList.remove('active');
    });
    
    // Afficher la section sélectionnée
    document.getElementById(sectionId).classList.add('active');
    
    // Fermer le sidebar sur mobile
    if (window.innerWidth <= 768) {
        document.getElementById('sidebar').classList.remove('open');
    }
}

// Fermer le sidebar si on clique en dehors
document.addEventListener('click', function(event) {
    const sidebar = document.getElementById('sidebar');
    const menuBtn = document.querySelector('.menu-btn');
    
    if (!sidebar.contains(event.target) && !menuBtn.contains(event.target)) {
        sidebar.classList.remove('open');
    }
});

// Gestionnaire d'événements pour l'initialisation
document.addEventListener('DOMContentLoaded', function() {
    console.log('Portfolio BUT R&T - Site initialisé');
    
    // Initialiser la première section comme active si aucune n'est sélectionnée
    const activeSections = document.querySelectorAll('.content-section.active');
    if (activeSections.length === 0) {
        document.getElementById('page-garde').classList.add('active');
    }
});