from django import forms


class PaymentForm(forms.Form):
    card_number = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder':'Card Number'}), required=True)
    card_name = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder':'Card Name'}), required=True)
    card_expiry = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder':'Card Expiry'}), required=True)
    card_cvv = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder':'Card CVV'}), required=True)


    