from json import JSONDecodeError

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.views import View
from rest_framework.utils import json
from rest_framework.views import APIView
from django.apps import apps
from products.models import Product, ProductSkus
from products.serializers import ProductSerializer, ProductSkuSerializer, SizeAttributeSerializer, \
    ColorAttributeSerializer
from rest_framework import generics

ATTRIBUTE_SERIALIZERS = {  # Add new attribute tables here
    'size': SizeAttributeSerializer,
    "color": ColorAttributeSerializer,
}


def validateAttribute(attr_name: str):
    return attr_name in ATTRIBUTE_SERIALIZERS.keys()


def getSerializer(attr_name: str):
    if validateAttribute(attr_name):
        print(ATTRIBUTE_SERIALIZERS[attr_name])
        return ATTRIBUTE_SERIALIZERS[attr_name]
    return None


# products/v1/{id}
# TODO: Remove in production
@method_decorator(csrf_exempt, name='dispatch')
class ProductView(APIView):
    # CRUD operation for PRODUCTS only
    @csrf_exempt
    def post(self, request):
        # TODO: Handle id passed with requestBody
        try:
            data = json.loads(request.body)
            serializer = ProductSerializer(data=data, many=False)

            print(data, type(data))

            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, safe=False, status=201)

            else:
                JsonResponse({f'{serializer.errors}': 'Failed creating product, invalid serializer'}, status=400)


        except JSONDecodeError:
            return JsonResponse({f'{JSONDecodeError}': 'Failed creating product, invalid json'}, status=400)

    def get(self, request):
        # If request is GET automatically comes here.
        # configure this method to check if request has an id passed to it. if yes, then give the details of one product
        products = Product.objects.all()

        serializer = ProductSerializer(products, many=True)
        print(JsonResponse(serializer.data, safe=False).getvalue())

        return JsonResponse(serializer.data, safe=False)

    @csrf_exempt
    def put(self, request, product_id):
        try:
            product_to_update = Product.objects.get(pk=product_id)
            serializer = ProductSerializer(instance=product_to_update, data=json.loads(request.body))

            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=200, safe=False)

            return JsonResponse({"Error": "Serializer not valid"}, status=404)
        except Product.DoesNotExist:
            return JsonResponse({"Error": "Product does not exist"}, status=404)

    def delete(self, request, product_id):
        try:
            product_to_delete = Product.objects.get(pk=product_id)
            product_to_delete.delete()
            return JsonResponse({"Success": "Product deleted"}, status=200)

        except Product.DoesNotExist:
            return JsonResponse({"Error": "Product does not exist"}, status=404)


'''
CRUD+ operations for ProductSku model 
'''


class ProductSkuListCreateAPIView(generics.ListCreateAPIView):
    queryset = ProductSkus.objects.all()
    serializer_class = ProductSkuSerializer
    '''Basic Create for POST method with proper json data
    Basic List for GET method
    '''


class ProductSkuUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):  # /<int:product_id>
    queryset = ProductSkus.objects.all()
    serializer_class = ProductSkuSerializer
    lookup_url_kwarg = 'id'
    lookup_field = 'id'


'''
CRUD for Attributes. Handles dynamically
'''


class ProductAttributeListCreateAPIView(APIView):

    def get(self, request, attribute_name):
        serializer_class = getSerializer(attribute_name)
        model_name = f"{attribute_name.capitalize()}Attribute"
        if serializer_class:
            try:
                model_class = apps.get_model('products', model_name)
                attribute = model_class.objects.all()
                serializer = serializer_class(attribute, many=True)
                return JsonResponse(serializer.data,safe=False)
            except LookupError:
                return JsonResponse({f'Error': 'Model class or attributes not found, check model name'}, status=400)

        return JsonResponse({f'Error': 'No serializer class, add it the dictionary'}, status=400)

    def post(self):
        pass
