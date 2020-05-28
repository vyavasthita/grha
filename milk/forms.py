from django import forms
from .models import Service


class SupplyViewForm(forms.Form):
    start_date = forms.CharField(label='From', widget=forms.widgets.DateTimeInput(attrs={"type": "date"}))
    end_date = forms.DateField(label='To', widget=forms.widgets.DateTimeInput(attrs={"type": "date"}))


class SupplyUpdateForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = '__all__' #['supplier', 'date', 'quantity', 'rate', 'remark']
    
        widgets = {
                'date': forms.DateInput(format=('%m/%d/%Y'), attrs={'type':'date'}),
            }