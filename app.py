from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from models import db, Product  # Importer depuis models.py
import click
from cli import init_db  # Importer la commande init_db depuis cli.py

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)  # Initialiser db avec l'application

# Initialiser la base de données dans le contexte de l'application
with app.app_context():
    db.create_all()

# Enregistrer la commande CLI init-db
@app.cli.command("init-db")
def init_db_command():
    """Initialise la base de données avec des produits de test."""
    init_db()  # Appel de la fonction init_db de cli.py
    print("Base de données initialisée avec des produits.")

@app.cli.command("reset-db")
def init_db_command():
    db.drop_all() # Appel de la fonction init_db de cli.py
    print("Base de données supprimée.")


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/products")
def products():
    products = Product.query.all()
    return render_template("products.html", products=products)

if __name__ == "__main__":
    app.run(debug=True)
