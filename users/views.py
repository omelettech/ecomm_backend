from allauth.socialaccount.providers.oauth2.client import OAuth2Client

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from users.models import Customer, Wishlist
from users.serializers import CustomerSerializer, WishlistSerializer


class GoogleLogin(SocialLoginView):  # if you want to use Authorization Code Grant, use this
    adapter_class = GoogleOAuth2Adapter
    # callback_url = CALLBACK_URL_YOU_SET_ON_GOOGLE
    client_class = OAuth2Client

class CustomerView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access

    def get_object(self):
        return Customer.objects.get(user=self.request.user)

    def get_queryset(self):
        return Customer.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        """
        This method overrides the default `perform_update` to save the user-specific customer data.
        """
        # Ensure we don't overwrite the user field, it is already linked to the user.
        serializer.save(user=self.request.user)


    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.soft_delete()
        return JsonResponse(status=200, data={'message': 'Customer deleted successfully.'})


class WishlistListCreateView(generics.ListCreateAPIView):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user.customer)


class WishlistRUDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.soft_delete()
        return JsonResponse(status=200, data={'message': 'Wishlist deleted successfully.'})
