from rest_framework import viewsets,status
from .models import Warehouse, Product
from .serializers import WarehouseSerializer, ProductSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated


class WarehouseViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    @action(detail=True, methods=["get"])
    def audit(self, request, pk=None, permission_classes=[IsAuthenticated]):
        warehouse = self.get_object()

        total_products = warehouse.products.count()

        return Response({
            "warehouse": warehouse.name,
            "location": warehouse.location,
            "total_products": total_products
        })

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    @action(detail=True, methods=["post"],permission_classes=[IsAuthenticated])
    def move(self, request, pk=None):
        # Récupérer le produit
        product = self.get_object()

        print(f"Produit récupéré: {product.name}, Statut: {product.status}")

        # Vérifier si le produit est périmé
        if product.status == Product.Status.EXPIRED:
            return Response(
                {"error": "Ce produit est périmé. Transfert impossible."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Récupérer l'id du nouvel entrepôt
        warehouse_id = request.data.get("warehouse")

        if not warehouse_id:
            return Response(
                {"error": "Le champ 'warehouse' est obligatoire."},
                status=status.HTTP_400_BAD_REQUEST
            )
        print(f"ID de l'entrepôt cible: {warehouse_id}")
        # Vérifier que l'entrepôt existe
        warehouse = get_object_or_404(Warehouse, pk=warehouse_id)

        # Effectuer le transfert
        product.warehouse = warehouse
        product.save()

        return Response(
            {
                "message": "Produit transféré avec succès.",
                "product": product.name,
                "new_warehouse": warehouse.name,
            },
            status=status.HTTP_200_OK
        )

