from django import forms


class SignUpForm(forms.Form):
    email = forms.EmailField(label='Email address', max_length=100,
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email address'}))
    password = forms.CharField(label='Password', max_length=100,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    card_number = forms.CharField(label='Card Number', max_length=16,
                                  widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Card Number'}))
    cvv_code = forms.CharField(label='CVV Code', max_length=4,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CVV Code'}))
    expiry_date = forms.CharField(label='Expiry Date', max_length=5,
                                  widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'MM/YY'}))


class SignInForm(forms.Form):
    email = forms.EmailField(label='Email address', max_length=100,
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email address'}))
    password = forms.CharField(label='Password', max_length=100,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
