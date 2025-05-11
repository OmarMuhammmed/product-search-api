from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Category, Brand, NutritionFact, Product

class ProductSearchAPITestCase(TestCase):
    def setUp(self):
        """Set up test data"""
        # Create categories
        self.dairy = Category.objects.create(name='Dairy', description='Milk and dairy products')
        self.beverages = Category.objects.create(name='Beverages', description='Drinks and liquids')
        
        # Create brands
        self.almarai = Brand.objects.create(name='Al Marai', country_of_origin='Saudi Arabia')
        self.coca_cola = Brand.objects.create(name='Coca-Cola', country_of_origin='USA')
        
        # Create nutrition facts
        self.milk_nutrition = NutritionFact.objects.create(
            calories=150, protein=8, carbohydrates=12, fat=8, sugar=12, sodium=100
        )
        self.cola_nutrition = NutritionFact.objects.create(
            calories=140, protein=0, carbohydrates=39, fat=0, sugar=39, sodium=45
        )
        
        # Create products
        self.milk = Product.objects.create(
            name='Milk',
            name_ar='حليب',
            description='Fresh cow milk',
            description_ar='حليب بقر طازج',
            sku='MILK001',
            price=3.99,
            brand=self.almarai,
            category=self.dairy,
            nutrition_facts=self.milk_nutrition,
            is_active=True
        )
        
        self.cola = Product.objects.create(
            name='Cola Drink',
            name_ar='مشروب الكولا',
            description='Refreshing cola beverage',
            description_ar='مشروب كولا منعش',
            sku='COLA001',
            price=1.99,
            brand=self.coca_cola,
            category=self.beverages,
            nutrition_facts=self.cola_nutrition,
            is_active=True
        )
        
        # Create an inactive product
        self.inactive_product = Product.objects.create(
            name='Inactive Product',
            sku='INACTIVE001',
            price=9.99,
            brand=self.almarai,
            category=self.dairy,
            is_active=False
        )
        
        # Initialize the API client
        self.client = APIClient()
    
    def test_search_exact_match(self):
        """Test search with exact match"""
        url = reverse('product-search')
        response = self.client.get(url, {'q': 'Milk'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['name'], 'Milk')
    
    def test_search_partial_match(self):
        """Test search with partial match"""
        url = reverse('product-search')
        response = self.client.get(url, {'q': 'Co'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['name'], 'Cola Drink')
    
    def test_search_arabic(self):
        """Test search with Arabic text"""
        url = reverse('product-search')
        response = self.client.get(url, {'q': 'حليب'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['name'], 'Milk')
    
    def test_search_with_filter(self):
        """Test search with category filter"""
        url = reverse('product-search')
        response = self.client.get(url, {'q': '', 'category': self.dairy.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)  # Only active products
        self.assertEqual(response.data['results'][0]['name'], 'Milk')
    
    def test_search_price_range(self):
        """Test search with price range"""
        url = reverse('product-search')
        response = self.client.get(url, {'min_price': 3.00, 'max_price': 5.00})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['name'], 'Milk')
    
    def test_inactive_products_excluded(self):
        """Test that inactive products are excluded from search results"""
        url = reverse('product-search')
        response = self.client.get(url, {'q': 'Inactive'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)  # Should not find inactive products
