from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api import serializers
from api.controllers import helpers


class LoginView(APIView):
    def post(self, request):
        try:
            user = authenticate(username=request.data.get('username'), password=request.data.get('password'))
            if user is None:
                response = Response(helpers.fail_context(message="username atau password tidak valid"),
                                    status=status.HTTP_401_UNAUTHORIZED)
            else:
                response = Response(helpers.success_context(user=serializers.UserSerializer(user)),
                                    status=status.HTTP_200_OK)
        except Exception as e:
            print(str(e))
            response = Response(helpers.fatal_context(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return response

