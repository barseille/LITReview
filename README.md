# LITReview

## Aperçu

LITReview est une application web destinée à deux principaux groupes d'utilisateurs :

- Ceux qui cherchent des critiques sur un livre ou un article spécifique
- Ceux qui recherchent des livres ou des articles intéressants à lire en fonction des critiques des autres

## Installation

### Cloner le projet : 

```
git clone https://github.com/barseille/LITReview.git
```

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
## Sur votre navigateur, entrer l'adresse suivant pour accéder au site : 

```
http://127.0.0.1:8000/
```

## Test de l'application

Vous pouvez vous connecter pour un test de l'application à l'aide de 3 utilisateurs au choix :

Nom d'utilisateur : barseille / Mot de passe : barseille
Nom d'utilisateur : tyson / Mot de passe : Jayden1234
Nom d'utilisateur : jayden / Mot de passe : Jayden1234


## Générer rapport Flake8

```
flake8 --format=html --htmldir=flake8_rapport
```