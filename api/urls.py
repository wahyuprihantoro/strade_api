from django.conf.urls import url

from api.views import user_views, product_views, request_views, location_views, store_views

urlpatterns = [
    url(r'^login', user_views.LoginView.as_view()),
    url(r'^register', user_views.RegisterView.as_view()),
    url(r'^products/?', product_views.ProductView.as_view()),
    url(r'^orders/(?P<req_id>[0-9]+)', request_views.UpdateOrderStatusView.as_view()),
    url(r'^orders/?', request_views.OrderView.as_view()),
    url(r'^user/location', location_views.LocationView.as_view()),
    url(r'^stores/(?P<category_id>[0-9]+)', store_views.GetStoresView.as_view()),
    url(r'^stores', store_views.StoreView.as_view()),
    url(r'^user/profile-picture', user_views.UpdatePhotoProfileView.as_view()),
]
