# bank

bank is a little script I'm working on mostly for personal purposes. I'm hoping it'll let you get your bank statement from whichever banks you use.

## Current capabilities

- List your transactions in one Monzo account and one Santander account
- Sort lists of transactions chronologically
- Work out the total cost of all transactions in a given statement
- Export these as CSV, with a cumulative balance column
- Export these as Excel, with a summary of which categories you've spent your money in.
  Note that for now that filling this in is a **manual process**. You need to go through the D column and fill in which category each purchase was made in.
- Combine most of the above functions

It's **currently nothing more than a convenience script at the minute**, but if it's of significant use to some, I'll definitely invest more time in it. For now, I'm perfecting it for my own use case only.

- Recognise regular merchants and assume the transaction category

Define the following variables in config.py:

- santander_statement: the location of the file containing your Santander statement, exported as a Midata CSV. Currently no API is exposed, meaning fetching the CSV needs to be done manually.
- monzo_token: your access token for Monzo. You'll need to fetch this every time, but I'll patch in OAuth2 support, which I've been told is a more laborious process that pays off in the long run.
- outgoings_categories: a list of names of categories in which you spend your money.
- income_categories: a list of names of categories in which you receive money, such as wages, student loan, etc.

Please fork and PR if you'd like to develop functionality for a bank you use! Naturally it'll be hard for me to test such a thing without an account, so a little bit of faith might be necessary on my part.
