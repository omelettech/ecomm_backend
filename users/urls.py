from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

# https://dj-rest-auth.readthedocs.io/en/latest/api_endpoints.html
from users.views import GoogleLogin, CustomerView, WishlistListCreateView, WishlistRUDView

urlpatterns = [
    path("v1/dj-rest-auth/", include("dj_rest_auth.urls")),
    path('v1/dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    path('v1/dj-rest-auth/google/', GoogleLogin.as_view(), name='google_login'),

    path('v1/customer/', CustomerView.as_view(), name='customer'),
    path('v1/wishlist/', WishlistListCreateView.as_view(), name='wishlist'),
    path('v1/wishlist/<int:pk>/', WishlistRUDView.as_view(), name='wishlist_rud'),

]
