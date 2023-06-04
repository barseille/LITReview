# LITReview

## Aperçu

LITReview est une application web destinée à deux principaux groupes d'utilisateurs :

- Ceux qui cherchent des critiques sur un livre ou un article spécifique
- Ceux qui recherchent des livres ou des articles intéressants à lire en fonction des critiques des autres

## Installation

### Créer un environnement virtuel : 

```
python -m venv env
```

### Activer l'environnement virtuel avec Powershell :

```
env/Scripts/Activate.ps1
```

### Installer les paquets Python répertoriés dans le fichier requirements.txt :

```
pip install -r requirements.txt
```

*Cette commande installera tous les packages nécessaires à l'application. Aucune installation manuelle n'est nécessaire.

### Configuration de la base de données

```
python manage.py migrate
```

### Exécution du serveur de développement

```
python manage.py runserver
```

## Test de l'application

Vous pouvez vous connecter pour un test de l'application en utilisant les informations de connexion suivantes :

```
username : barseille
password : barseille
```
