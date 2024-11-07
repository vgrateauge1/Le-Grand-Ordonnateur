# cli.py
from models import db, Product

def init_db():
    """Initialise la base de données avec des produits de test."""
    db.create_all()
    product1 = Product(name="Produit 1", description="Description du produit 1", price=10.99)
    product2 = Product(name="Produit 2", description="Description du produit 2", price=12.49)
    db.session.add_all([product1, product2])
    db.session.commit()
