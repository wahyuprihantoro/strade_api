from rest_framework import serializers

from api.models import User, Product, Order, UserLocation, Store, OrderItem, StoreCategory


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['id', 'status', 'name', 'category', 'open_time', 'close_time', 'image_url']


class UserSerializer(serializers.ModelSerializer):
    store = StoreSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'full_name', 'role', 'phone_number', 'image_url', 'store']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'image_url')


class OrderItemSerializer(serializers.ModelSerializer):
    item = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = ('id', 'item', 'count')


class OrderSerializer(serializers.ModelSerializer):
    seller = UserSerializer()
    buyer = UserSerializer()
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'seller', 'status', 'total_price', 'latitude', 'longitude', 'note', 'address', 'buyer', 'items')


class UserLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLocation
        fields = ('id', 'latitude', 'longitude', 'current_address')


class StoreCategorySerializer(serializers.ModelSerializer):
    class Meta:
        module = StoreCategory
        fields = ('id', 'name', 'image_url')
