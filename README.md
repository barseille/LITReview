# LITReview

## Aperçu

LITReview est une application web destinée à deux principaux groupes d'utilisateurs :

- Ceux qui cherchent des critiques sur un livre ou un article spécifique
- Ceux qui recherchent des livres ou des articles intéressants à lire en fonction des critiques des autres

## Installation

### Cloner le projet depuis votre éditeur de code: 

```
https://github.com/barseille/LITReview.git
```

### Créer un environnement virtuel : 

```
python -m venv env
```

### Activer l'environnement virtuel :

Pour Windows avec Powershell :

```
env/Scripts/Activate.ps1
```

Pour macOS ou Linux avec Bash :

```
source env/bin/activate

```
### Mise à jour "pip" si besoin à l'aide cette commande :

```
python -m pip install --upgrade pip
```

### Installer les paquets Python requis:

Avec l'environnement virtuel activé, installez les dépendances requises :

```
pip install -r requirements.txt
```

### Configuration de la base de données

Exécutez les migrations de la base de données avec :

```
python manage.py migrate
```

### Exécution du serveur de développement

```
python manage.py runserver
```

## Accéder à l'application : 

Dans votre navigateur web, accédez à l'application à l'adresse suivante :

```
http://127.0.0.1:8000/
```

## Test de l'application

Pour tester l'application, vous pouvez vous connecter avec l'un des comptes de test suivants :

- Nom d'utilisateur : barseille / Mot de passe : barseille

- Nom d'utilisateur : tyson / Mot de passe : Jayden1234

- Nom d'utilisateur : jayden / Mot de passe : Jayden1234

## Générer rapport Flake8

```
flake8 --format=html --htmldir=flake8_rapport
```