import random
from django.core.management.base import BaseCommand
from products.models import Category, Brand, NutritionFact, Product

class Command(BaseCommand):
    help = 'Loads sample data for testing the product search API'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating sample data...')
        
        # Create categories
        categories = [
            {'name': 'Beverages', 'description': 'Drinks and liquids'},
            {'name': 'Dairy', 'description': 'Milk and dairy products'},
            {'name': 'Bakery', 'description': 'Bread and baked goods'},
            {'name': 'Fruits', 'description': 'Fresh fruits'},
            {'name': 'Vegetables', 'description': 'Fresh vegetables'},
            {'name': 'Snacks', 'description': 'Chips, nuts, and other snacks'},
            {'name': 'Canned Goods', 'description': 'Canned and jarred items'},
            {'name': 'Frozen Foods', 'description': 'Frozen meals and ingredients'},
        ]
        
        for cat_data in categories:
            Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
        
        # Create brands
        brands = [
            {'name': 'Nestle', 'country_of_origin': 'Switzerland'},
            {'name': 'Pepsi', 'country_of_origin': 'USA'},
            {'name': 'Coca-Cola', 'country_of_origin': 'USA'},
            {'name': 'Danone', 'country_of_origin': 'France'},
            {'name': 'Kellogg\'s', 'country_of_origin': 'USA'},
            {'name': 'General Mills', 'country_of_origin': 'USA'},
            {'name': 'Kraft Heinz', 'country_of_origin': 'USA'},
            {'name': 'Unilever', 'country_of_origin': 'UK/Netherlands'},
            {'name': 'Al Marai', 'country_of_origin': 'Saudi Arabia'},
            {'name': 'Nadec', 'country_of_origin': 'Saudi Arabia'},
        ]
        
        for brand_data in brands:
            Brand.objects.get_or_create(
                name=brand_data['name'],
                defaults={'country_of_origin': brand_data['country_of_origin']}
            )
        
        # Create products with nutrition facts
        products = [
            {
                'name': 'Milk', 
                'name_ar': 'حليب',
                'description': 'Fresh cow milk',
                'description_ar': 'حليب بقر طازج',
                'sku': 'MILK001',
                'price': 3.99,
                'brand': 'Al Marai',
                'category': 'Dairy',
                'nutrition': {
                    'calories': 150,
                    'protein': 8,
                    'carbohydrates': 12,
                    'fat': 8,
                    'sugar': 12,
                    'sodium': 100
                }
            },
            {
                'name': 'Whole Wheat Bread',
                'name_ar': 'خبز القمح الكامل',
                'description': 'Healthy whole wheat bread',
                'description_ar': 'خبز صحي من القمح الكامل',
                'sku': 'BREAD001',
                'price': 2.49,
                'brand': 'Nadec',
                'category': 'Bakery',
                'nutrition': {
                    'calories': 80,
                    'protein': 4,
                    'carbohydrates': 15,
                    'fat': 1,
                    'sugar': 2,
                    'sodium': 150
                }
            },
            {
                'name': 'Cola Drink',
                'name_ar': 'مشروب الكولا',
                'description': 'Refreshing cola beverage',
                'description_ar': 'مشروب كولا منعش',
                'sku': 'COLA001',
                'price': 1.99,
                'brand': 'Coca-Cola',
                'category': 'Beverages',
                'nutrition': {
                    'calories': 140,
                    'protein': 0,
                    'carbohydrates': 39,
                    'fat': 0,
                    'sugar': 39,
                    'sodium': 45
                }
            },
            # Add more products as needed
        ]
        
        # Create 100 more random products for testing
        for i in range(1, 101):
            category = random.choice(Category.objects.all())
            brand = random.choice(Brand.objects.all())
            
            product_name = f"Product {i}"
            product_name_ar = f"منتج {i}"
            
            products.append({
                'name': product_name,
                'name_ar': product_name_ar,
                'description': f"Description for {product_name}",
                'description_ar': f"وصف ل {product_name_ar}",
                'sku': f"SKU{i:04d}",
                'price': round(random.uniform(0.99, 99.99), 2),
                'brand': brand.name,
                'category': category.name,
                'nutrition': {
                    'calories': random.randint(0, 500),
                    'protein': random.randint(0, 30),
                    'carbohydrates': random.randint(0, 50),
                    'fat': random.randint(0, 30),
                    'sugar': random.randint(0, 30),
                    'sodium': random.randint(0, 500)
                }
            })
        
        # Create the products
        for product_data in products:
            brand = Brand.objects.get(name=product_data['brand'])
            category = Category.objects.get(name=product_data['category'])
            
            # Create or update nutrition facts
            nutrition_data = product_data['nutrition']
            nutrition, _ = NutritionFact.objects.get_or_create(
                calories=nutrition_data['calories'],
                protein=nutrition_data['protein'],
                carbohydrates=nutrition_data['carbohydrates'],
                fat=nutrition_data['fat'],
                sugar=nutrition_data['sugar'],
                sodium=nutrition_data['sodium']
            )
            
            # Create or update product
            product, created = Product.objects.get_or_create(
                sku=product_data['sku'],
                defaults={
                    'name': product_data['name'],
                    'name_ar': product_data['name_ar'],
                    'description': product_data['description'],
                    'description_ar': product_data['description_ar'],
                    'price': product_data['price'],
                    'brand': brand,
                    'category': category,
                    'nutrition_facts': nutrition,
                    'is_active': True
                }
            )
            
            if created:
                self.stdout.write(f"Created product: {product.name}")
            else:
                self.stdout.write(f"Updated product: {product.name}")
        
        self.stdout.write(self.style.SUCCESS('Successfully loaded sample data!'))