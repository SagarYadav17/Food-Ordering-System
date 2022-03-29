# Models & Serializers
from core.models import MenuItem, Tag, Category, Order, OrderedItem, Payment
from core.serializers import MenuItemSerializer, AuthTokenPairSerializer, OrderSerializer, OrderedItemSerializer, PaymentSerializer, TagSerializer, CategorySerializer

# Django & Other 3rd Party Libraries
from django.contrib.auth import logout
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django_filters.rest_framework import DjangoFilterBackend


class AuthTokenPairView(TokenObtainPairView):
    serializer_class = AuthTokenPairSerializer


class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        logout(request)
        return Response()


class TagsViewset(ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_fields = {
        "name": ["startswith", "exact"],
    }
    http_method_names = ["get", "post", "patch", "delete"]


class CategoryViewset(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_fields = {
        "name": ["startswith", "exact"],
    }
    http_method_names = ["get", "post", "patch", "delete"]


class MenuItemViewset(ModelViewSet):
    serializer_class = MenuItemSerializer
    queryset = MenuItem.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_fields = {
        "name": ["startswith", "exact"],
        "category": ["exact"],
        "tags": ["exact"],
    }
    http_method_names = ["get", "post", "patch", "delete"]


class OrderViewset(ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_fields = {
        "table_number": ["exact"],
        "status": ["exact"],
    }
    http_method_names = ["get", "post", "patch", "delete"]


class OrderedItemViewset(ModelViewSet):
    serializer_class = OrderedItemSerializer
    queryset = OrderedItem.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_fields = {
        "order": ["exact"],
    }
    http_method_names = ["get", "post", "patch", "delete"]


class PaymentViewset(ModelViewSet):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_fields = {
        "order": ["exact"],
    }
    http_method_names = ["get", "post", "patch", "delete"]
