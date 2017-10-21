from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from api.controllers import helpers
from api.models import Product, User, RequestItem, Request, UserLocation
from api.permissions import IsBuyer
from api.serializers import RequestSerializer
from geopy.distance import vincenty


class RequestView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]

    @permission_classes(IsBuyer, )
    def post(self, request):
        try:
            seller_id = request.data.get('seller_id')
            product_ids = request.data.get('product_ids')
            latitude = request.data.get('latitude')
            longitude = request.data.get('longitude')
            seller = User.objects.filter(id=seller_id).first()
            user = request.user
            if seller is None:
                response = Response(helpers.fail_context(message="penjual yang anda pilih tidak valid"),
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
                r = Request.objects.create(seller=seller, buyer=user, status_id=1, total_price=total_price,
                                           latitude=latitude, longitude=longitude)
                for p in products:
                    RequestItem.objects.create(request=r, item=p)
                request_data = RequestSerializer(r).data
                response = Response(helpers.success_context(request=request_data), status=status.HTTP_200_OK)
        except Exception as e:
            print(str(e))
            response = Response(helpers.fatal_context(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return response

    def get(self, request):
        try:
            user = request.user
            location = UserLocation.objects.get(user=user)
            if user.role.name == 'seller':
                requests = Request.objects.filter(seller=user).all()
                request_data = []
                for r in requests:
                    buyer_location = (location.latitude, location.longitude)
                    seller_location = (r.latitude, r.longitude)
                    distance = vincenty(buyer_location, seller_location).km
                    data = RequestSerializer(r).data
                    data['distance'] = distance
                    request_data += [data]
                response = Response(helpers.success_context(requests=request_data),
                                    status=status.HTTP_200_OK)
            elif user.role.name == 'buyer':
                requests = Request.objects.filter(buyer=user).all()
                request_data = []
                for r in requests:
                    location = UserLocation.objects.get(user=r.seller)
                    buyer_location = (location.latitude, location.longitude)
                    seller_location = (r.latitude, r.longitude)
                    distance = vincenty(buyer_location, seller_location).km
                    data = RequestSerializer(r).data
                    data['distance'] = distance
                    request_data += [data]
                response = Response(helpers.success_context(requests=request_data),
                                    status=status.HTTP_200_OK)
            else:
                response = Response(helpers.fail_context(message="Permission denied"),
                                    status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            print(str(e))
            response = Response(helpers.fatal_context(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return response
