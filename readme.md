# bank

bank is a little script I'm working on mostly for personal purposes. I'm hoping it'll let you get your bank statement from whichever banks you use.

## Current capabilities

- List your transactions in one Monzo account
- Sort lists of transactions chronologically and by month
- Work out the total cost of all transactions in a given statement
- Export these as CSV, with a cumulative balance column
- Export these in Excel format, with a summary of which categories you've spent your money in.
  Note that filling this in is a **manual process**. You need to go through the D column and fill in which category each purchase was made in. However, you can at least take pride in the fact that any changes you make are reflected in the Spending Summary, since it sums from the statement sheets.
- Combine most of the above functions

It's **currently nothing more than a convenience script at the minute**, but if it's of significant use to some, I'll definitely invest more time in it. For now, I'm perfecting it for my own use case only. If you're a dab hand at Python, replace the closing lines (init section and export) with the methods you need. 

For example, use the existing methods to `init`ialise and `parse` your transactions, then in the final line:

- run `beautify(transactions)`for clean terminal output of your statement
- run `write_to_csv(transactions, "transactions.csv")`to create a CSV statement
- run `excel_export(sort_months(transactions))` for a forecast of the entire time instance, with each month's transaction on its own sheet.

I'd like it to recognise regular merchants and assume the transaction category, like Monzo does, but that would require extending their method of choosing tags in a major way for it to be intelligent at all. From then, it'd be hard to automate it any further.

## Usage

Define the following variables in config.py:

- outgoings_categories: a list of names of categories in which you spend your money, such as food, transport, etc.
- income_categories: a list of names of categories in which you receive money, such as wages, student loan, etc.

Additionally, configure `pymonzo` either with their setup documentation.

Please fork and PR if you'd like to develop functionality for a bank you use!

### On previous functionality

`bank` previously supported the legacy bank Santander. I am no longer a customer of theirs, but please investigate the `legacy-santander` branch if you are still a customer and wish to use `bank` to parse your statements.
