from django import forms 
from accounts.models import Account
from category.models import Category
from store.models import Product

class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('first_name','last_name','username','email','phone_number')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('category_name','slug','description','cat_image')

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('product_name','slug','price','stock','category','is_available')

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'



