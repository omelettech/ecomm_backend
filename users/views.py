from urllib.parse import urljoin

from allauth.socialaccount.providers.oauth2.client import OAuth2Client

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from ecomm_backend import settings
from users.models import Customer, Wishlist, WishlistItem
from users.serializers import CustomerSerializer, WishlistSerializer, WishlistItemSerializer


class GoogleLogin(SocialLoginView):  # if you want to use Authorization Code Grant, use this
    adapter_class = GoogleOAuth2Adapter
    callback_url = settings.GOOGLE_OAUTH_CALLBACK_URL
    client_class = OAuth2Client

class GoogleLoginCallback(APIView):  # if you want to use Implicit Grant, use this
    def get(self, request):
        code=request.GET.get('code')

        if not code or code is None:
            return JsonResponse(status=400, data={'message': 'Invalid code.'})
        tokenendpoint = urljoin(settings.GOOGLE_OAUTH_TOKEN_URL, 'token')

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


class WishlistView(generics.RetrieveAPIView):
    serializer_class = WishlistSerializer

    def get_object(self):
        return Wishlist.objects.get(customer=self.request.user.customer)

    def get_queryset(self):
        return Wishlist.objects.filter(customer=self.request.user.customer)


class WishlistItemView(generics.ListCreateAPIView, generics.RetrieveDestroyAPIView):
    queryset = WishlistItem.objects.all()
    serializer_class = WishlistItemSerializer
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access

    def get_queryset(self):
        return WishlistItem.objects.filter(wishlist=self.request.user.customer.wishlist)

    def get_object(self):
        return WishlistItem.objects.get(pk=self.kwargs['pk'])

    def perform_create(self, serializer):
        """
        This method overrides the default `perform_create` to save the user-specific wishlist item data.
        """
        serializer.save(wishlist=self.request.user.customer.wishlist)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.soft_delete()
        return JsonResponse(status=200, data={'message': 'Wishlist Item deleted successfully.'})

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if pk:
            # get a specific wishlist item
            if WishlistItem.objects.get(pk=pk).wishlist.customer.user == request.user:
                return self.retrieve(request, *args, **kwargs)
            return JsonResponse(status=403, data={'message': 'You are not authorized to view this wishlist item.'})
        else:
            # get all wishlist items for the user
            return self.list(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        request.data['wishlist'] = request.user.customer.wishlist.id
        return self.create(request, *args, **kwargs)

