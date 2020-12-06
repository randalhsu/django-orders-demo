from django import forms
from .models import *


class AddNewOrderForm(forms.Form):
    product_id = forms.ChoiceField(label='Select Product')
    # TODO: max_value ban
    qty = forms.IntegerField(label='Quantity', min_value=1, initial=1)
    customer_id = forms.IntegerField(
        label='Customer ID', min_value=1, initial=1)
    customer_is_vip = forms.BooleanField(label='I am VIP', required=False)

    def __init__(self, *args, **kwargs):
        super(AddNewOrderForm, self).__init__(*args, **kwargs)
        choices = []
        for product in Product.objects.all():
            choices.append(
                (product.product_id, f'Product ID: {product.product_id}'))
        self.fields['product_id'].choices = choices
