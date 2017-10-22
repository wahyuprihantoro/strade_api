from rest_framework_jwt.settings import api_settings

from api.serializers import UserSerializer, StoreSerializer


def success_context(**kwargs):
    context = {
        'status': True,
        'message': "OK",
        **kwargs
    }
    return context


def fail_context(message=None, **kwargs):
    context = {
        'status': False,
        'message': message,
        **kwargs
    }
    return context


def fatal_context():
    context = {
        'status': False,
        'message': 'terjadi kesalahan pada server'
    }
    return context


def generate_token(user):
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    payload = jwt_payload_handler(user)
    return jwt_encode_handler(payload)


def get_user_data(header):
    jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
    return jwt_decode_handler(header.get('HTTP_AUTHORIZATION').split(' ')[1])


def construct_login_return_content(user):
    token = generate_token(user)
    user_data = UserSerializer(user).data
    return success_context(user=user_data, token=token)
