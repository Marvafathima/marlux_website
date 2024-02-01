from django import forms

from .models import Subcategory
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