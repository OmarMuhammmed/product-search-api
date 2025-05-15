from django.db.models import Q, Value, F, FloatField
from django.db.models.functions import Greatest
from django.contrib.postgres.search import SearchQuery, SearchRank, TrigramSimilarity
from .models import Product

class ProductSearchService:

    @staticmethod
    def search(query_string, **filters):
        """
        Perform a comprehensive search on products using multiple techniques:
        1. Full-text search using PostgreSQL's search capabilities
        2. Trigram similarity for fuzzy matching/misspellings
        3. Direct field matching for partial keywords
        """
        # Initialize queryset
        queryset = Product.objects.filter(is_active=True)
        
        # If no search query, return filtered queryset
        if not query_string or not query_string.strip():
            queryset = ProductSearchService._apply_filters(queryset, **filters)
            return queryset.order_by('name').select_related('brand', 'category')
        
        # Clean the query string
        query_string = query_string.strip()
        
        # Check if query contains Arabic characters
        has_arabic = any('\u0600' <= c <= '\u06FF' for c in query_string) # Retrun True if any character is Arabic
        
        # Create appropriate search configurations
        search_configs = ['english']
        if has_arabic:
            search_configs.append('arabic')
        
        # -----
        
        # Initialize a complex query with multiple ranking components
        queryset = queryset.annotate(
            # Full-text search ranking
            full_text_rank=SearchRank(
                F('search_vector'),
                SearchQuery(query_string, config=search_configs[0])
            ),
            name_similarity=TrigramSimilarity('name', query_string),
            name_ar_similarity=TrigramSimilarity('name_ar', query_string),
            brand_similarity=TrigramSimilarity('brand__name', query_string),
            # Calculate overall relevance score
            relevance=Greatest(
                F('full_text_rank') * Value(2.0, output_field=FloatField()),  # Full-text gets higher weight
                F('name_similarity'),
                F('name_ar_similarity') * Value(0.9 if has_arabic else 0.7, output_field=FloatField()),
                F('brand_similarity') * Value(0.8, output_field=FloatField()),
                Value(0.0, output_field=FloatField())  # Fallback value
            )
        ).filter(
            # Combined filter condition for better performance
            Q(search_vector=SearchQuery(query_string, config=search_configs[0])) |
            Q(name__icontains=query_string) |
            Q(name_ar__icontains=query_string) |
            Q(brand__name__icontains=query_string) |
            Q(category__name__icontains=query_string) |
            # Trigram similarity conditions for fuzzy matching
            Q(name_similarity__gt=0.3) |
            Q(name_ar_similarity__gt=0.3) |
            Q(brand_similarity__gt=0.3)
        )
        
        # Apply additional filters
        queryset = ProductSearchService._apply_filters(queryset, **filters)
        
        # Order by relevance and optimize with select_related
        return queryset.order_by('-relevance', 'name').select_related('brand', 'category')
    
    @staticmethod
    def _apply_filters(queryset, **filters):
        """Apply additional filters to the queryset"""
        
        if 'category' in filters and filters['category']:
            queryset = queryset.filter(category__id=filters['category'])
            
        if 'brand' in filters and filters['brand']:
            queryset = queryset.filter(brand__id=filters['brand'])
            
        if 'min_price' in filters and filters['min_price'] is not None:
            queryset = queryset.filter(price__gte=filters['min_price'])
            
        if 'max_price' in filters and filters['max_price'] is not None:
            queryset = queryset.filter(price__lte=filters['max_price'])
            
        return queryset