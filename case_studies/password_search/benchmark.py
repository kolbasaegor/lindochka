import time
import random

from utils import from_csv_to_dict, get_random_passwords
from sequential_approach import search_passwords_sequential
from linda_approach import search_password_linda


random.seed(52)

number_of_passwords = 1000000
number_of_passwords_to_search = 5000

db = from_csv_to_dict(f'data/hashed_passwords{number_of_passwords}.csv')

passwords_to_search = get_random_passwords(
    db=db,
    num=number_of_passwords_to_search,
)

if __name__ == "__main__":

    _, time_ = search_passwords_sequential(passwords_to_search, db)
    print("t1 =", time_, "s")

    _, time_ = search_password_linda(passwords_to_search, db, number_of_workers=4)
    print("t2 =", time_, "s")
