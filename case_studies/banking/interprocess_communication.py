from multiprocessing import Pool, Manager
from multiprocessing.managers import ListProxy
from typing import List

from customer import Customer, Transaction
from utils import divide_list


def find_customer(customers, id):
    i = 0
    for customer in customers:
        if customer.id == id:
            return customer, i
        
        i += 1


def worker(transactions: List[Transaction], customers: ListProxy):
    for transaction in transactions:
        customer, index = find_customer(customers, transaction.customer_id)
        customer.new_transaction(transaction)
        customers[index] = customer


def process_transactions_parallel(
    customers: List[Customer],
    transactions: List[Transaction],
    number_of_workers: int = 1
):
    
    assert number_of_workers > 0

    manager = Manager()
    customers_manager = manager.list(customers)

    divided_transactions = divide_list(transactions, number_of_workers)
    args = [(part_of_transactions, customers_manager) for part_of_transactions in divided_transactions]

    pool = Pool(processes=number_of_workers)
    pool.starmap(worker, args)

    pool.close()
    pool.join()

    return list(customers_manager)
