import lindypy
import os
from typing import List

from customer import Customer, Transaction
from utils import divide_list


def worker(ts, transactions: List[Transaction]):
    for transaction in transactions:
        customer_tuple = ts.inp(('customer', transaction.customer_id, Customer))
        customer = customer_tuple[2]
        customer.new_transaction(transaction)

        ts.out(('customer', customer.id, customer))

    ts.out(('transactions have been processed', os.getpid()))

    while True:
        pass


def process_transactions_linda(
    customers: List[Customer],
    transactions: List[Transaction],
    number_of_workers: int = 1
):
    
    assert number_of_workers > 0

    divided_transactions = divide_list(transactions, number_of_workers)

    with lindypy.tuplespace() as ts:

        for part_of_transactions in divided_transactions:
            ts.eval(worker, part_of_transactions)

        for customer in customers:
            ts.out(('customer', customer.id, customer))

        for _ in range(number_of_workers):
            ts.inp(('transactions have been processed', int))
