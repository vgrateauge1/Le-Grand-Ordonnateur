# **Le Grand Ordonnateur**

## **Installation**

### **Cloner le projet**
Clonez ce dépôt sur votre machine locale :
```bash
git clone https://github.com/vgrateauge1/Le-Grand-Ordonnateur.git
cd Le-Grand-Ordonnateur
```

### **Appliquer les migrations**
```
python manage.py migrate
```

### **Créer un environnement conda (optionnel)**
```
conda create plm_env
```

### **Installer les dépendances nécessaire**
```
pip install -r requirements.txt
```

### **Créer un superutilisateur (optionnel)**
```
python manage.py createsuperuser
```
Accédez à l’application dans votre navigateur en tant que superuser à l’adresse http://127.0.0.1:8000/admin

### **Lancer le serveur**
```
python manage.py runserver
```
Accédez à l’application dans votre navigateur à l’adresse http://127.0.0.1:8000/

### **Structure du projet**

manage.py : Point d’entrée du projet.

nom_de_ton_app/ : Contient les fichiers de l’application.

models.py : Modèles pour la base de données.

views.py : Logique métier.

templates/ : Fichiers HTML.

static/ : Fichiers CSS et JS.

requirements.txt : Dépendances du projet.
