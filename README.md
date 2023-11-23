# Module Servier
[![Ask Me Anything !](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ask Me Anything !](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10-blue)]()
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

Ce module Python contient l'intelligence qui sera utilisée lors du pipeline.

## Poetry
Ce module est développé avec Poetry pour éviter les problèmes de conflit de dépendances.

### Installation de Poetry
Pour installer Poetry localement, exécutez :
```bash
make poetry_install
```

### Environnement Virtuel
Une fois installé, il est impératif d'activer votre environnement virtuel :
```bash
make env
```

### Installation de Dépendances
Si c'est la première fois que vous configurez le projet, installez les dépendances avec :
```bash
make install
```

### Construction du Package
Pour intégrer une fonctionnalité au package, utilisez la commande :
```bash
make build
```

## Pre-commit
Pour appliquer automatiquement les bonnes pratiques de codage, installez pre-commit avec :
```bash
make pre_commit
```

## Tests
Ce module est testé avec pytest. Pour exécuter les tests, utilisez :
```bash
make test
```

## Documentation

### Génération de la Documentation

Ce module peut générer automatiquement la documentation lorsque le docstring des fonctions suit le format NumPy :
```bash
make docs
```

### Consultation de la documentation
Pour mieux comprendre le code en consultant la documentation du module, visitez [l'URL](https://jonathanndambapro.github.io/servier/docs/app.html)
