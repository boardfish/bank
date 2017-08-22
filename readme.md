# bank

bank is a little script I'm working on mostly for personal purposes. I'm hoping it'll let you get your bank statement from whichever banks you use.

## Current capabilities

- List your transactions in one Monzo account and one Santander account
- Sort lists of transactions chronologically
- Work out the total cost of all transactions in a given statement
- Export these as CSV, with a cumulative balance column
- Combine the above functions

It's **currently nothing more than a convenience script at the minute**, so don't expect it to do much... At least not until I've developed the following features:

- Export your transactions in one unified sheet, or several separate sheets
- Sort your transactions into categories and figure out how much you've spent where each month
- Recognise regular merchants and assume the transaction category

Define the following variables in config.py:

- santander_statement: the location of the file containing your Santander statement, exported as a Midata CSV. Currently no API is exposed, meaning fetching the CSV needs to be done manually.
- monzo_token: your access token for Monzo. You'll need to fetch this every time, but I'll patch in OAuth2 support, which I've been told is a more laborious process that pays off in the long run.

Please fork and PR if you'd like to develop functionality for a bank you use! Naturally it'll be hard for me to test such a thing without an account, so a little bit of faith might be necessary on my part.
