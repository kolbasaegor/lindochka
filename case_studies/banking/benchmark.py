import random
import time

from customer import Customer,Transaction
from linda_approach import process_transactions_linda
from interprocess_communication import process_transactions_parallel
from sequential_approach import process_transactions_sequential


random.seed(52)

number_of_customers = 1000 # на измене
number_of_transactions = 100
categories = ['Supermarkets', 'Public transport', 'Beauty and health', 'Car', 'Cafes and restaurants']

customers = [Customer(i) for i in range(number_of_customers)]
transactions = [
    Transaction(
        customer_id=random.randint(0, number_of_customers - 1),
        category=random.choice(categories),
        amount=round(random.uniform(1, 10000), 2)
    ) for _ in range(number_of_transactions)
]

if __name__ == "__main__":
    print('Number of customers:', number_of_customers)
    print('Number of transactions:', number_of_transactions)
    print('----------------------------------')

    start = time.perf_counter()
    process_transactions_linda(customers, transactions, number_of_workers=4)
    end = time.perf_counter()
    print('linda:', end - start, "s")

    start = time.perf_counter()
    process_transactions_parallel(customers, transactions, number_of_workers=4)
    end = time.perf_counter()
    print('interprocess communication::', end - start, "s")

    start = time.perf_counter()
    process_transactions_sequential(customers, transactions)
    end = time.perf_counter()
    print('sequential:', end - start, "s")
    