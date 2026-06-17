# Vérification de la target branch

Dans le fichier `.github/workflows/check-pr-base.yml`, on vérifie que la PR vise bien le repo forké et non pas celui d'origine. En effet, sur github lors d'un fork, par défaut lorsqu'on ouvre une PR la branche dans laquelle va être mergé le contenu est celle du repository à l'origine du fork. Il est donc facile de se tromper si on ne pense pas explicitement à changer la branche cible. 
Ce fichier va donc permettre de vérifier cela pour nous en cas d"oubli.