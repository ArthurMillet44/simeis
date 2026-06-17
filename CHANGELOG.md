# Changelog

Tous les changements notables de ce projet sont documentés dans ce fichier.

## [Unreleased]

### Added
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