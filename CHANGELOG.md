# Changelog

Tous les changements notables de ce projet sont documentés dans ce fichier.

## [v0.0.2]

### Added
- **Workflows de dépendances**
  - Ajout d'un workflow `.github/workflows/dependencies.yml` pour mettre à jour automatiquement les dépendances Rust chaque semaine et créer une pull request si des modifications apparaissent.


## [v0.0.1]

### Added
- **Workflows qualité de code**
  - Ajout d'un workflow pour la qualité du code rust et des tests python : `.github/workflows/check-code-quality.yml`

- **Workflows branches**
  - Ajout d'un workflow qui vérifie si la PR pointe vers le bon dépôt : `.github/workflows/check-pr-base.yml`
  - Ajour d'un workflow qui ajoute des règles sur les branches (par exemple sur une branche release seule les branches bugs peuvent effectuer une PR) : `.github/workflows/check-branch-type.yml`

- **Système CI/CD** (`.github/workflows/ci.yml`)
  - Pipeline GitHub Actions pour vérification automatique des pull requests
  - Workflow de release automatique sur push vers `main`
  - Tâches: check, test, build, et compilation du manuel
  - Support multi-plateforme avec installation de Typst

- **Makefile** pour simplifier les tâches de build et développement
  - `make all` - Exécute checks, tests, build et compilation du manuel
  - `make build` - Build le projet en mode debug
  - `make release` - Build optimisé pour la production (avec strip sur Unix)
  - `make clean` - Nettoie les artifacts de build
  - `make test` - Lance les tests unitaires
  - `make check` - Vérifie le code et exécute clippy
  - `make manual` - Compile le manuel au format PDF

### Changed
- **simeis-data/src/ship.rs** (ligne 355-359)
  - Remplacement de `assert!(false)` suivi de `unreachable!()` par un `panic!()` explicite
  - Message d'erreur plus clair: "This code path should never be reached"
  - Amélioration de la maintenabilité du test `test_ship_flight()`

- **simeis-server/src/api/crew.rs** (ligne 66)
  - Optimisation: remplacement de `args.clone()` par `*args` dans la fonction `fire_crew()`
  - Utilise le dereferencing automatique au lieu du clonage de la tuple
  - Amélioration de performance et réduction de l'allocation mémoire

### Technical Details
- Ajout d'un workflow de qualité avec Rust toolchain stable
- Installation automatique de Typst pour la compilation du manuel
- Intégration de cargo clippy pour les vérifications statiques
- Support Windows détecté dans le Makefile (pas de strip sur Windows)

### Test
- Ajout de 3 tests fonctionnel sur l'achat de vaisseaux et d'upgrade 
- Ajout d'un workflow pour le lancement des tests fonctionnels