import time

from utils import from_csv_to_dict, get_random_passwords


number_of_passwords = 1000000
number_of_passwords_to_search = 5000

db = from_csv_to_dict(f'data/hashed_passwords{number_of_passwords}.csv')

passwords_to_search = get_random_passwords(
    db=db,
    num=number_of_passwords_to_search,
    seed=52
)

result = []

# --------------------------------------------------------------------

if __name__ == "__main__":
    print(f'{number_of_passwords=}\n{number_of_passwords_to_search=}\n')
    
    print('[start]')
    start = time.perf_counter()

    for hashed_password in passwords_to_search:
        for item in db:
            if hashed_password == item['hashed_password']:
                result.append((item['hashed_password'], item['password']))
                break

    end = time.perf_counter()
    print('[end]')

    print('search time:', end - start, 's')