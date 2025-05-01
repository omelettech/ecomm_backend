from json import JSONDecodeError

from django.core import serializers
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import JSONParser
from django.views import View
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.utils import json
from rest_framework.views import APIView
from django.apps import apps
from products.models import Product, ProductSku
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


class ProductPagination(PageNumberPagination):
    page_size = 5  # Show 5 employees per page


# products/v1/{id}
class ProductView(APIView):
    serializer_class = ProductSerializer
    pagination_class = ProductPagination

    def get_permissions(self):
        if self.request.method != 'GET':
            # Only allow admins to create
            return [IsAdminUser()]
        return [AllowAny()]  # CRUD operation for PRODUCTS only

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
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        print(JsonResponse(serializer.data, safe=False).getvalue())

        return JsonResponse(serializer.data, safe=False)

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


def get_featured_products(request):
    # If request is GET automatically comes here.
    if request.method == 'GET':
        products = Product.objects.filter(featured=True)
        serializer = []

        for product in products:
            # get the default sku
            default_sku = ProductSku.objects.filter(product=product).first()

            # parse the serializer data for the product
            serializer_data = ProductSerializer(product, many=False).data

            # add the default sku to the serializer data
            serializer_data["default_sku"] = ProductSkuSerializer(default_sku).data if default_sku else None

            # append the data to the serializer
            serializer.append(serializer_data)

        return JsonResponse(serializer, safe=False)
    else:
        return JsonResponse({"Error": f"{request.method} not allowed"}, status=405)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_products_with_default_variations(request):
    paginator = PageNumberPagination()  # Instantiate paginator
    paginator.page_size = request.GET.get("page_size", 1)  # Default page size = 10

    products = Product.objects.all()  # Get all products
    paginated_products = paginator.paginate_queryset(products, request)  # Apply pagination

    serialized_products = []
    for product in paginated_products:
        default_sku = ProductSku.objects.filter(product=product).first()

        serializer_data = ProductSerializer(product, many=False).data
        serializer_data["default_sku"] = ProductSkuSerializer(default_sku).data if default_sku else None

        serialized_products.append(serializer_data)

    return paginator.get_paginated_response(serialized_products)  # Return paginated response

'''
CRUD+ operations for ProductSku model 
'''


class ProductSkuListCreateAPIView(generics.ListCreateAPIView):
    queryset = ProductSku.objects.all()
    serializer_class = ProductSkuSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            # Only allow admins to create
            return [IsAdminUser()]
        return [AllowAny()]

    '''Basic Create for POST method with proper json data
    Basic List for GET method
    '''


class ProductSkuUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):  # /<int:product_id>
    queryset = ProductSku.objects.all()
    serializer_class = ProductSkuSerializer
    lookup_url_kwarg = 'id'
    lookup_field = 'id'

    def get_permissions(self):
        if self.request.method == 'GET':
            # Only allow admins to create
            return [IsAdminUser()]
        return [AllowAny()]
    # TODO: Add a get method with product_id as param that returns the top sold product_sku variation to display the image and the price


class ProductSkusByProductId(APIView):

    def get_permissions(self):
        if self.request.method != 'GET':
            # Only allow admins to create
            return [IsAdminUser()]
        return [AllowAny()]

    def get(self, request, product_id):
        try:
            product_skus = ProductSku.objects.filter(product_id=product_id)
            serializer = ProductSkuSerializer(product_skus, many=True)
            return JsonResponse(serializer.data, status=200, safe=False)
        except ProductSku.DoesNotExist:
            return JsonResponse({"error:": "No product_skus exists"}, status=400)


'''
CRUD for Attributes. Handles dynamically
'''


class ProductAttributeListCreateAPIView(APIView):

    def get(self, request, attribute_name):
        serializer_class = getSerializer(attribute_name)
        model_class = apps.get_model('products', f"{attribute_name.capitalize()}Attribute")
        if serializer_class:
            try:
                attribute = model_class.objects.all()
                serializer = serializer_class(attribute, many=True)
                if serializer:
                    return JsonResponse(serializer.data, safe=False)
            except LookupError:
                return JsonResponse({f'Error': 'Model class or attributes not found, check model name'}, status=400)

        return JsonResponse({f'Error': 'No serializer class, add it the dictionary'}, status=400)

    def post(self, request, attribute_name):

        serializer_class = getSerializer(attribute_name)

        if serializer_class:
            try:
                data = json.loads(request.body)
                serializer = serializer_class(data=data, many=False)

                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse(serializer.data, safe=False)

            except LookupError:
                return JsonResponse({f'Error': 'attributes not found, check model name'}, status=400)

        return JsonResponse({f'Error': 'No serializer class, add it the dictionary'}, status=400)
