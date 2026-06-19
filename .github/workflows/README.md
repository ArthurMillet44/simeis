# Vérification de la target branch

Dans le fichier `.github/workflows/check-pr-base.yml`, on vérifie que la PR vise bien le repo forké et non pas celui d'origine. En effet, sur github lors d'un fork, par défaut lorsqu'on ouvre une PR la branche dans laquelle va être mergé le contenu est celle du repository à l'origine du fork. Il est donc facile de se tromper si on ne pense pas explicitement à changer la branche cible. 
Ce fichier va donc permettre de vérifier cela pour nous en cas d"oubli.

# Vérification du type de branche (`check-branch-type.yml`)

Le fichier `.github/workflows/check-branch-type.yml` vérifie qu'une pull request respecte la convention de nommage des branches définie pour ce projet (`feature/*`, `bug/*`, `release/*`, `docs/*`), et surtout que le **type** de la branche source est cohérent avec le **type** de la branche cible.

Les règles appliquées sont les suivantes :

| Branche cible | Branches source autorisées |
| --- | --- |
| `main` | `feature/*`, `bug/*`, `docs/*` |
| `feature/*` | `feature/*`, `bug/*`, `docs/*` |
| `bug/*` | `bug/*` uniquement |
| `release/*` | `bug/*` uniquement |
| `docs/*` | `docs/*` uniquement |

Concrètement, le workflow extrait le préfixe (la partie avant le premier `/`) du nom de la branche source et de la branche cible de la pull request, puis compare cette combinaison à la table ci-dessus. Si la combinaison n'est pas autorisée, le check échoue.

## Pipeline CI/CD (ci.yml)

Le fichier `.github/workflows/ci.yml` configure un pipeline d'intégration continue et de déploiement qui s'exécute automatiquement sur les pull requests et les push vers la branche `main`. Il effectue des vérifications de qualité (check, clippy, tests), compile le projet, et génère le manuel. Lors d'un push sur `main`, il déclenche également une release optimisée.

## CI Rust parallèle (`rust-ci.yml`)

Le fichier `.github/workflows/rust-ci.yml` ajoute une CI dédiée au projet Rust. Il se déclenche sur les push vers `main` et les branches `feature/*`, ainsi que sur les pull requests qui ciblent `main`.

Le workflow sépare les vérifications Rust en plusieurs jobs indépendants afin qu'ils puissent être exécutés en parallèle :

1. **`fmt`** : vérifie le formatage du code avec `cargo fmt --check`.
2. **`check`** : vérifie rapidement que tout le workspace compile avec `cargo check --workspace`.
3. **`clippy`** : analyse la qualité du code avec `cargo clippy --workspace --all-targets -- -D warnings`.
4. **`tests`** : lance les tests Rust avec `cargo test`.
5. **`build`** : vérifie que le projet compile en mode release avec `cargo build --release`.

Cette séparation permet d'obtenir un retour plus clair et plus rapide : une erreur de formatage, de lint, de test ou de build apparaît dans un job dédié, sans attendre l'exécution séquentielle de toutes les commandes dans un seul job.

Par ailleurs, chaque job utilise `Swatinem/rust-cache@v2` pour mettre en cache les dépendances Cargo et les artifacts de compilation, réduisant ainsi considérablement les temps de build sur les exécutions suivantes.

### Stratégie de parallélisation et arrêt rapide

Le workflow utilise une stratégie de dépendances (`needs`) pour optimiser l'exécution et permettre un arrêt rapide en cas d'erreur :

