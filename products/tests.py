import json

from django.test import TestCase

from products.models import Product
from django.urls import reverse

PRODUCT_CREATE_INIT = {
    "name": "Tshirt",
    "description": "basic tshirt",
    "summary": "unisex punk tshirt shirt"
}


class ProductTestCase(TestCase):
    # fixtures = ['products.json']

    def test_product_view(self):

        url = reverse("product_view")
        #Create success
        response=self.client.post(url,data=json.dumps(PRODUCT_CREATE_INIT)
                                  ,content_type='application/json')
        self.assertEqual(response.status_code,201)

        #GET all
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
