# Rapport de Projet : Sacha GALLEZ & Romain DUBOC

## 1. Choix réalisés

### Choix sur la fiche : 'pokestats'

Le sujet des différentes statistiques des Pokémon dans une zone était intéressant, car, étant petits, nous nous sommes toujours demandés quels Pokémon s'y abritaient, etc. Cela nous a souvent conduit à des recherches sur Internet, alors qu'ici, cela nous a permis d'automatiser le processus et de le rendre plus rapide. Nous pouvons y retrouver les statistiques suivantes :
- Le nom de la zone ;
- Le ou les jeux ainsi que leurs régions ;
- Le nom et les identifiants des Pokémon dans cette zone ;
- Les talents et types de ces Pokémon ;
- La moyenne des types ressemblants ;
- La moyenne des types seuls ;
- La moyenne des types en double ;

### Choix techniques pertinents

L'utilisation de fonctions telles que isinstance(), next(), set() ou encore zip() visait à optimiser les performances et à permettre la production d'un code plus simple et plus fonctionnel.

- isinstance() permet de vérifier le type de l'objet à l'intérieur ;
- next() permet de prendre l'élément suivant d'un itérateur ;
- set() permet de supprimer les doublons dans une liste ;
- zip() permet de regrouper des objets en un seul itérateur.

Par exemple, l'une des utilisations importantes de ces fonctions se trouve dans la fiche pokestats.py, où l'on souhaite calculer la moyenne des types, et où l'on utilise la fonction set().


## 2. Difficultés rencontrées et solutions trouvées

### Difficultés & solutions

- **L'utilisation des dictionnaires :** Dans ce projet, il y a eu énormément de dictionnaires, avec aussi des dictionnaires de dictionnaires, etc. Cela a été compliqué à manipuler, mais avec le temps, cela est devenu plus simple.
  
- **Manipulation d'une API :** Étant un sujet nouveau, il a été tout aussi complexe à manipuler qu'à utiliser, compte tenu de la quantité de données fournies par l'API.


- **Optimisation du code:** Nous avons eu beaucoup de problèmes avec nos fonctions, notamment des répétitions, de la latence, des bugs, etc. Grâce à nos recherches, nous avons utilisé, par exemple, ces nouvelles fonctions et méthodes de code.

## 3. Ce que j'ai appris

Ce projet nous a permis d'être plus à l'aise avec l'utilisation d'une API et la manipulation des dictionnaires. De plus, désormais, nous savons transformer un code Python en fichier Markdown et, à partir de ce dernier, le convertir en fichier HTML.

## 4. État d'avancement du projet

Le projet est fonctionnel. Il est possible d'utiliser la fonction convert pour transformer un fichier Markdown en fichier HTML, bien qu'elle n'ait pas été utilisée dans nos codes Python. Ce choix a été fait pour pouvoir personnaliser nos pages HTML. Il est également possible d'utiliser la fonction ou bien d'utiliser le terminal de commande pour son utilisation. Cela est également le cas pour les fichiers pokefiche.py et pokestats.py. La fonction fiche_pokemon() peut aussi être utilisée. Pour le fichier pokestats.py, une commande start() a été développée. La traduction quasi-complète a été effectuée, mais l'implémentation d'un cache est manquante par manque de temps. Le retard dans la remise de ce projet est dû au fait qu'il y a eu quelques problèmes par rapport aux codes et à quelques soucis d'oubli.

