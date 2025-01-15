from rest_framework import serializers

from .models.Kanban.Column import Column
from .models.Kanban.Task import Task
from .models.product.product import Product
from .models.product.product_version import ProductVersion
from .models.product.product_material import ProductMaterial
from .models.product.product_stock import ProductStock

from .models.material.material import Material

from .models.supplier.supplier import Supplier
from .models.manufacturing.manufacturing import Manufacturing
from .models.manufacturing.step import Step

# Serializer for the ProductStock model
class ProductStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductStock
        fields = '__all__'

# Serializer for the ProductVersion model
class ProductVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVersion
        fields = '__all__'

# Serializer for the Product model
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class BomLineSerializer(serializers.Serializer):
    material = serializers.PrimaryKeyRelatedField(
        queryset=Material.objects.all(),
        required=True
    )
    supplier = serializers.PrimaryKeyRelatedField(
        queryset=Supplier.objects.all(),
        required=True
    )
    unit_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=True,
        min_value=0.01
    )
    quantity = serializers.FloatField(
        required=True,
        min_value=0
    )
    def validate(self, data):
        return data

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


# Serializer for the Supplier model
class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'column', 'position']

class ColumnSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Column
        fields = '__all__'

class StepSerializer(serializers.ModelSerializer):
    class Meta:
        model = Step
        fields = '__all__'


class ManufacturingSerializer(serializers.ModelSerializer):
    steps = StepSerializer(many=True, read_only=True)  # This will include all related steps

    class Meta:
        model = Manufacturing
        fields = ['id', 'name', 'product', 'version', 'steps']
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Manufacturing.objects.all(),
                fields=['product', 'version'],
                message="A manufacturing process for this product version already exists."
            )
        ]
