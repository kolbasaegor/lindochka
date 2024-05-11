from typing import List

from customer import Customer, Transaction


def process_transactions_sequential(
    customers: List[Customer],
    transactions: List[Transaction]
):
    
    for transaction in transactions:
        for customer in customers:
            if customer.id == transaction.customer_id:
                customer.new_transaction(transaction)
                break

    return customers
