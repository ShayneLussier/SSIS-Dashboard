import csv
import random

PRODUCTS = "C:/Users/shayn/OneDrive/Desktop/L3/python/data/products.csv"
TRANSACTIONS = "C:/Users/shayn/OneDrive/Desktop/L3/python/data/transactions.csv"

def fetch_product_data(num_items):
    rows = []
    
    with open(PRODUCTS, encoding='utf-8') as file:
        reader = csv.reader(file)
        rows = list(reader)
    
    num_items = min(num_items, len(rows))
    # Randomly select num_items rows
    selected_rows = random.sample(rows, num_items)
    
    return selected_rows

def fetch_transaction_data(num_items):
    rows = []

    with open(TRANSACTIONS, encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        rows = list(reader)
    
    num_items = min(num_items, len(rows))
    # Randomly select num_items rows
    selected_rows = random.sample(rows, num_items)
    
    return selected_rows

def append_to_csv(data):
    with open(TRANSACTIONS, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(data)