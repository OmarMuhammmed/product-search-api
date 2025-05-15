# Product Search API

A powerful and efficient product search API built with Django and PostgreSQL. This API provides advanced search capabilities for products, including handling partial keywords, misspellings, and mixed-language queries (English/Arabic).

## Task Overview

This API is designed to handle large-scale product searches with the following key features:
- Full-text search with PostgreSQL's advanced search capabilities
- Multi-language support (English/Arabic)
- Fuzzy matching for handling misspellings
- Partial keyword matching
- Advanced filtering and sorting
- Performance optimization with caching
- Comprehensive nutrition facts tracking

## Tech Stack

- **Backend Framework**: Django , Django REST Framework (DRF)
- **Database**: PostgreSQL 12+
- **Additional Libraries**:
  - django-filter: For advanced filtering
  - django-cors-headers: For CORS support
  - psycopg2-binary: PostgreSQL adapter
  - django-cacheops: For query caching

## Features

### Search Accuracy and Relevance 
- Full-text search across product names and descriptions
- Fuzzy matching for handling misspellings
- Support for partial keywords
- Mixed language support (English/Arabic)
- Smart ranking of search results
- Support for compound queries

### Performance and Query Optimization 
- PostgreSQL full-text search indexing
- Query result caching
- Efficient database queries
- Pagination support
- Optimized response times

### Code Quality and Structure 
- Clean, maintainable Django code
- Follows Django best practices
- Modular architecture
- Comprehensive test coverage
- Well-documented code

### Documentation and Usability 
- Clear API documentation
- Example usage
- Setup instructions
- Testing guidelines

### Bonus Features 
- Advanced filtering capabilities
- Response caching
- Rate limiting
- Bulk operations support

##  API Documentation

### Categories

- `GET /api/categories/` - List all categories
- `GET /api/categories/{id}/` - Retrieve a specific category

### Brands

- `GET /api/brands/` - List all brands
- `GET /api/brands/{id}/` - Retrieve a specific brand

### Products

- `GET /api/products/` - List all products
  - Query Parameters:
    - `category`: Filter by category ID
    - `brand`: Filter by brand ID
    - `ordering`: Sort by field (name, price, created_at)
- `GET /api/products/{id}/` - Retrieve a specific product
- `GET /api/products/search/` - Advanced product search
  - Query Parameters:
    - `q`: Search query (supports full-text search)
    - `category`: Filter by category ID
    - `brand`: Filter by brand ID
    - `min_price`: Filter by minimum price
    - `max_price`: Filter by maximum price

##  Data Models

### Category
- `name` (string): Category name
- `description` (text, optional): Category description

### Brand
- `name` (string): Brand name
- `description` (text, optional): Brand description
- `country_of_origin` (string, optional): Country of origin

### Product
- `name` (string): Product name
- `name_ar` (string, optional): Product name in Arabic
- `description` (text, optional): Product description
- `description_ar` (text, optional): Product description in Arabic
- `sku` (string): Unique product identifier
- `price` (decimal): Product price
- `brand` (foreign key): Associated brand
- `category` (foreign key): Associated category
- `nutrition_facts` (one-to-one): Associated nutrition facts
- `is_active` (boolean): Product availability status
- `created_at` (datetime): Creation timestamp
- `updated_at` (datetime): Last update timestamp

### NutritionFacts
- `calories` (float, optional): Calorie content
- `protein` (float, optional): Protein content in grams
- `carbohydrates` (float, optional): Carbohydrate content in grams
- `fat` (float, optional): Fat content in grams
- `sugar` (float, optional): Sugar content in grams
- `sodium` (float, optional): Sodium content in mg

## Setup Instructions

### Prerequisites

- Python 3.8+
- PostgreSQL 12+
- pip (Python package manager)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/OmarMuhammmed/product-search-api.git
   cd product-search-api
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure PostgreSQL:
   - Create a new database
   - Update settings.py with your database credentials

5. Run migrations:
   ```bash
   python manage.py migrate
   ```

6. Create a superuser (optional):
   ```bash
   python manage.py createsuperuser
   ```

7. Start the development server:
   ```bash
   python manage.py runserver
   ```

##  Testing

### Running Tests

```bash
python manage.py test
```

### Test Coverage

```bash
coverage run manage.py test
coverage report
```

##  Performance Optimization

### Database Indexing
- Full-text search indexes on product names and descriptions
- Indexes on frequently queried fields
- Composite indexes for common query patterns

### Caching Strategy
- Category and brand listings cached for 1 hour
- Search results cached based on query parameters
- Cache invalidation on data updates

### Query Optimization
- Efficient use of PostgreSQL's full-text search
- Optimized JOIN operations
- Pagination for large result sets

## Security

- CORS configuration
- Rate limiting
- Input validation
- SQL injection prevention
- XSS protection

## Monitoring

- Query performance monitoring
- Cache hit/miss tracking
- Error logging
- Response time tracking


