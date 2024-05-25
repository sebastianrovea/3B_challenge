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
1. Create and activate virtual enviroment:
    a. ***python3 -m venv venv***
    b. ***source venv/bin/activate (Linux)***
    b. ***source venv/Scripts/activate (Windows)***
2. Install dependecies:
    a. ***pip install -r requirements.txt***
3. Create and up local database to test:
    a. ***py manage.py makemigrations business_logic***
    b. ***py manage.py migrate***
4. Run server:
    a. ***py manage.py runserver 8000*** (Elegir puerto disponible, default es 8000)
    b. Validate services: A Postman collection is shared to validate services
    c. See documentation running this url: http://localhost:8000/swagger/ in your local internet navigator.
5. Database is empty.
    Use service to add new products, add stock, see the products or generate an order.
    Use Postman collection shared to validate different services and fill Db with information.
6. Run cron to check lower stock:
    a. Open another console
    b. Activate virtual enviroment: ***source venv/bin/activate***
    c. configure the execution time using the variable **TIME_CHECK_LOWER_STOCK** of the business_logic/util/const.py file
        Now is setting with 10 seconds.
    d. Run: ***py manage.py runserver_cron***
    e. In this console, you will see next text each 10 seconds: "Starting job to check lower stock"
        and you will see the alert if exist a lower stock.
7. Close your server and cron:
    a. Quit the server with CTRL-BREAK in your console
    b. Quit the cron with CTRL-BREAK in your another console
8. Deactivate virtual enviroment:
    a. ***deactivate***

## Testing
Open virtual enviroment (source venv/Script/activate)
Run this command: ***py manage.py test business_logic***

## Documentation
You could see the documentation running this url in your explorer:
You could see step by step following the "Deploy locally to validate services" steps.
    Point 4: Run server, subsection c: See documentation
```bash
http://localhost:8000/swagger/
```