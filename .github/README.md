# Protection de la branche `main`

Le fichier `branch-protection-rules.json` contient la configuration de protection appliquée à la branche
`main` du dépôt, via l'API GitHub afin de
garder une trace.

## Règles appliquées

- Aucun push direct sur `main` : tout changement doit passer par une PR.

- Au moins 1 review obligatoire avant de pouvoir merger une PR
  (`required_approving_review_count: 1`).

- Les administrateurs du dépôt sont également soumis à ces règles (`enforce_admins: true`)

- Force push interdit sur `main` (`allow_force_pushes: false`).

- Suppression de la branche `main` interdite (`allow_deletions: false`).

## Comment appliquer la configuration

Avec l'outil `gh`, authentifié via `gh auth login` :

```bash
gh api --method PUT repos/<owner>/<repo>/branches/main/protection --input .github/branch-protection-rules.json
```

## CODEOWNERS

Le fichier `.github/CODEOWNERS` définit les propriétaires de code par dossier et permet à GitHub d'ajouter automatiquement les reviewers appropriés lorsqu'une PR modifie ces chemins.

- `/.github/` est attribué à `@ArthurMillet44`
- `/simeis-data/` est attribué à `@bryanmetro99`
- `/simeis-server/` est attribué à `@MaximeKiniffo`
- `/tests/` est attribué à `@DjoCaire`