1. **Jobs initiaux** (s'exécutent en parallèle immédiatement) :
   - `fmt` : vérifie le formatage du code
   - `check` : vérifie rapidement que le code compile

2. **Jobs dépendants** (s'exécutent uniquement si `check` réussit) :
   - `clippy` : analyse la qualité du code
   - `tests` : exécute les tests Rust
   - `build` : compile le projet en mode release

Cette approche permet un **arrêt rapide** (fail-fast) : si le code ne compile pas (`check` échoue), les jobs coûteux (`clippy`, `tests`, `build`) ne sont pas lancés, économisant ainsi du temps de CI et des ressources compute.
## Mise à jour automatique des dépendances (`dependencies.yml`)

Le fichier `.github/workflows/dependencies.yml` exécute une mise à jour automatique des dépendances Rust chaque semaine. Il :

1. s'exécute sur une planification hebdomadaire et peut être lancé manuellement via `workflow_dispatch` ;
2. installe `cargo-update` et lance `cargo upgrade` pour mettre à jour `Cargo.toml` et `Cargo.lock` ;
3. vérifie s'il y a eu des modifications et, si oui, crée automatiquement une pull request avec les changements de dépendances.

## Lancement des tests fonctionnels (`run-functional-test.yml`)

Le fichier `.github/workflows/run-functional-test.yml` exécute les tests fonctionnels du projet à chaque ouverture, modification ou mise à jour d'une pull request.

Le workflow effectue les étapes suivantes :

1. Installation de la toolchain Rust et des dépendances Python (`pytest`, `requests`).
2. Compilation du serveur (`cargo build -p simeis-server`).
3. Démarrage du serveur en arrière-plan (`cargo run -p simeis-server`), avec ses logs redirigés vers `server.log`.
4. Attente de la disponibilité du serveur, en interrogeant l'endpoint `http://localhost:8080/gamestats` jusqu'à 30 fois (1 seconde d'intervalle). Si le serveur n'est pas prêt après ce délai, le job échoue et affiche le contenu de `server.log` pour faciliter le diagnostic.
5. Exécution des tests fonctionnels avec `pytest tests/test_functional.py`, qui viennent valider le comportement du serveur via des requêtes HTTP.

# Qualité du code Rust (`check-code-quality.yml`)

Ce workflow vérifie la qualité du code Rust du projet. Il se déclenche :

- à chaque `push`, sur n'importe quelle branche
- à chaque pull request peu importe la branche.

Il effectue trois vérifications :

1. **`cargo check --all-targets`** : vérifie que le code compile correctement sans générer de binaire final.
2. **`cargo fmt --all -- --check`** : vérifie que le code respecte le formatage standard de `rustfmt`.
3. **`cargo clippy --all-targets -- -D warnings`** : lance Clippy, le linter de Rust, qui détecte les mauvais schémas de code.

Si l'une de ces trois étapes échoue, le workflow entier est en échec.

# Formatage des tests python

Le fichier `.github/workflows/check-code-quality.yaml` vérifie le formatage des scripts Python présents dans `tests/` via la commande `black --check tests/`. Black contrôle que le code respecte son style de formatage standard (longueur de ligne, lignes vides entre fonctions...). Si un fichier n'est pas conforme, le workflow échoue.

# Analyse avancée du code (`advanced-code-analysis.yml`)

Ce workflow effectue une analyse approfondie du code lors d'une pull request ciblant une branche `release/*`. Il exécute les étapes suivantes :

1. Lancement des tests unitaires avec la feature `heavy-testing` (`cargo test --features heavy-testing`).
2. Compilation du serveur en mode debug avec la feature `heavy-testing` (`cargo build -p simeis-server --features heavy-testing`).
3. Exécution du script de tests fonctionnels lourds (`tests/heavy_tests.py`).
4. Audit de sécurité des dépendances via `cargo audit`.
5. Détection des dépendances inutilisées via `cargo +nightly udeps --all-targets`.

# Propagation des branches bug (`bug-branch-analysis.yml`)

Ce workflow se déclenche lorsqu'une PR dont la branche source est `bug/*` est mergée. Pour chaque label de la forme `propagate:release/x` présent sur la PR, il crée automatiquement une PR de la branche `bug/*` vers la branche `release/x` correspondante.

# Couverture du code (`check-code-coverage.yml`)

Ce workflow vérifie la couverture de code grâce à l'outil `cargo-tarpaulin`. 
Il ce déclenche sur chaque pull request. Si la couverture est inférieur à 50%, un label `not enough tests` est ajouté sur la pull
request.