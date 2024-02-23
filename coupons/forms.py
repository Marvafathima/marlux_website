# from django import forms
# from .models import Coupon
# from category .models import Category,Products

# class CouponForm(forms.ModelForm):
#     class Meta:
#         model = Coupon
#         fields = ['code', 'discount_amount', 'discount_percentage', 'expiration_date', 'usage_limit', 'applicable_categories', 'applicable_products', 'minimum_order_amount', 'active', 'user_limit', 'description']

#     applicable_categories = forms.ModelMultipleChoiceField(
#         queryset=Category.objects.all(),
#         widget=forms.CheckboxSelectMultiple
#     )

#     applicable_products = forms.ModelMultipleChoiceField(
#         queryset=Products.objects.all(),
#         widget=forms.CheckboxSelectMultiple
#     )