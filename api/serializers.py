from rest_framework import serializers

from api.models import User, Product, Request, UserLocation, Store, RequestItem


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'full_name', 'email', 'role', 'phone_number', 'image_url']


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['id', 'status', 'name', 'category', 'open_time', 'close_time', 'image_url']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'image_url')


class RequestItemSerializer(object):
    item = ProductSerializer()

    class Meta:
        model = RequestItem
        fields = ('id', 'item', 'count')


class RequestSerializer(serializers.ModelSerializer):
    seller = UserSerializer()
    buyer = UserSerializer()
    items = serializers.RelatedField(many=True, read_only=True)

    class Meta:
        model = Request
        fields = ('id', 'seller', 'status', 'total_price', 'latitude', 'longitude', 'note', 'address', 'buyer', 'items')


class UserLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLocation
        fields = ('id', 'latitude', 'longitude', 'current_address')
