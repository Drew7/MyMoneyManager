from django.contrib.auth.models import User
from mymoneymanager.models import Document, DocumentItem, Currency, Wallets_and_Accounts, Income_item, Expense_item, Counterparties

user = User.objects.first()
currency = Currency.objects.first()
wallet = Wallets_and_Accounts.objects.first()
income = Income_item.objects.first()
expense = Expense_item.objects.first()
counterparty = Counterparties.objects.first()
active = True

for i in range(100):
    if i%2 == 0:
        document_type = "EXPENCE"
        expense = Expense_item.objects.first()
        income = None
    else:
        document_type = "INCOME"
        income = Income_item.objects.first()
        expense = None
    
    comment = 'Comment test #{}'.format(i)
    document = Document.objects.create(document_type=document_type, active=active, counterparty=counterparty, wallet = wallet, currency = currency, amount = 1000 * i, user = user, comment = comment)
    
    DocumentItem.objects.create(expense_item=expense, income_item=income, quantity=i, amount = i * 25, comment = comment, document = document)
    DocumentItem.objects.create(expense_item=expense, income_item=income, quantity=i, amount = i * 26, comment = comment, document = document)
    DocumentItem.objects.create(expense_item=expense, income_item=income, quantity=i, amount = i * 27, comment = comment, document = document)
    DocumentItem.objects.create(expense_item=expense, income_item=income, quantity=i, amount = i * 28, comment = comment, document = document)
    DocumentItem.objects.create(expense_item=expense, income_item=income, quantity=i, amount = i * 29, comment = comment, document = document)
    DocumentItem.objects.create(expense_item=expense, income_item=income, quantity=i, amount = i * 30, comment = comment, document = document)