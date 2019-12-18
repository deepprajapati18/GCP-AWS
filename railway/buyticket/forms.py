from django import forms


class TicketForm(forms.Form):
    privateKey = forms.CharField(max_length=100)
    ticket_number = forms.CharField(max_length=10)
    price = forms.CharField(max_length=5)
