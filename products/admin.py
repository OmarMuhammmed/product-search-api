from django.contrib import admin
from .models import Category, Brand, NutritionFact, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'country_of_origin')
    search_fields = ('name',)

@admin.register(NutritionFact)
class NutritionFactAdmin(admin.ModelAdmin):
    list_display = ('calories', 'protein', 'carbohydrates', 'fat', 'sugar', 'sodium')

# Remove the NutritionFactInline class and use a different approach
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'price', 'brand', 'category', 'is_active')
    list_filter = ('is_active', 'brand', 'category')
    search_fields = ('name', 'name_ar', 'description', 'sku')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('name', 'name_ar', 'sku', 'price', 'brand', 'category', 'is_active')
        }),
        ('Description', {
            'fields': ('description', 'description_ar')
        }),
        ('Nutrition Facts', {
            'fields': ('nutrition_facts',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at')
        }),
    )
