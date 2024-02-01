from django import forms

from .models import Subcategory,Products
class SubcategoryForm(forms.ModelForm):
    class Meta:
        model=Subcategory
        fields=['sub_name', 'sub_img', 'cat_id']
        labels= {
            'sub_name':'SubCategory Name',
            'sub_img':'SubCategory image',
            'cat_id':'Category id',
        }


    def __init__(self,*args,**kwargs):
        super(SubcategoryForm,self).__init__(*args,**kwargs)
        self.fields['cat_id'].empty_label="Select"
class ProductsForm(forms.ModelForm):
    class Meta:
        model=Products
        fields=['pr_name', 'cat_id', 'brand_id', 'subcat_id', 'is_available']
        labels={
            'pr_name':'Product Name',
            'cat_id':'Category',
            'brand_id':'Brand',
            'subcat_id':'Subcategory',
            'is_available':'Active',

        }
    def set_empty_label(self, field_name):
        self.fields[field_name].empty_label = "Select"

    def __init__(self, *args, **kwargs):
        super(ProductsForm, self).__init__(*args, **kwargs)
        # Set empty_label for cat_id and brand_id
        self.set_empty_label('cat_id')
        self.set_empty_label('brand_id')
        self.set_empty_label('subcat_id')