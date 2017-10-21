from django.conf.urls import url

from api.views import user_views, product_views, request_views, location_views

urlpatterns = [
    url(r'^login', user_views.LoginView.as_view()),
    url(r'^register', user_views.RegisterView.as_view()),
    url(r'^products/?', product_views.ProductView.as_view()),
    url(r'^requests/?', request_views.RequestView.as_view()),
    url(r'^user/location', location_views.LocationView.as_view()),
]
