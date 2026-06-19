# Changelog

Tous les changements notables de ce projet sont documentés dans ce fichier.

## [v0.0.2]

### Changed
- **Workflow qualité de code** (`.github/workflows/check-code-quality.yml`)
  - Le workflow se déclenche désormais sur toutes les pull requests, quelle que soit la branche cible (auparavant limité aux PRs vers `main`)
- **Cache Rust**: remplacement de `Swatinem/rust-cache@v2` par `actions/cache@v4` dans tous les workflows pour une gestion manuelle du cache
- **Build Rust multi-OS** (`.github/workflows/rust-ci.yml`)
  - Ajout d'une matrice de build sur le job `build` pour compiler le projet sur `macos-latest`, `ubuntu-latest` et `windows-latest`
  - La matrice teste les versions Rust `1.75.0`, `1.80.0`, `1.85.0` et `1.88.0`
  - Les clés de cache Cargo utilisent l'OS du runner, le fichier `Cargo.lock` et les fichiers Rust racine
- **Runtime serveur par défaut** (`simeis-server/Cargo.toml`)
  - Remplacement du runtime par défaut `compio` par `tokio` pour garder le build compatible avec les anciennes versions Rust de la matrice CI
- **Suppression de dépendances inutilisées** :
  - `env_logger` retiré de `simeis-data`
  - `urlencoding` retiré de `simeis-server`

### Added
- **Workflow d'analyse avancée du code** (`.github/workflows/advanced-code-analysis.yml`)
  - Déclenché sur les pull requests ciblant une branche `release/*`
  - Tests unitaires avec la feature `heavy-testing`
  - Compilation du serveur en mode debug avec la feature `heavy-testing`
  - Squelette d'un script de tests fonctionnels lourds (`tests/heavy_tests.py`)
  - Audit de sécurité des dépendances via `cargo-audit`
  - Détection des dépendances inutilisées via `cargo-udeps`
- **Feature `heavy-testing`** dans `simeis-data` et `simeis-server`
  - Feature Cargo vide pour l'instant, destinée à activer les tests lourds dans le workflow d'analyse avancée

- **Workflows de dépendances**
  - Ajout d'un workflow `.github/workflows/dependencies.yml` pour mettre à jour automatiquement les dépendances Rust chaque semaine et créer une pull request si des modifications apparaissent.
- **CODEOWNERS**
  - Ajout d'un fichier `.github/CODEOWNERS` pour assigner automatiquement les propriétaires de répertoire à la revue des changements.

- **Templates de PR et d'issues** (`.github/templates/`)
  - Ajout de templates standardisés pour les pull requests (`pull_request_template.md`) et les issues (`issue_template.md`) pour harmoniser les contributions.

- **CI Rust parallèle** (`.github/workflows/rust-ci.yml`)
  - Ajout d'un workflow Rust dédié aux vérifications de formatage, compilation, lint, tests et build release.
  - Séparation des vérifications en jobs indépendants pour permettre leur exécution en parallèle.
  - **Optimisation du cache** : Intégration de `Swatinem/rust-cache@v2` dans tous les jobs pour mettre en cache les dépendances Cargo et les artifacts de compilation, réduisant significativement les temps de build.
  - **Optimisation de la parallélisation** : Ajout de dépendances `needs` entre les jobs pour un arrêt rapide (fail-fast). Les jobs `clippy`, `tests` et `build` dépendent maintenant du job `check`, évitant ainsi de lancer des tâches coûteuses si le code ne compile pas.

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
