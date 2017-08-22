from monzo.monzo import Monzo # Import Monzo Class
from dateutil import parser
import pytz
import config as cfg
import csv
import datetime
from openpyxl.styles import colors
from openpyxl.styles import Font, Color
from openpyxl import Workbook


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
                date = datetime.datetime.strptime(row[0], "%d/%m/%Y" ).replace(tzinfo=pytz.UTC)
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
    # transactions.sort(key=lambda item:item['date'])
    transactions = sorted(transactions, key=lambda k:k['date'])
    return transactions

def to_2sf(value):
    return float(str.format('{0:.2f}',value/100))

def to_pounds(pence):
    value = to_2sf(pence)
    if value[0] == '-':
        value = value[1:]
        prefix = "-£"
    else:
        prefix = "+£"
    return prefix + value

def format_for_display(transactions):
    for row in transactions:
        row['date'] = row['date'].strftime('%d/%m/%y')
        row['transaction'] = to_pounds(row['transaction'])
        print(row)
    return transactions

def write_to_csv(transactions, filename):
    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=';',
                                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(['Date', 'Merchant', 'Transaction', 'Balance'])
        cumulative_total = 0
        for row in transactions:
            cumulative_total += int(row['transaction'])
            csvwriter.writerow([str(row['date']), row['merchant'], row['transaction'], cumulative_total])
        csvwriter.writerow(['', 'Total', total(transactions)])

def beautify(transactions):
    col_width = 40
    for row in sort_chronologically(transactions):
        print("".join(str(row[key]).ljust(col_width) for key in row))

def excel_autofit(ws):
    # from https://stackoverflow.com/questions/39529662/python-automatically-adjust-width-of-an-excel-files-columns
    for col in ws.columns:
        max_length = 0
        column = col[0].column # Get the column name
        for cell in col:
            try: # Necessary to avoid error on empty cells
                if len(str(cell.value)) > max_length:
                    max_length = len(cell.value)
            except:
                pass
        adjusted_width = (max_length + 2) * 1.2
        ws.column_dimensions[column].width = adjusted_width

def excel_export(transactions, filename):
    wb = Workbook()

    # grab the active worksheet
    ws = wb.active
    ws.title = "Spending Summary"

    ws.append(["Category", "Total"])
    header_font = Font(bold=True)
    for row in ws.iter_rows(min_row=1, max_col=2, max_row=1):
        for cell in row:
            cell.font = header_font
    for category in cfg.outgoings_categories:
        ws.append([category, '=SUMPRODUCT((TransactionList!D2:D{1}="{0}")*TransactionList!C2:C{1})'.format(category, len(transactions)+20)])
    # append sum of outgoings
    ws.append(["Total Outgoings", '=SUM(B2:B{})'.format(len(cfg.outgoings_categories)+1)])
    for row in ws.iter_rows(min_row=len(cfg.outgoings_categories)+2, max_col=1, max_row=len(cfg.outgoings_categories)+2):
        for cell in row:
            cell.font = header_font
    for category in cfg.income_categories:
        ws.append([category, '=SUMPRODUCT((TransactionList!D2:D{1}="{0}")*TransactionList!C2:C{1})'.format(category, len(transactions)+20)])
    # append sum of incomes
    incomeStart = len(cfg.outgoings_categories)+3
    incomeEnd = incomeStart + len(cfg.income_categories) - 1
    ws.append(["Total Income", '=SUM(B{}:B{})'.format(incomeStart, incomeEnd)])
    # append sum of both
    ws.append(["Balance", '=B{}+B{}'.format(len(cfg.outgoings_categories)+2, incomeEnd+1)])
    for row in ws.iter_rows(min_row=incomeEnd+1, max_col=2, max_row=incomeEnd+2):
        for cell in row:
            cell.font = header_font
    ws1 = wb.create_sheet("TransactionList")
    ws1.append(['Date', 'Merchant', 'Transaction', "Category"])
    for row in ws1.iter_rows(min_row=1, max_col=4, max_row=1):
        for cell in row:
            cell.font = header_font
    for transaction in transactions:
        ws1.append([transaction['date'], transaction['merchant'], to_2sf(transaction['transaction'])])
    excel_autofit(ws)
    excel_autofit(ws1)
    # Save the file
    wb.save(filename)
    print("Saved. Don't forget to check cell references - it might not be perfect.")
    import subprocess
    subprocess.Popen(["libreoffice", filename])

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
beautify(sort_chronologically(transactions))
