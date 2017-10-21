import uuid
from base64 import b64decode
from datetime import time

from django.core.files.base import ContentFile
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from api.controllers import helpers
from api.models import StoreCategory, Store, StoreStatus, Image
from api.serializers import StoreSerializer


class StoreView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]

    def post(self, request):
        try:
            user = request.user
            store_name = request.data.get('name')
            store_category = request.data.get('category')
            open_time = request.data.get('open_time')
            close_time = request.data.get('close_time')
            image_base64 = request.data.get('image')
            user_store_category = StoreCategory.objects.filter(id=store_category).first()
            if user.role.name != 'seller':
                response = Response(helpers.fail_context(message="Permission denied"),
                                    status=status.HTTP_403_FORBIDDEN)
            elif store_name is None or len(store_name) < 4:
                response = Response(helpers.fail_context(message="Nama toko tidak valid"),
                                    status=status.HTTP_200_OK)
            elif user_store_category is None:
                response = Response(helpers.fail_context(message="Kategori toko tidak valid"),
                                    status=status.HTTP_200_OK)
            elif open_time is None or close_time is None:
                response = Response(helpers.fail_context(message="Jam operasional toko tidak valid"),
                                    status=status.HTTP_200_OK)
            elif image_base64 is None:
                response = Response(helpers.fail_context(message="Gambar toko tidak valid"),
                                    status=status.HTTP_200_OK)
            else:

                image_data = b64decode(image_base64)
                image_name = "store-" + str(uuid.uuid4()) + ".jpg"
                file = ContentFile(image_data, image_name)
                image = Image.objects.create(filename=image_name, file=file)

                store_status = StoreStatus.objects.filter(name="open").first()
                if store_status is None:
                    store_status = StoreStatus.objects.create(name="open")
                store = Store.objects.create(name=store_name, status=store_status, open_time=open_time,
                                             close_time=close_time,
                                             category=user_store_category, image=image)

                data = StoreSerializer(store).data
                response = Response(helpers.success_context(store=data),
                                    status=status.HTTP_200_OK)
        except Exception as e:
            print(str(e))
            response = Response(helpers.fatal_context(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return response