from datetime import datetime

from geopy import Nominatim, ArcGIS
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from api.controllers import helpers
from api.models import UserLocation
from api.serializers import UserLocationSerializer


class LocationView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]

    def post(self, request):
        try:
            user = request.user
            latitude = request.data.get('latitude')
            longitude = request.data.get('longitude')
            if latitude is None or longitude is None or latitude == 0 or longitude == 0:
                response = Response(helpers.fail_context(message="koordinat lokasi tidak valid"),
                                    status=status.HTTP_200_OK)
            else:
                geolocator = ArcGIS()
                location = geolocator.reverse(str(latitude) + ", " + str(longitude))
                user_location = UserLocation.objects.filter(user=user).first()
                if user_location is None:
                    user_location = UserLocation.objects.create(user=user)
                user_location.latitude = latitude
                user_location.longitude = longitude
                user_location.current_address = location.address
                user_location.updated_at = datetime.utcnow()
                user_location.save()
                data = UserLocationSerializer(user_location).data
                response = Response(helpers.success_context(location=data),
                                    status=status.HTTP_200_OK)
        except Exception as e:
            print(str(e))
            response = Response(helpers.fatal_context(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return response
