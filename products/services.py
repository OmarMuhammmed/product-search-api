from django.db.models import Q, Value, F, FloatField
from django.contrib.postgres.search import SearchQuery, SearchRank
from .models import Product

class ProductSearchService:

    @staticmethod
    def search(query_string, **filters):
        """
        Perform a comprehensive search on products using multiple techniques:
        1. Full-text search using PostgreSQL's search capabilities
        2. Direct field matching for partial keywords
        """
        if not query_string:
            # If no search query, return filtered queryset
            queryset = Product.objects.filter(is_active=True)
            return ProductSearchService._apply_filters(queryset, **filters)
        
        # Clean the query string
        query_string = query_string.strip()
        
        # 1. Full-text search
        search_query = SearchQuery(query_string, config='english')
        full_text_results = Product.objects.filter(
            search_vector=search_query,
            is_active=True
        ).annotate(
            rank=SearchRank(F('search_vector'), search_query)
        )
        
        # 2. Direct field matching for partial keywords
        partial_match_results = Product.objects.filter(
            Q(name__icontains=query_string) |
            Q(name_ar__icontains=query_string) |
            Q(description__icontains=query_string) |
            Q(description_ar__icontains=query_string) |
            Q(brand__name__icontains=query_string) |
            Q(category__name__icontains=query_string),
            is_active=True
        ).annotate(
            rank=Value(0.0, output_field=FloatField())  # Add rank field with default value
        )
        
        # Combine results (using UNION to remove duplicates)
        combined_results = full_text_results.union(partial_match_results)
        
        # Apply additional filters
        filtered_results = ProductSearchService._apply_filters(combined_results, **filters)
        
        # Order by relevance (if from full-text search) or name
        if query_string:
            return filtered_results.order_by('-rank', 'name')
        return filtered_results.order_by('name')
    
    @staticmethod
    def _apply_filters(queryset, **filters):
        """Apply additional filters to the queryset"""
        if 'category' in filters and filters['category']:
            queryset = queryset.filter(category__id=filters['category'])
        
        if 'brand' in filters and filters['brand']:
            queryset = queryset.filter(brand__id=filters['brand'])
        
        if 'min_price' in filters and filters['min_price']:
            queryset = queryset.filter(price__gte=filters['min_price'])
        
        if 'max_price' in filters and filters['max_price']:
            queryset = queryset.filter(price__lte=filters['max_price'])
            
        return queryset