import argparse
from faker import Faker
import random
from datetime import datetime, timedelta
import uuid
import os

from files import fetch_product_data, fetch_transaction_data, append_to_csv

# -------------------- VALUES -------------------- #

START_DATE = datetime.strptime("2023-01-01", "%Y-%m-%d")
END_DATE = datetime.today()

CSV = "C:/Users/shayn/OneDrive/Desktop/L3/python/data/transactions.csv"

# -------------------- FUNCTIONS -------------------- #

fake = Faker(locale='fr_CA')

def generate_quebec_address():
    while True:
        address = fake.address()
        if "Québec" in address or "QC" in address:
            address = address.replace('\n', ', ')
            if "Suite" not in address and "Apt." not in address:
                return address

def generate_date(start_date=START_DATE, end_date=END_DATE):
    time_delta = end_date - start_date
    random_days = random.randint(0, time_delta.days)
    random_date = (start_date + timedelta(days=random_days)).strftime("%Y%m%d")
    return random_date

def transaction_new_customer(max_id):
    num_items = random.randint(1, 5)
    product_data = fetch_product_data(num_items)

    rate = 0.016

    transaction_id = uuid.uuid4().hex
    date = generate_date()
    store_id = int(f'1200{num_items}')

    customer_id = max_id + 1
    customer_name = fake.name()
    email = (f"{''.join(customer_name.split())}@email.com")
    address = generate_quebec_address()
    phone = fake.phone_number()
    card_number = fake.credit_card_number()

    for chosen_product in product_data:
        product_id = chosen_product[0]
        price_cad = round(float(chosen_product[4]) * rate, 2)

        data_row = [
                    transaction_id,              # Transaction ID
                    date,                        # Date
                    store_id,                    # Store ID
                    product_id,                  # Product ID
                    price_cad,                   # Price in CAD
                    customer_id,                 # Customer ID
                    customer_name,               # Customer Name
                    email,                       # Customer Email
                    address,                     # Customer Address
                    phone,                       # Customer Phone
                    card_number                  # Customer Card Number
                ]
        
        append_to_csv(data_row)
    return customer_id

def transaction_returning_customer(max_id):
    num_items = random.randint(1, 5)
    product_data = fetch_product_data(num_items)

    if not os.path.exists(CSV):
        transaction_new_customer(max_id)
        return

    transaction_data = fetch_transaction_data(num_items)
    existing_customer = random.choice(transaction_data)

    rate = 0.016

    transaction_id = uuid.uuid4().hex
    date = generate_date()
    store_id = int(f'1200{num_items}')

    for chosen_product in product_data:
        product_id = chosen_product[0]
        price_cad = round(float(chosen_product[4]) * rate, 2)

        data_row = [
                    transaction_id,              # Transaction ID
                    date,                        # Date
                    store_id,                    # Store ID
                    product_id,                  # Product ID
                    price_cad,                   # Price in CAD
                    existing_customer[5],        # Customer ID
                    existing_customer[6],        # Customer Name
                    existing_customer[7],        # Customer Email
                    existing_customer[8],        # Customer Address
                    existing_customer[9],        # Customer Phone
                    existing_customer[10]        # Customer Card Number
                ]
        
        append_to_csv(data_row)

def generate_fake_transaction(amount, max_id):
    if os.path.exists(CSV):
        os.remove(CSV)

    for _ in range(amount):
        is_repeat_customer = random.choices([True, False], weights=[0.25, 0.75])[0]

        if is_repeat_customer:
            transaction_returning_customer(max_id)
        else:
            new_id = transaction_new_customer(max_id)
            max_id = max(max_id, new_id)  # Update max_id with the new customer ID
    
    print("### TRANSACTIONS COMPLETE ###")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate fake transaction data.")
    parser.add_argument("amount", type=int, help="Number of transactions to generate.")
    parser.add_argument("--max_id", type=int, default=0, help="Starting max customer ID.")


    args = parser.parse_args()

    generate_fake_transaction(args.amount, args.max_id)

# {path}/dist/transactions.exe 50 --max_id 100
