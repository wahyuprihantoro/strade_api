from rest_framework import serializers

from api.models import User, Product, Request, UserLocation


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'full_name', 'email', 'role', 'phone_number', 'store_name', 'store_category']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'image_url')


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ('id', 'seller', 'status', 'total_price', 'latitude', 'longitude')


class UserLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLocation
        fields = ('id', 'latitude', 'longitude', 'current_address')
