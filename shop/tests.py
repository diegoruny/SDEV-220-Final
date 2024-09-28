from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Product

# Create your tests here.

class ProductModelTest(TestCase):
    def test_string_representation(self):
        """
        Test that the string representation of a Product object
        is equal to its name.
        """
        product = Product(name="Espresso")
        self.assertEqual(str(product), "Espresso")

class ProductListViewTest(TestCase):
    def setUp(self):
        """
        Set up data for the ProductListView tests.
        Creates a test client and a sample product.
        """
        self.client = Client()
        Product.objects.create(name='Espresso', price=2.50, stock=10)

    def test_view_url_exists_at_desired_location(self):
        """
        Test that the product list view is accessible at the root URL ('/').
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """
        Test that the product list view uses the correct template.
        """
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'shop/product_list.html')

class CartViewTest(TestCase):
    def setUp(self):
        """
        Set up data for the CartView tests.
        Creates a test client and a test user.
        """
        self.client = Client()
        User.objects.create_user(username='testuser', password='testpass')

    def test_redirect_if_not_logged_in(self):
        """
        Test that an unauthenticated user is redirected to the login page
        when trying to access the cart.
        """
        response = self.client.get('/cart/')
        self.assertRedirects(response, '/accounts/login/?next=/cart/')
