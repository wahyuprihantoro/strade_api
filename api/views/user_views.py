from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.controllers import helpers
from api.models import User, StoreCategory, Store, StoreStatus
from django.contrib.auth.models import Group


class LoginView(APIView):
    def post(self, request):
        try:
            user = authenticate(username=request.data.get('username'), password=request.data.get('password'))
            if user is None:
                response = Response(helpers.fail_context(message="username atau password tidak valid"),
                                    status=status.HTTP_401_UNAUTHORIZED)
            elif user.role.name != request.data.get('role'):
                response = Response(helpers.fail_context(message="role tidak valid"),
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                content = helpers.construct_login_return_content(user)
                response = Response(content, status=status.HTTP_200_OK)
        except Exception as e:
            print(str(e))
            response = Response(helpers.fatal_context(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return response


class RegisterView(APIView):
    def post(self, request):
        try:
            name = request.data.get('name')
            username = request.data.get('username')
            password = request.data.get('password')
            role = request.data.get('role')
            store_name = request.data.get('store_name')
            store_category = request.data.get('store_category')
            open_time = request.data.get('open_time')
            close_time = request.data.get('close_time')
            phone_number = request.data.get('phone_number')
            user_role = Group.objects.filter(name=role).first()
            user_store_category = StoreCategory.objects.filter(id=store_category).first()
            if User.objects.filter(username=username).first() is not None:
                response = Response(helpers.fail_context(message="username sudah digunakan"),
                                    status=status.HTTP_200_OK)
            elif user_role is None:
                response = Response(helpers.fail_context(message="role tidak valid"),
                                    status=status.HTTP_200_OK)
            elif user_role == 'seller' and user_store_category is None:
                response = Response(helpers.fail_context(message="kategori yang anda pilih tidak valid"),
                                    status=status.HTTP_200_OK)
            elif password is None or len(password) < 5:
                response = Response(helpers.fail_context(message="password tidak valid"),
                                    status=status.HTTP_200_OK)
            elif username is None or len(username) < 5:
                response = Response(helpers.fail_context(message="username tidak valid"),
                                    status=status.HTTP_200_OK)
            elif phone_number is None or len(phone_number) < 10:
                response = Response(helpers.fail_context(message="nomor hp tidak valid"),
                                    status=status.HTTP_200_OK)
            elif store_name is None or len(store_name) < 4:
                response = Response(helpers.fail_context(message="nama toko tidak valid"),
                                    status=status.HTTP_200_OK)
            else:
                user = User.objects.create(
                    first_name=name,
                    username=username,
                    password=make_password(password),
                    role=user_role,
                    phone_number=phone_number
                )
                if role == 'seller':
                    store_status = StoreStatus.objects.filter(name="open").first()
                    if store_status is None:
                        store_status = StoreStatus.objects.create(name="open")
                    store = Store.objects.create(name=store_name, status=store_status,
                                                 category=user_store_category)
                    user.store = store
                    user.save()
                content = helpers.construct_login_return_content(user)
                response = Response(content, status=status.HTTP_200_OK)
        except Exception as e:
            print(str(e))
            response = Response(helpers.fatal_context(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return response
