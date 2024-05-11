class Transaction:

    def __init__(self, customer_id: int, category: str, amount: float):
        self.customer_id: int = customer_id
        self.category = category
        self.amount = amount


class Customer:

    def __init__(self, id: int):
        self.id: int = id
        self.transaction_count: int = 0
        self.total: float = 0
        self.spending_by_category: dict[str, float] = dict()


    def __str__(self) -> str:
        return f'{self.id=}\n{self.total=}\n{self.transaction_count=}\n{self.spending_by_category=}'

    
    def new_transaction(self, transaction: Transaction) -> None:
        self.transaction_count += 1
        self.total += transaction.amount
        
        if transaction.category in self.spending_by_category:
            self.spending_by_category[f'{transaction.category}'] += transaction.amount
        else:
            self.spending_by_category[f'{transaction.category}'] = transaction.amount
