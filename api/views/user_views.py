from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.controllers import helpers


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
