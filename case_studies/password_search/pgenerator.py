import hashlib
import csv
import sys

from password_generator import PasswordGenerator


file_prefix = 'data/hashed_passwords'
number_of_passwords = int(sys.argv[1])

pwo = PasswordGenerator()
sha256 = hashlib.sha256()

hashed_passwords = []

print('Starting...')

for _ in range(number_of_passwords):
    password = pwo.generate()

    sha256.update(password.encode('utf-8'))
    hashed_password = sha256.hexdigest()

    hashed_passwords.append({
        'password': password,
        'hashed_password': hashed_password
    })

with open(f'{file_prefix}{number_of_passwords}.csv', 'w', newline='') as file:
    writer = csv.DictWriter(
        file,
        fieldnames=['password', 'hashed_password']
    )

    writer.writeheader()
    writer.writerows(hashed_passwords)

print(f'Done! {number_of_passwords} passwords are recorded \
in the "{file_prefix}{number_of_passwords}.csv"')
