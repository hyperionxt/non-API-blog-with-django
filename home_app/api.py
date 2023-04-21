from .models import *
from rest_framework import viewsets, permissions
from .serializers import CategorySerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset=Category.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = CategorySerializer