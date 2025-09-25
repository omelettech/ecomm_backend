# Django REST API Backend

## Project Overview
This is a Django REST API backend using PostgreSQL as the database. It consists of multiple Django apps, each managing different aspects of the system. The API provides various endpoints for data manipulation and retrieval, with an interactive Swagger documentation available.

## Features
- Django REST Framework (DRF) powered API
- PostgreSQL database
- Modular Django apps
- Swagger API documentation
- Authentication & Authorization

## Installation & Setup
### Prerequisites
Ensure you have the following installed:
- Python 3.x
- PostgreSQL
- pip
- pipenv 

### Setup Instructions
```bash
# Clone the repository
git clone <repo-url>
cd <repo-name>

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Update the .env file with correct database credentials

pipenv shell
# Apply database migrations
python manage.py migrate

# Create a superuser (if needed)
python manage.py createsuperuser

# Run the server
python manage.py runserver
```

## Database Structure
The application consists of several database tables, each corresponding to different Django models. Below is an overview of key tables:
- **Users**: Stores user authentication data
- **Customer**: Contains customer details
- **Gallery**: Manages gallery items for showcasing images
- **Products**: Stores products and their variants
- **ProductSKU**: Stores individual product details
- **Images**: Stores image paths that is delivered by a CDN
- **Orders**: Stores orders, their status and a corresponding profile
- **OrderItem**: Stores individual products as orderitems
- **Carts**: Stores user carts that they can modify
- **CartItems**: Stores individual cart item which is almost the same as products (potential multiple carts in the future)
- **Commissions**: [coming soon] Stores commissions/requests for the Artist by their customers

## API Documentation
The API is documented using Swagger, accessible at:
```
[Your Domain]/swagger/
```

## API Endpoints
### Images
| Method | Endpoint                          | Description                        |
|--------|----------------------------------|------------------------------------|
| GET    | `/images/v1/GalleryItem/`       | Retrieves gallery items           |
| POST   | `/images/v1/GalleryItem/`       | Creates a gallery item            |
| GET    | `/images/v1/GalleryItem/{id}/`  | Retrieves a specific gallery item |
| PUT    | `/images/v1/GalleryItem/{id}/`  | Updates a gallery item            |
| PATCH  | `/images/v1/GalleryItem/{id}/`  | Partially updates a gallery item  |
| DELETE | `/images/v1/GalleryItem/{id}/`  | Deletes a gallery item            |

### Cart
| Method | Endpoint                    | Description                  |
|--------|----------------------------|------------------------------|
| GET    | `/orders/v1/cart/`         | Retrieves all cart items     |
| POST   | `/orders/v1/cart/`         | Creates a new cart item      |
| GET    | `/orders/v1/cart/{id}`     | Retrieves a specific cart item |
| PUT    | `/orders/v1/cart/{id}`     | Updates a cart item         |
| PATCH  | `/orders/v1/cart/{id}`     | Partially updates a cart item |
| DELETE | `/orders/v1/cart/{id}`     | Deletes a cart item         |

### Orders
| Method | Endpoint                   | Description                  |
|--------|---------------------------|------------------------------|
| POST   | `/orders/v1/order`        | Creates a new order         |
| GET    | `/orders/v1/order/{id}`   | Retrieves a specific order  |
| PUT    | `/orders/v1/order/{id}`   | Updates an order            |
| PATCH  | `/orders/v1/order/{id}`   | Partially updates an order  |
| DELETE | `/orders/v1/order/{id}`   | Deletes an order            |

### Products
| Method | Endpoint                                     | Description                        |
|--------|---------------------------------------------|------------------------------------|
| GET    | `/products/v1/product_attribute/{id}`      | Retrieves a product attribute     |
| POST   | `/products/v1/product_attribute/{id}`      | Creates a product attribute       |
| PUT    | `/products/v1/product_attribute/{id}`      | Updates a product attribute       |
| DELETE | `/products/v1/product_attribute/{id}`      | Deletes a product attribute       |
| GET    | `/products/v1/product_skus/`               | Retrieves product SKUs            |
| POST   | `/products/v1/product_skus/`               | Creates a product SKU             |
| GET    | `/products/v1/products`                    | Retrieves all products            |
| POST   | `/products/v1/products`                    | Creates a new product             |
| PUT    | `/products/v1/products`                    | Updates a product                 |
| DELETE | `/products/v1/products`                    | Deletes a product                 |
| GET    | `/products/v1/products/{product_id}`       | Retrieves a specific product      |

### Users
| Method | Endpoint                               | Description                         |
|--------|---------------------------------------|-------------------------------------|
| GET    | `/users/v1/customer/`                | Retrieves customer details         |
| PUT    | `/users/v1/customer/`                | Updates customer details           |
| DELETE | `/users/v1/customer/`                | Deletes a customer                 |
| POST   | `/users/v1/dj-rest-auth/login/`      | Authenticates a user               |
| GET    | `/users/v1/dj-rest-auth/logout/`     | Logs out a user                    |
| POST   | `/users/v1/dj-rest-auth/registration/` | Registers a new user          |
| POST   | `/users/v1/dj-rest-auth/password/reset/` | Resets user password         |
| GET    | `/users/v1/wishlist/`                | Retrieves user wishlist            |
| POST   | `/users/v1/wishlistitem/`            | Adds an item to wishlist           |
| DELETE | `/users/v1/wishlistitem/{product_sku}` | Removes an item from wishlist |

## Contributing
Feel free to contribute to this project by following these steps:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature-name`)
3. Commit changes (`git commit -m 'Add new feature'`)
4. Push to the branch (`git push origin feature-name`)
5. Open a Pull Request

## License
This project is licensed under the MIT License. See the LICENSE file for details.

