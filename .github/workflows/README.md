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