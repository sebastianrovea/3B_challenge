# 3B Challenge

3B company Challenge.
Goals:
1. Craate api POST /api/products to create a new product.
2. Create api GET /api/products/list to get all products (not mencionated in this challenge).
3. Create api PATCH /inventories/product/<product_id> to update stock in this product.
4. Create api POST /api/orders to create a new order of products.
5. Create a cron job to identify low stock of any product.

## Framework used: Django

## Database E-R schema:

product (1) <---> (N) order_line (N) <---> (1) order

## Tables description

### product
| Campo         | Tipo   |
|---------------|--------|
| id            | INT    |
| sku           | VARCHAR|
| name          | VARCHAR|
| description   | TEXT   |
| stock         | INT    |

### order
| Campo     | Tipo     |
|-----------|----------|
| id        | INT      |
| client    | INT      |
| order_date| DATETIME |

### order_line
| Campo     | Tipo   |
|-----------|--------|
| id        | INT    |
| order_id  | INT    |
| product   | INT    |


### Deploy locally to validate services
(Required to have installed python3 and virtualenv)
1. Create and activate virtual envoroment:
```bash
    a. python3 -m venv venv
    b. source venv/bin/activate (Linux)
    b. source venv/Scripts/activate (Windows)
```
2. Install dependecies:
```bash
    a. pip install -r requirements.txt
```
3. Create and up local database to test:
```bash
    a. py manage.py makemigrations business_logic
    b. py manage.py migrate
```
4. Run server:
```bash
    a. python3 manage.py runserver 8000 (Elegir puerto disponible, default es 8000)
    b. Validate services: A Postman collection is shared to validate services
    c. Quit the server with CTRL-BREAK
```
5. Database is empty.
    Use service to add new products, add stock, see the products or generate an order.
    Use Postman collection shared to validate different services and fill Db with information.
6. Deactivate virtual enviroment:
```bash
    a. deactivate
```

## Testing
Open virtual enviroment (source venv/bin/activate)
Run this command: ***python3 -m pytest test/ --cov=.***