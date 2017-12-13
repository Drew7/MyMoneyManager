from django.contrib import admin
from .models import Counterparties, Expense_item, Income_item, Wallets_and_Accounts, Document, DocumentItem, Currency, Country, Bank, Exchange_rate

admin.site.register(Counterparties)
admin.site.register(Expense_item)
admin.site.register(Income_item)
admin.site.register(Wallets_and_Accounts)
admin.site.register(Document)
admin.site.register(DocumentItem)
admin.site.register(Currency)
admin.site.register(Country)
admin.site.register(Bank)
admin.site.register(Exchange_rate)