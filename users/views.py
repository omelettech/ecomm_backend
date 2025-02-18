from urllib.parse import urljoin

from allauth.socialaccount.providers.oauth2.client import OAuth2Client

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from ecomm_backend import settings
from products.models import ProductSku
from users.models import Customer, Wishlist, WishlistItem
from users.serializers import CustomerSerializer, WishlistSerializer, WishlistItemSerializer


class GoogleLogin(SocialLoginView):  # if you want to use Authorization Code Grant, use this
    adapter_class = GoogleOAuth2Adapter
    callback_url = settings.GOOGLE_OAUTH_CALLBACK_URL
    client_class = OAuth2Client


class GoogleLoginCallback(APIView):  # if you want to use Implicit Grant, use this
    def get(self, request):
        code = request.GET.get('code')

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
