from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name',
                  'last_name',
                  'email',
                  'address',
                  'postal_code',
                  ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': "form-control",
                                             'id': "first_name",
                                             'placeholder': 'Имя'}),
            'last_name': forms.TextInput(attrs={'class': "form-control",
                                             'id': "last_name",
                                             'placeholder': 'Фамилия'}),
            'email': forms.TextInput(attrs={'class': "form-control",
                                             'id': "email",
                                             'placeholder': 'example@gmail.com'}),
            'address': forms.TextInput(attrs={'class': "form-control",
                                             'id': "address",
                                             'placeholder': 'г. Бишкек, ул. Манас 7'}),
            'postal_code': forms.TextInput(attrs={'class': "form-control",
                                             'id': "postal_code",
                                             'placeholder': '720017'}),
            
        }