from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path

# https://dj-rest-auth.readthedocs.io/en/latest/api_endpoints.html
from users.views import GoogleLogin, CustomerView, WishlistView, WishlistItemView, WishlistDeleteView

urlpatterns = [
    path("v1/dj-rest-auth/", include("dj_rest_auth.urls")),
    path('v1/dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    path('v1/dj-rest-auth/google/', GoogleLogin.as_view(), name='google_login'),

    path('v1/customer/', CustomerView.as_view(), name='customer'),

    path('v1/wishlist/', WishlistView.as_view(), name='wishlist_rud'),
    path('v1/wishlistitem/', WishlistItemView.as_view(), name='wishlist_item'),
    path('v1/wishlistitem/<str:product_sku>',WishlistDeleteView.as_view(),name="delete_wishlist_item")
]
