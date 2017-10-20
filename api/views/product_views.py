import uuid

from django.core.files.base import ContentFile
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from api.controllers import helpers
from api.models import Product, Image
from api.permissions import IsSeller
from api.serializers import ProductSerializer

from base64 import b64decode


class CreateProductView(APIView):
    permission_classes = [IsSeller]
    authentication_classes = [JSONWebTokenAuthentication]

    def post(self, request):
        try:
            user = request.user
            name = request.data.get('name')
            price = request.data.get('price')
            image_base64 = request.data.get('image')
            if user is None:
                response = Response(helpers.fail_context(message="silahkan login terlebih dahulu"),
                                    status=status.HTTP_401_UNAUTHORIZED)
            elif name is None or len(name) < 4:
                response = Response(helpers.fail_context(message="nama produk anda tidak valid"),
                                    status=status.HTTP_200_OK)
            elif price is None or int(price) < 0:
                response = Response(helpers.fail_context(message="harga produk anda tidak valid"),
                                    status=status.HTTP_200_OK)
            else:
                image_data = b64decode(image_base64)
                image_name = str(uuid.uuid4()) + ".jpg"
                file = ContentFile(image_data, image_name)
                image = Image.objects.create(filename=image_name, file=file)
                product = Product.objects.create(store=user, name=name, price=price, image=image)
                product_data = ProductSerializer(product).data
                response = Response(helpers.success_context(product=product_data), status=status.HTTP_200_OK)
        except Exception as e:
            print(str(e))
            response = Response(helpers.fatal_context(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return response
