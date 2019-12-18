from django import forms


class SetTime(forms.Form):
    hh = forms.CharField(max_length=2)
    mm = forms.CharField(max_length=2)


class TicketInfo(forms.Form):
    ticket_number = forms.CharField(max_length=10)