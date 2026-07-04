from rest_framework import serializers
from .models import Product, Warehouse

class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ['id', 'name', 'location', 'capacity']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'warehouse', 'name', 'quantity', 'expiration_date', 'status']