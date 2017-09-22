from django.conf.urls import url

from api.views import user_views

urlpatterns = [
    url(r'login/', user_views.LoginView.as_view())
]
