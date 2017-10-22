import uuid
from base64 import b64decode

from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.core.files.base import ContentFile
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from api.controllers import helpers
from api.models import User, Store, Image
from django.contrib.auth.models import Group

from api.serializers import UserSerializer


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
            phone_number = request.data.get('phone_number')
            user_role = Group.objects.filter(name=role).first()
            if User.objects.filter(username=username).first() is not None:
                response = Response(helpers.fail_context(message="username sudah digunakan"),
                                    status=status.HTTP_200_OK)
            elif user_role is None:
                response = Response(helpers.fail_context(message="role tidak valid"),
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
            else:
                user = User.objects.create(
                    first_name=name,
                    username=username,
                    password=make_password(password),
                    role=user_role,
                    phone_number=phone_number
                )
                if user.role.name == 'seller':
                    store = Store.objects.create(name=username)
                    user.store = store
                    user.save()
                content = helpers.construct_login_return_content(user)
                response = Response(content, status=status.HTTP_200_OK)
        except Exception as e:
            print(str(e))
            response = Response(helpers.fatal_context(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return response


class UpdatePhotoProfileView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]

    def post(self, request):
        user = request.user
        image_base64 = request.data.get('image')
        try:
            if image_base64 is None:
                response = Response(helpers.fail_context(message="Gambar tidak valid"),
                                    status=status.HTTP_200_OK)
            else:
                image_data = b64decode(image_base64)
                image_name = "user-" + str(uuid.uuid4()) + ".jpg"
                file = ContentFile(image_data, image_name)
                image = Image.objects.create(filename=image_name, file=file)
                user.image = image
                user.save()
                data = UserSerializer(user).data
                response = Response(helpers.success_context(user=data), status=status.HTTP_200_OK)
        except Exception as e:
            print(str(e))
            response = Response(helpers.fatal_context(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return response
