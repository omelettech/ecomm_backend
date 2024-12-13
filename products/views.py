from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.views import View

from products.models import Product
from products.serializers import ProductSerializer


class ProudctView(View):
    # CRUD operation for PRODUCTS only
    def post(self, request):
        pass

    def get(self, request):
        # If request is GET automatically comes here.
        # configure this method to check if request has an id passed to it. if yes, then give the details of one product
        products = Product.objects.all()
        serializer= ProductSerializer(products,many=True)
        return JsonResponse(serializer.data)

    def put(self, request):
        pass

    def delete(self, request):
        pass


class ProductSkuView(View):

    def post(self, request):
        pass

    def get(self, request):
        pass

    def put(self, request):
        pass

    def delete(self, request):
        pass

# Create your views here.
