from django.test import TestCase
from rest_framework.test import APITestCase
import datetime
from .models import *
from rest_framework import status
from rest_framework.reverse import reverse as api_reverse
from rest_framework.test import APIRequestFactory
import json

factory = APIRequestFactory()

class TestingAPITestCase(APITestCase):
    def setUp(self):

        userObject = Users(username="reaganscofield", email="reaganscofield@outlook.com")
        userObject.set_password("someRandomPassword123456")
        userObject.save()

        products = Products.objects.create(
            name = "Artificial Intelligence",
            price = 234.0,
            file = "test.jpg",
            created_at = datetime.datetime.now(),
            updated_at = None,
            active = True,
            deleted_at = None
        )

        addCard = AddCard.objects.create(
            product_id = products,
            customer_id = userObject,
            product_name = products.name,
            product_price = products.price,
            number_of_items = 23,
            active = True,
            created_at = datetime.datetime.now(),
            updated_at = None,
            deleted_at = None,
        )

        bought = Bought.objects.create(
            product_id = products,
            customer_id = userObject,
            payments_id = "6aa3fb27-83f1-427e-a245-10e66892795f",
            total_paid = 2345,
            total_tax = 34.34,
            total_discount = 12.0,
            paid_at = datetime.datetime.now(),
            active = True,
            created_at = datetime.datetime.now(),
            updated_at = None,
            deleted_at = None
        )

    
    def test(self):
        products = Products.objects.count()
        self.assertEqual(products, 1)

    def test_user(self):
        user = Users.objects.count()
        self.assertEqual(user, 1)

    def test_add_card(self):
        addcard = AddCard.objects.count()
        self.assertEqual(addcard, 1)

    def test_bought(self):
        bought = Bought.objects.count()
        self.assertEqual(bought, 1)

    def test_user_login(self):
        data = {
            'username': 'reaganscofield',
            'password': 'someRandomPassword123456'
        }
        url = api_reverse("login-view")
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data.get("token")
        print(f"returned token is : {token}")

    def test_search(self):
        request = factory.get('api/products_searc/?name=Artificial Intelligence')
        self.assertEqual(Products.objects.count(), 1)
        self.assertEqual(Products.objects.get().name, 'Artificial Intelligence')
        print(request)


    def test_bought_create(self):
        data = {
            'name': "Artificial Intelligence",
            'price': 234.0,
            'file': "test.jpg",
            'created_at': None,
            'updated_at':  None,
            'active':  True,
            'deleted_at': None
        }
        request = factory.post('products/', json.dumps(data), content_type='application/json')
        print(request)























