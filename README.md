## Étape 0 : Installer les librairies

```
pip install -r requirements.txt
```
## Étape 1 : Crée la varibale d'environnement 

Sous Windows/macOS/Linux :
```
set FLASK_APP=app.py
```

## Étape 2 : Vérifie ensuite que la variable a été bien définie 

```
echo $FLASK_APP  # Sous macOS/Linux
echo %FLASK_APP%  # Sous Windows
```

## Étape 3 : Exécuter flask init-db
Lance la commande suivante pour initialiser la base de données :
```
flask init-db
```

## Étape 4 : Lancer app.py
```
flask run
```
Tu pourras y accéder à l'url suivant : http://127.0.0.1:5000