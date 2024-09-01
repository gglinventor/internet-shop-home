import re
from django import forms

class CreateOrderForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    phone_number = forms.CharField()
    requires_delivery = forms.ChoiceField(
        choices=[
            ("0", 'False'),
            ("1", 'True'),
        ],
    )
    delivery_address = forms.CharField(required=False)
    payment_on_get = forms.ChoiceField(
        choices=[
            ("0", 'False'),
            ("1", 'True'),
            ],
        )
    
    def clean_phone_number(self): #"clean_" - нужно чтобы django понял, что это дополнительная валидация
        data = self.cleaned_data['phone_number']
        if not data.isdigit():
            raise forms.ValidationError("Номер телефона должен содержать только цифры")
        
        pattern = re.compile(r'^\d{11}$') #"re" - регулярные выражения, "r'^\d{11}$'" - число из 11 цифр
        if not pattern.match(data):
            raise forms.ValidationError("Неверный формат номера")
        
        return data
    
    def clean_delivery_address(self):
        requires_delivery = self.cleaned_data['requires_delivery']
        delivery_address = self.cleaned_data['delivery_address']
        if requires_delivery == '1' and len(delivery_address) == 0:
            raise forms.ValidationError('Введите адрес доставки')

        return delivery_address