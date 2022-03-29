from rest_framework import serializers
from core.models import Category, MenuItem, Order, OrderedItem, Payment, Tag


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class AuthTokenPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class MenuItemSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField(read_only=True)
    tags_list = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = MenuItem
        exclude = ("is_active", "created_at", "updated_at")

    def get_category_name(self, obj):
        return obj.category.name

    def get_tags_list(self, obj):
        tags = obj.tags.filter(is_active=True).values_list("name", flat=True)
        return tags


class OrderedItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderedItem
        fields = "__all__"

    def get_menu_item_detail(self, obj):
        return obj.menu_item


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
