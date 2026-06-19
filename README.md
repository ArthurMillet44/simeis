# Simeis

Jeu par API

## Membres du groupe
- Arthur MILLET
- Mathéo SOUCHET
- Bryan METRO
- Maxime KINIFFO

## Protection de la branche `main`

La branche `main` est protégée. Voir [.github/README.md](.github/README.md) pour le détail de la configuration et la commande utilisée.

Convention de nommage des branches

Le développement suit une convention de branches (`feature/*`, `bug/*`, `release/*`, `docs/*`), avec des règles précises sur quel type de branche peut être mergé dans quel autre. Cette convention est vérifiée automatiquement par le workflow `check-branch-type.yml`. Voir [.github/README.md](.github/README.md) pour le détail des règles appliquées.

## Worflows

Les différents workflows de ci sont expliqués dans le fichier [.github/workflows/README.md](.github/workflows/README.md).

### Build Rust multi-OS

Le workflow Rust CI (`.github/workflows/rust-ci.yml`) utilise une matrice de build pour vérifier que le projet compile en mode release sur plusieurs systèmes d'exploitation :

- `macos-latest`
- `ubuntu-latest`
- `windows-latest`

Le build est aussi testé avec plusieurs versions de Rust :

- `1.75.0`
- `1.80.0`
- `1.85.0`
- `1.88.0`

Cette matrice permet de détecter plus rapidement les problèmes spécifiques à un OS, par exemple des chemins de fichiers ou des commandes incompatibles entre Linux, Windows et macOS.

Pour rester compatible avec les anciennes versions de Rust testées dans la matrice, le serveur utilise `tokio` comme runtime par défaut. Le runtime `compio` reste disponible via la feature Cargo `compio`, mais il n'est pas activé par défaut.
