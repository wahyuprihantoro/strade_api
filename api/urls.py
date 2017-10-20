from django.conf.urls import url

from api.views import user_views, product_views

urlpatterns = [
    url(r'login/?', user_views.LoginView.as_view()),
    url(r'register/?', user_views.RegisterView.as_view()),
    # url(r'^products/$', product_views.CreateProductView.as_view()),
    url(r'^products/?', product_views.ProductView.as_view()),
]
