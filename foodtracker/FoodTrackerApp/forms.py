from django import forms

from .models import Food,Category


class FoodForm(forms.ModelForm):

    class Meta():
        model = Food
        fields = ('food_name','category','quantity','calories','fat','carbohydrates','protein','food_img','info')
        category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label=None)
        def __init__(self, *args, **kwargs):
            super(FoodForm, self).__init__(*args, **kwargs)
            for visible in self.visible_fields():
                visible.field.widget.attrs['class'] = 'form-control'


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name',)
