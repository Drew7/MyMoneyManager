from django import forms
from django.forms import inlineformset_factory
from .models import Document, DocumentItem


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['document_type', 'number', 'active', 
                  'counterparty', 'wallet', 'currency', 'amount', 'user', 'comment']



class NewDocumentForm(forms.ModelForm):

    class Meta:
        model = Document
        fields = ['document_type', 'number', 'active', 
                  'counterparty', 'wallet', 'currency', 'amount', 'user', 'comment']


class NewDocumentItemForm(forms.ModelForm):
    class Meta:
        model = DocumentItem
        fields = ['expense_item', 'income_item', 'quantity', 'amount',
                  'comment', 'document']

DocumentFormSet = inlineformset_factory(Document, DocumentItem, form=NewDocumentItemForm, extra=1)
