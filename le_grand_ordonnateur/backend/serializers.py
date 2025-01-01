from rest_framework import serializers
from .models.product.product import Product
from .models.product.product_version import ProductVersion
from .models.product.product_material import ProductMaterial

from .models.material.material import Material
from .models.material.material_supplier import MaterialSupply

from .models.supplier.supplier import Supplier

# Serializer for the Product model
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

# Serializer for the ProductVersion model
class ProductVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVersion
        fields = '__all__'

# Serializer for the ProductMaterial model
class ProductMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductMaterial
        fields = '__all__'

# Serializer for the Material model
class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'

# Serializer for the MaterialSupply model
class MaterialSupplySerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialSupply
        fields = '__all__'

# Serializer for the Supplier model
class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'
