from urllib.parse import urljoin

import requests
from allauth.socialaccount.providers.oauth2.client import OAuth2Client

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from ecomm_backend import settings
from products.models import ProductSku
from users.models import Customer, Wishlist, WishlistItem
from users.serializers import CustomerSerializer, WishlistSerializer, WishlistItemSerializer
from .models import User
#
# class GoogleLogin(SocialLoginView):
#     adapter_class = GoogleOAuth2Adapter
#     callback_url = settings.GOOGLE_OAUTH_CALLBACK_URL
#     client_class = OAuth2Client


class GoogleSSOLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.data.get("token") or request.headers.get("Authorization").split(" ")[1]

        if not token:
            return JsonResponse({"error": "Token is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Verify Google ID Token
        google_verify_url = f"https://oauth2.googleapis.com/tokeninfo?id_token={token}"
        response = requests.get(google_verify_url)
        if response.status_code != 200:
            return JsonResponse({"error": "Invalid ID Token"}, status=status.HTTP_400_BAD_REQUEST)

        user_info = response.json()
        email = user_info.get("email")
        username = user_info.get("email").split("@")[0]
        first_name = user_info.get("given_name", "")
        last_name = user_info.get("family_name", "")
        profile_picture = user_info.get("picture", "")

        # Create or retrieve user
        user, _ = User.objects.get_or_create(email=email,
                                             username=username,
                                             defaults={"first_name": first_name, "last_name": last_name})
        user.profile_picture = profile_picture
        user.save()

        # Generate auth token
        token, _ = Token.objects.get_or_create(user=user)
        return JsonResponse({"token": token.key, "user": {"email": user.email, "profile_picture": user.profile_picture}})


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


class WishlistItemView(generics.ListCreateAPIView):
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
        request.data['product_sku'] = ProductSku.objects.get(sku=request.data['product_sku']).id
        return self.create(request, *args, **kwargs)


class WishlistDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        product_sku = self.kwargs['product_sku']
        try:
            wishlist_item = WishlistItem.objects.get(wishlist=request.user.customer.wishlist.id,
                                                     product_sku=ProductSku.objects.get(sku=product_sku).id,
                                                     deleted_at__isnull=True)
            if wishlist_item:
                wishlist_item.soft_delete()
                return JsonResponse(status=status.HTTP_202_ACCEPTED,
                                    data={'message': f"{product_sku} deleted from wishlist"})

        except ProductSku.DoesNotExist:
            return JsonResponse(status=status.HTTP_400_BAD_REQUEST,
                                data={'message': f"{product_sku} sku code doesnt exist"})
        except WishlistItem.DoesNotExist:
            return JsonResponse(status=status.HTTP_400_BAD_REQUEST,
                                data={'message': f"{product_sku} Is deleted or doesnt exist"})
