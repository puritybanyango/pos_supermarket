Supermarket Point of Sale API

This is a complete backend system built for a supermarket. It handles all the backend business logic needed to run a checkout system, manage stock, and track sales data safely.
The project is built using Python, FastAPI, and SQLAlchemy to connect to a PostgreSQL database.

What the project does

Inventory Management: You can create, read, update, and delete Products, Categories, and Suppliers.
Sales: When you process a sale, the system checks if you have enough items in stock, calculates the total amount with a 10% tax rate, and automatically subtracts the purchased quantity from your inventory.
Safety Rules: The database has strict relationship rules. For example, you can't create a sale item for a product ID that doesn't exist, which keeps the data clean.
Receipt Tracking: The system creates an unchangeable audit receipt tracking code for every single completed sale.
Loyalty Points: Customers automatically earn 1 loyalty point for every 100 units of money spent during a transaction.

How the Code is Organized
The project uses a clean, separated structure where every database table has its own file across the packages:

database.py: Sets up the connection to the database.
main.py: The starting point of the app that loads everything and builds the tables.
app/models/: Contains the actual database table layouts and relationship paths.
app/schemas/: Contains the Pydantic data profiles that check and validate user input.
app/services/: The brain of the app that does all the heavy lifting (math, stock checks, database writes).
app/routers/: The front doors of the API that accept requests from Postman or a browser and send back answers.

How to Run the App Locally
Set up your virtual environment
Open your terminal inside this folder and run:
'python -m venv env'

Activate:
'source env/bin/activate`


Install the required libraries
Run the following command to download all the packages needed for this project:
pip install -r requirements.txt

Run the development server
Start your local server by running:
uvicorn main:app --reload

Test the API
Once the server is running, open the web browser and go to:
http://127.0.0

This will open the interactive Swagger UI page where you can see and test every single endpoint using sample data. You can also connect Postman to the exact same URL links to run your tests.
