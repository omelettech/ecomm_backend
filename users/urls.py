from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

# https://dj-rest-auth.readthedocs.io/en/latest/api_endpoints.html
from users.views import GoogleLogin

urlpatterns = [
    path("v1/dj-rest-auth/", include("dj_rest_auth.urls")),
    path('v1/dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    path('v1/dj-rest-auth/google/', GoogleLogin.as_view(), name='google_login')

]
