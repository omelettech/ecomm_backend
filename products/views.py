from json import JSONDecodeError

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.views import View
from rest_framework.utils import json
from rest_framework.views import APIView

from products.models import Product
from products.serializers import ProductSerializer


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
