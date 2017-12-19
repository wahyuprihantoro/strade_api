from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from api.controllers import helpers
from api.models import Product, User, OrderItem, Order, UserLocation, OrderStatus
from api.permissions import IsBuyer
from api.serializers import OrderSerializer
from geopy.distance import vincenty


class OrderView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]

    @permission_classes(IsBuyer, )
    def post(self, request):
        try:
            seller_id = request.data.get('seller_id')
            product_ids = request.data.get('product_ids')
            latitude = request.data.get('latitude')
            longitude = request.data.get('longitude')
            note = request.data.get('note')
            address = request.data.get('address')
            seller = User.objects.filter(id=seller_id).first()
            user = request.user
            if seller is None or seller.role.name != 'seller':
                response = Response(helpers.fail_context(message="penjual yang anda pilih tidak valid"),
                                    status=status.HTTP_200_OK)
            elif address is None:
                response = Response(helpers.fail_context(message="alamat tidak valid"),
                                    status=status.HTTP_200_OK)
            elif user.role.name != 'buyer':
                response = Response(helpers.fail_context(message="Permission denied"),
                                    status=status.HTTP_403_FORBIDDEN)
            elif product_ids is None or len(product_ids) == 0:
                response = Response(helpers.fail_context(message="daftar produk tidak valid"),
                                    status=status.HTTP_200_OK)
            else:
                products = Product.objects.filter(pk__in=product_ids).all()
                total_price = 0
                for p in products:
                    total_price += p.price
                order = Order.objects.create(seller=seller, buyer=user, status_id=1, total_price=total_price,
                                             latitude=latitude, longitude=longitude, note=note, address=address)
                for p in products:
                    count = product_ids.count(p.id)
                    OrderItem.objects.create(order=order, item=p, count=count)
                request_data = OrderSerializer(order).data
                response = Response(helpers.success_context(order=request_data), status=status.HTTP_200_OK)
        except Exception as e:
            print(str(e))
            response = Response(helpers.fatal_context(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return response

    def get(self, request):
        try:
            user = request.user
            if user.role.name == 'seller':
                location = UserLocation.objects.get(user=user)
                orders = Order.objects.filter(seller=user).all()
                order_data = []
                for o in orders:
                    buyer_location = (location.latitude, location.longitude)
                    seller_location = (o.latitude, o.longitude)
                    distance = vincenty(buyer_location, seller_location).km
                    data = OrderSerializer(o).data
                    data['distance'] = distance
                    order_data += [data]
                response = Response(helpers.success_context(orders=order_data),
                                    status=status.HTTP_200_OK)
            elif user.role.name == 'buyer':
                orders = Order.objects.filter(buyer=user).all()
                order_data = []
                for o in orders:
                    print(o.seller)
                    location = UserLocation.objects.get(user=o.seller)
                    buyer_location = (location.latitude, location.longitude)
                    seller_location = (o.latitude, o.longitude)
                    distance = vincenty(buyer_location, seller_location).km
                    data = OrderSerializer(o).data
                    data['distance'] = distance
                    order_data += [data]
                response = Response(helpers.success_context(orders=order_data),
                                    status=status.HTTP_200_OK)
            else:
                response = Response(helpers.fail_context(message="Permission denied"),
                                    status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            print(str(e))
            response = Response(helpers.fatal_context(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return response


class UpdateOrderStatusView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]

    def post(self, request, req_id):
        try:
            r = Order.objects.filter(id=req_id).first()
            status_name = request.data.get('status')
            order_status = OrderStatus.objects.filter(name=status_name).first()
            if r is None:
                response = Response(helpers.fail_context(message="order tidak ditemukan"),
                                    status=status.HTTP_200_OK)
            elif order_status is None:
                response = Response(helpers.fail_context(message="order status salah"),
                                    status=status.HTTP_200_OK)
            else:
                r.status = order_status
                r.save()
                order_data = OrderSerializer(r).data
                response = Response(helpers.success_context(order=order_data), status=status.HTTP_200_OK)
        except Exception as e:
            print(str(e))
            response = Response(helpers.fatal_context(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return response
