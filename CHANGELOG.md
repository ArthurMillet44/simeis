# Changelog

Tous les changements notables de ce projet sont documentés dans ce fichier.

## [v0.0.2]

### Changed
- **Workflow qualité de code** (`.github/workflows/check-code-quality.yml`)
  - Le workflow se déclenche désormais sur toutes les pull requests, quelle que soit la branche cible (auparavant limité aux PRs vers `main`)
  - Ajout d'un cache des dépendances Rust via `Swatinem/rust-cache@v2` pour accélérer les builds suivants
- Ajout d'un cache partagé entre les pull requests

### Added
- **Workflows de dépendances**
  - Ajout d'un workflow `.github/workflows/dependencies.yml` pour mettre à jour automatiquement les dépendances Rust chaque semaine et créer une pull request si des modifications apparaissent.
- **CODEOWNERS**
  - Ajout d'un fichier `.github/CODEOWNERS` pour assigner automatiquement les propriétaires de répertoire à la revue des changements.

- **CI Rust parallèle** (`.github/workflows/rust-ci.yml`)
  - Ajout d'un workflow Rust dédié aux vérifications de formatage, compilation, lint, tests et build release.
  - Séparation des vérifications en jobs indépendants pour permettre leur exécution en parallèle.

- **Workflow de couverture de test**
  - Ajout d'un workflow `.github/workflows/check-code-coverage.yml` pour permettre de vérifier la couverture de test et de signaler si elle est inférieur à 50%.

## [v0.0.1]

### Added
- **Workflow qualité de code**
  - Ajout d'un workflow pour la qualité du code rust et des tests python : `.github/workflows/check-code-quality.yml`

- **Workflow branches**
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