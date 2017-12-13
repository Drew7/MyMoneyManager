from django.db import models
from django.contrib.auth.models import User


class Currency(models.Model):

    name = models.CharField(max_length=30, unique=True)
    active = models.BooleanField()

    digital_code = models.PositiveSmallIntegerField(unique=True)
    char_code = models.CharField(max_length=3, unique=True)
    upload_rates = models.BooleanField()

    def __str__(self):
        return self.name


class Country(models.Model):

    name = models.CharField(max_length=120, unique=True)
    active = models.BooleanField()

    digital_code = models.PositiveSmallIntegerField(unique=True)
    char_code = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class Bank(models.Model):

    name = models.CharField(max_length=120, unique=True)
    active = models.BooleanField()

    digital_code = models.PositiveSmallIntegerField(unique=True)
    char_code = models.CharField(max_length=30, unique=True)
    country = models.ForeignKey(Country, related_name='banks')

    def __str__(self):
        return self.name

class Exchange_rate(models.Model):

    date_of_rate = models.DateTimeField()
    bank = models.ForeignKey(Bank, related_name='Exchange_rates')
    currency = models.ForeignKey(Currency, related_name='Exchange_rates_currency')
    base_currency = models.ForeignKey(Currency, related_name='Exchange_rates_base_currency')
    rate = models.DecimalField(max_digits=16, decimal_places=6)
    multiplicity = models.PositiveIntegerField()

    def __str__(self):
        return "{:%Y-%m-%d} {} {} {}".format(self.date_of_rate, self.bank, self.currency, self.base_currency)


class Wallets_and_Accounts(models.Model):

    CASH = 'Cash'
    CREDITCARD = 'Credit_Card'
    WALLET_TYPE_CHOICES = (
        (CASH, 'Cash'),
        (CREDITCARD, 'Credit card'),
    )

    name = models.CharField(max_length=30, unique=True)
    active = models.BooleanField()
    wallet_type = models.CharField(
        max_length=30, choices=WALLET_TYPE_CHOICES, default=CASH)
    currency = models.ForeignKey(
        Currency, related_name='Wallets_and_Accounts_currency')

    def __str__(self):
        return self.name


class Income_item(models.Model):

    name = models.CharField(max_length=30, unique=True)
    active = models.BooleanField()

    def __str__(self):
        return self.name


class Expense_item(models.Model):

    name = models.CharField(max_length=30, unique=True)
    active = models.BooleanField()
    quantitative = models.BooleanField()

    def __str__(self):
        return self.name


class Counterparties(models.Model):

    name = models.CharField(max_length=30, unique=True)
    active = models.BooleanField()

    contacts = models.CharField(max_length=120, blank=True)
    comment = models.CharField(max_length=120, blank=True)

    def __str__(self):
        return self.name


class Document(models.Model):

    EXPENCE = 'EXPENCE'
    INCOME = 'INCOME'
    DOCUMENT_TYPE_CHOICES = (
        (EXPENCE, 'EXPENCE'),
        (INCOME, 'INCOME'),
    )

    document_type = models.CharField(
        max_length=30, choices=DOCUMENT_TYPE_CHOICES, default=EXPENCE)

    number = models.AutoField(primary_key=True)
    active = models.BooleanField()
    document_date = models.DateTimeField(auto_now_add=True)

    counterparty = models.ForeignKey(
        Counterparties, related_name='Expence_counterparty')
    wallet = models.ForeignKey(
        Wallets_and_Accounts, related_name='Expence_wallet')
    currency = models.ForeignKey(Currency, related_name='Expence_currency')

    amount = models.DecimalField(max_digits=16, decimal_places=6)

    user = models.ForeignKey(User, related_name='Expence_user')
    comment = models.CharField(max_length=120, blank=True)

    def __str__(self):
        return 'Document {} number {} as of {}'.format(self.document_type, self.number, self.document_date)


class DocumentItem(models.Model):

    expense_item = models.ForeignKey(
        Expense_item, related_name='Expense_item_expense_item', blank=True, null=True)
    income_item = models.ForeignKey(
        Income_item, related_name='Income_item_income_item', blank=True, null=True)
    quantity = models.DecimalField(max_digits=16, decimal_places=6)
    amount = models.DecimalField(max_digits=16, decimal_places=6)
    comment = models.CharField(max_length=120, blank=True)
    document = models.ForeignKey(Document, related_name='Document_expense')

    def __str__(self):
        return 'Expence {} or income {} of {}'.format(self.expense_item, self.income_item, self.document)
