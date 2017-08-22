from monzo.monzo import Monzo # Import Monzo Class
from dateutil import parser
import pytz
import config as cfg
import csv

def init_monzo():

    client = Monzo(cfg.monzo_token) # Replace access token with a valid token found at: https://developers.getmondo.co.uk/
    account_id = client.get_first_account()['id'] # Get the ID of the first account linked to the access token
    transactions = client.get_transactions(account_id) # Get your balance object
    return transactions

def parse_monzo(transactions):
    transactionsParsed = [];
    for item in transactions['transactions']:
        # Merchant
        try:
            merchant = item['merchant']['name']
        except AttributeError:
            merchant = "No name"
        except TypeError:
            merchant = "No merchant for this item"
        # Date
        date = item['created']
        amount = int(item['amount'])
        transactionsParsed.append({
            'date': parser.parse(date).replace(tzinfo=pytz.UTC),
            'transaction': amount,
            'merchant': merchant})
    return transactionsParsed

def init_santander(filename):
    transactions = []
    with open(filename, encoding='mac_roman', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';')
        for row in spamreader:
            try:
                date = parser.parse(row[0]).replace(tzinfo=pytz.UTC)
                merchant = row[2]
                transaction = int(row[3].translate({ord(c): None for c in '£.'}))
                # TODO: Parse to integer value of pennies
                # TODO: Config file
            except IndexError:
                continue
            except ValueError:
                continue
            transactions.append({
                'date': date,
                'transaction': transaction,
                'merchant': merchant})
        return transactions

def sort_chronologically(transactions):
    new_transactions = sorted(transactions, key=lambda k: k['date']) 
    return new_transactions

def write_to_csv(transactions, filename):
    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=';',
                                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(['Date', 'Merchant', 'Transaction'])
        for row in transactions:
            csvwriter.writerow([str(row['date']), row['merchant'], row['transaction']])
        csvwriter.writerow(['', 'Total', total(transactions)])

def beautify(transactions):
    col_width = 40
    for row in sort_chronologically(transactions):
        print("".join(str(row[key]).ljust(col_width) for key in row))

def total(transactions):
    sum = 0
    for row in transactions:
        sum += int(row['transaction'])
    return sum

# INIT
t = init_monzo()
parse_monzo(t)
santanderTransactions = init_santander(cfg.santander_statement)
monzoTransactions = parse_monzo(init_monzo())
transactions = santanderTransactions + monzoTransactions
# PRINT
# beautify(transactions)
print(total(transactions))
print('Choose a filename to write to: ')
filename = str(input(">>> "))
write_to_csv(sort_chronologically(transactions), filename)
