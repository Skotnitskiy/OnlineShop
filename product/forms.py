from django import forms

from product.models import OrderDetails


class AddProductForm(forms.Form):
    next = forms.CharField(widget=forms.HiddenInput())
    product_id = forms.CharField(widget=forms.HiddenInput())
    quantity = forms.IntegerField(min_value=1)


class DelProductForm(forms.Form):
    product_id = forms.CharField(widget=forms.HiddenInput())


class OrderForm(forms.ModelForm):
    class Meta:
        model = OrderDetails
        fields = '__all__'
