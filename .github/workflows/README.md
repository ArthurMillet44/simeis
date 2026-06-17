# Vérification de la target branch

Dans le fichier `.github/workflows/check-pr-base.yml`, on vérifie que la PR vise bien le repo forké et non pas celui d'origine. En effet, sur github lors d'un fork, par défaut lorsqu'on ouvre une PR la branche dans laquelle va être mergé le contenu est celle du repository à l'origine du fork. Il est donc facile de se tromper si on ne pense pas explicitement à changer la branche cible. 
Ce fichier va donc permettre de vérifier cela pour nous en cas d"oubli.

## Pipeline CI/CD (ci.yml)

Le fichier `.github/workflows/ci.yml` configure un pipeline d'intégration continue et de déploiement qui s'exécute automatiquement sur les pull requests et les push vers la branche `main`. Il effectue des vérifications de qualité (check, clippy, tests), compile le projet, et génère le manuel. Lors d'un push sur `main`, il déclenche également une release optimisée.

