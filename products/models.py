from django.db import models
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name
     
    class Meta:
        verbose_name_plural = "Categories"

class Brand(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    country_of_origin = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return self.name

class NutritionFact(models.Model):
    calories = models.FloatField(blank=True, null=True)
    protein = models.FloatField(blank=True, null=True)  # in grams
    carbohydrates = models.FloatField(blank=True, null=True)  # in grams
    fat = models.FloatField(blank=True, null=True)  # in grams
    sugar = models.FloatField(blank=True, null=True)  # in grams
    sodium = models.FloatField(blank=True, null=True)  # in mg
    
    def __str__(self):
        return f"Nutrition Facts (Cal: {self.calories})"

class Product(models.Model):
    name = models.CharField(max_length=255)
    name_ar = models.CharField(max_length=255, blank=True, null=True)  
    description = models.TextField(blank=True, null=True)
    description_ar = models.TextField(blank=True, null=True)  
    sku = models.CharField(max_length=100, unique=True) # Stock Keeping Unit 
    price = models.DecimalField(max_digits=10, decimal_places=2)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    nutrition_facts = models.OneToOneField(NutritionFact, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    # Search vector field for full text search with postegres
    search_vector = SearchVectorField(null=True) 
    
    def __str__(self):
        return self.name
    
    class Meta:
        indexes = [
            GinIndex(fields=['search_vector']),
        ]
        ordering = ['name']
